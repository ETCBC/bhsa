---
title: otype
---

**node type**

Types for text objects.
As text objects are represented by nodes in
[Text-Fabric](https://github.com/ETCBC/text-fabric/wiki),
we shall use both *object* and *node* without much consistency.  

---|---|---
`word`         |slot          |single word, fills a *slot*; sometimes words are not separated by a space
`lex`          |--            |lexeme, contains all slots of occupied by its occurrences
`subphrase`    |functional    |part of a phrase
`phrase`       |functional    |phrase, maybe with gaps
`phrase_atom`  |distributional|maximal consecutive part of a phrase
`clause`       |functional    |clause, maybe with gaps
`clause_atom`  |distributional|maximal consecutive part of a clause
`sentence`     |functional    |clause, maybe with gaps
`sentence_atom`|distributional|maximal consecutive part of a sentence
`half_verse`   |section       |main division of the verse, usually into two, somtimes into three parts
`verse`        |section       |numbered unit of a chapter
`chapter`      |section       |numbered unit of a book
`book`         |section       |named part of the Bible

All objects have a type, which is just a label.
Objects and their slots are represented in Text-Fabric as *nodes*.
The information which object occupies which slot is stored in the edge feature [oslots](oslots).

---|---
[Section types](#section-types)        |division in books, chapters, etc
[Word type](#word-type)                |all about the individual words
[Linguistic types](#linguistic-types)  |phrases, clauses, etc

# Section types

The section types correspond to the various divisional units in the Bible.
The Hebrew Bible is divided in books, books are divided in chapters, chapters are divided in verses, and verses in half-verses.
The sectional types
`book`, `chapter`, `verse`, and `half_verse`
specify features which indicate which book, chapter, verse, half-verse their objects refer to.

A `book` object carries the [book](book) feature, which contains the name of the book.
A `chapter` object carries the [chapter](chapter) feature, which contains the number of the chapter.
It carries also the [book](book) feature to indicate the book of which it is a chapter.
Analogously, the `verse` object carries the [verse](verse) feature, which contains the number of the chapter,
and the [book](book) and [chapter](chapter) features.
Additionally, the `verse` object also carries [label](label), which contains a label string indicating the passage.
However, the `half_verse` object only carries the [half_verse](half_verse) feature, which contains a key for the half-verse.

# Word type

There is only one type for words, the `word` type.
Word objects correspond to the smallest divisional units in the ETCBC4 dataset.
They are also identified with *slots*, because each slot is filled by a word and each word fills a slot.
Words are not identified with strings, because there are various
string representations of the words, none of which is canonical. All word occurrences are numbered
with a slot number.

There are many features that have related forms, e.g. `vbe`, `g_vbe` and `g_vbe_utf8`.
The `g_` versions have *graphical* values, meaning that it contains the *pointing*,
i.e. all diacritics that occur in the full text.
For the purpose if this documentation, we shall use the contrast *consonantal* (without diacritics)
and *pointed* (with diacritics).
The `_utf8` versions contain UNICODE representations of the values, using the Hebrew code block.
The non `_utf8` versions contain ASCII representations of the values, according to the
[ETCBC transliteration table](https://shebanq.ancient-data.org/shebanq/static/docs/ETCBC4-transcription.pdf). 

The text of a word occurrence is in
[g_word](g_word) (pointed, transliterated) and [g_word_utf8](g_word_utf8) (pointed, Hebrew),
[g_cons](g_cons) (consonantal, transliterated) and [g_cons_utf8](g_cons_utf8) (consonantal, Hebrew).
None of these features contains material from in between words.
In order to get inter-word material, use 
[trailer_utf8](trailer_utf8).

Word occurrences corresponds to lexemes, i.e. dictionary entries, for which we have a separate object type.
For the textual representation of lexemes we have a variety of features, in order to get their 
consonantal values:
---|---
[lex](lex) | transcription
[lex0](lex0) | transcription without disambiguation characters at the end
[lex_utf8](lex_utf8) | Hebrew

or their vocalized values:

---|---
[g_lex](g_lex) | transcription
[g_lex_utf8](g_lex_utf8) | Hebrew

# Lexeme type

The type `lex` corresponds to lexemes. A lexeme object occupies the slots of all its occurrences.
It does not fit into the hierarchy, because these objects will very rarely lie embedded in another object.
Except if a lexeme is rare.

##### Hint
> Have a look at the [tutorial](https://github.com/ETCBC/text-fabric/blob/master/docs/tutorial.ipynb)
so see how you could exploit this object type to find
lexemes that are unique to books or chapters very easily.

##### Caution
> Precisely because of the non-embedding of lexemes in other object types, its use
in MQL queries is limited. In Text-Fabric there are no problems.
See the note in [gloss](gloss).

# Linguistic types

Linguistic types correspond to syntactical entities such as sentences, clauses and phrases.
The ETCBC4 distinguishes between *functional* and *distributional* variants of them.
The functional object types are `sentence`, `clause`, and `phrase`.
They correspond to possibly discontinuous stretches of text that function as a unit.
The distributional object types are `sentence_atom`, `clause_atom`, and `phrase_atom`.
They are continuous stretches of text within their functional counterparts.
So the functional objects consist of sequences of the corresponding distributional objects, and any gaps in
the functional object fall neatly between their distributional atoms.

##### Note
> More explanation needed about the distributional and functional objects hierarchies and how they hang together.
Is `subphrase` functional or distributional?
Are atoms always *maximal* continous stretches, or can you have two adjacent atoms of the same type?

See the [AtomsAndMothers notebook](https://github.com/ETCBC/text-fabric-data/blob/master/docs/notebooks/AtomsAndMothers.ipynb)
which makes some basic explorations into these matters.

##### Note
> If you are writing an MQL query, there is not a feature as such in which the type is stored.
Rather you refer to the type when you write the building blocks such as `[word ...]` or
`[clause_atom [phrase ]]`. 

The *otype* feature has the same values as the possible names of the MQL blocks.

##### Hint
> In Text-Fabric we have developed a new way of querying.
Read more in
[searchTutorial](/etcbc/text-fabric/blob/master/docs/searchTutorial.ipynb).
