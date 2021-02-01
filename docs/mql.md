# Text-Fabric versus SHEBANQ

The [ETCBC]({{institute}}) provides two tools to work with its dataset of linguistic annotations
to the Hebrew Bible.

One is [SHEBANQ]({{shebanq}}) which provides a human readable view on the data on the basis of which researchers
can write queries. SHEBANQ is an **online** tool that offers to save such queries and show them next to the relevant chapters of the Bible.

SHEBANQ is best used for drawing attention of fellow researchers to interesting patterns in the Hebrew Bible.
It even provides visualizations of result sets, which can also be downloaded as `.csv` files.

Nevertheless, SHEBANQ falls short for those researchers that want to perform statistical analysis on the data.
These researchers need to preprocess the data in ways that an application author cannot anticipate.

The good news is the existence of the other tool,
[Text-Fabric]({{tfd}}).
This is an **offline** tool based on exactly the same data that powers SHEBANQ.
The programming researcher can use Text-Fabric as a preprocessing tool for transforming the complex BHSA data into the formats that are suitable to
R, spreadsheets, or any format of choice.
Text-Fabric is open source, downloadable from [GitHub]({{tf}}),
and the data is downloadable from [bhsa]({{repo}}).

It can be installed on MacOS, Windows and Linux.
The recommended mode of working with the data is: programming in Python within a Jupyter Notebook.

## Tutorial

Text-Fabric is ideal if you interested in a certain phenomenon and you want to gather data about that phenomenon.
Take for example the following notebook:

* [start]({{tut}}/start.ipynb)
* [search]({{tut}}/search.ipynb)

This points to an explorative way of researching syntactical patterns, without knowing in advance how exactly
the data is organized.

## Text-Fabric versus MQL

The queries in SHEBANQ are based on MQL, the query language of
[Emdros]({{emdros}}).

In Text-Fabric we have *search templates*, that can do similar things as MQL queries, but not exactly the same.
TF-search and MQL-queries have different strengths and weaknesses.
See the examples in 

* [search vs MQL]({{tut}}/searchFromMQL.ipynb)

where we translate a number of MQL queries that are shared by SHEBANQ into Text-Fabric search templates.

## Differences between TF-search and MQL-queries

* **MQL-queries** is richer than TF-search query in some respects, while in order areas TF-search is more refined.
  * both can specify refined feature conditions on objects (feature `NOT IN` values; feature `~` regular expression);
  * MQL can specify `NOT EXIST` blocks, which has no parallel in TF-search;
  * TF-search has quantifiers /with/, /without/, /where/ which do not have direct counterparts in MQL;
* **TF-search** is more flexible in dealing with spatial relationships between objects
  * you can leave the order between objects free, or constrain it as you wish
  * you can use a variety of relations like *adjacent before*, *same slots*, *overlapping*, *embedded* and more to express
    spatial relationships;
* **MQL-queries** requires separate software, Emdros, plus a database (MYSQL or SQLite), plus a dataset converted to MQL, in
  order to work with it. There is some friction if you want to issue an Emdros query from a Python3 program
  and process its results by the same program;
* **TF-search** works wherever Text-Fabric works, is totally integrated with it, and results are being delivered
  as Python tuples that are extremely easy to process further;
* **MQL-queries** is implemented in C + backend database, and has a really good performance;
* **TF-search** is implemented in pure Python, and requires more memory and more CPU time, although performance is quite acceptable.
* **MQL-queries** let you define your search criteria very well, but it is poor in letting you specify the context information
  of results that you want to fetch as well;
* **TF-search** lets you focus on search criteria; because you can process the results after the search, it is very easy to
  draw in context information at will.
   
## Pitfalls of MQL

You can also use MQL to get a limited amount of context information.
If you have a query that pinpoints the textual phenomenon that you are after,
you can wrap context objects around it.
But this turns out to be risky, because
there might be unexpected misses.
For example, if you look for: 

```
[phrase function = 'Pred' [word first lex = 'NTN[']]
```

and you want to collect the passage information as well, you want to say this:

```
[book [chapter [verse [sentence
  [phrase function = 'Pred' [word first lex = 'NTN[']]
]]]]
```

then you miss the cases where a sentence spans more than one verse!

And if you want the other words or phrases in the same clause as the target phrase, you want something like:

```
[book [chapter [verse [sentence
  [clause
    [phrase first]
    [phrase function = 'Pred' [word first lex = 'NTN[']]
    [phrase]*
    [phrase last]
   ]
]]]]
```

But what if the target phrase is itself the first one, or the last one, or both?
We need to distinguish cases:

```
[book [chapter [verse [sentence
  [clause
    [phrase first and last function = 'Pred' [word first lex = 'NTN[']]
    OR
    [phrase first function = 'Pred' [word first lex = 'NTN[']]
    [phrase]*
    [phrase last]
    OR
    [phrase first]
    [phrase]*
    [phrase last function = 'Pred' [word first lex = 'NTN[']]
    OR
    [phrase first]
    [phrase]*
    [phrase function = 'Pred' [word first lex = 'NTN[']]
    [phrase]*
    [phrase last]
   ]
]]]]
```

This is not pleasant and it is still wrong, because if the clause has gaps, and those gaps occur between phrases,
then any such clause will not be found by this query.
We have to say this instead:

```
[book [chapter [verse [sentence
  [clause
    [phrase first and last function = 'Pred' [word first lex = 'NTN[']]
    OR
    [phrase first function = 'Pred' [word first lex = 'NTN[']]
    [[phrase][gap?]]*
    [phrase last]
    OR
    [phrase first]
    [[phrase][gap?]]*
    [phrase last function = 'Pred' [word first lex = 'NTN[']]
    OR
    [phrase first]
    [[phrase][gap?]]*
    [phrase function = 'Pred' [word first lex = 'NTN[']]
    [[phrase][gap?]]*
    [phrase last]
   ]
]]]]
```

And still we will miss results, because the target phrase may occur in a phrase that itself fills the gap inside another phrase.
These thing are not academic, they occur in the BHSA data! In order to get them the size of this query will explode,
completely obscuring the intention of it.

Using TF-search, you can avoid all this trouble by just issuing the search template

```python
S.study('''
phrase function= Pred
  word lex=NTN[
''')
```

and then processing the results, with complete access to any part of the context:

```python
for (phrase, word) in S.fetch():
    (book, chapter, verse) = T.sectionFromNode(phrase)
    clause = L.u(phrase, otype='clause')
    # etc
``` 
