---
title: otype
---

**node type**

Types for text objects.
As text objects are represented by nodes in
[Text-Fabric]({{tfd}}),
we shall use both *object* and *node* without much consistency.  

type|kind|description
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
The information which object occupies which slot is stored in the edge feature [oslots](oslots.md).

type|description
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

A `book` object carries the [book](book.md) feature, which contains the name of the book.
A `chapter` object carries the [chapter](chapter.md) feature, which contains the number of the chapter.
It carries also the [book](book.md) feature to indicate the book of which it is a chapter.
Analogously, the `verse` object carries the [verse](verse.md) feature, which contains the number of the chapter,
and the [book](book.md) and [chapter](chapter.md) features.
Additionally, the `verse` object also carries [label](label.md), which contains a label string indicating the passage.
However, the `half_verse` object only carries the [half_verse](label.md) feature, which contains a key for the half-verse.

# Word type

There is only one type for words, the `word` type.
Word objects correspond to the smallest divisional units in the BHSA dataset.
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
[BHSA transliteration]({{tfd}}/Writing/Hebrew.html).

The text of a word occurrence is in
[g_word](g_word.md) (pointed, transliterated) and [g_word_utf8](g_word_utf8.md) (pointed, Hebrew),
[g_cons](g_cons.md) (consonantal, transliterated) and [g_cons_utf8](g_cons_utf8.md) (consonantal, Hebrew).
None of these features contains material from in between words.
In order to get inter-word material, use 
[trailer_utf8](trailer_utf8.md).

Word occurrences corresponds to lexemes, i.e. dictionary entries, for which we have a separate object type.
For the textual representation of lexemes we have a variety of features, in order to get their 
consonantal values:

code|description
---|---
[lex](lex.md) | transcription
[lex0](lex0.md) | transcription without disambiguation characters at the end
[lex_utf8](lex_utf8.md) | Hebrew

or their vocalized values:

code|description
---|---
[g_lex](g_lex.md) | transcription
[g_lex_utf8](g_lex_utf8.md) | Hebrew

# Lexeme type

The type `lex` corresponds to lexemes. A lexeme object occupies the slots of all its occurrences.
It does not fit into the hierarchy, because these objects will very rarely lie embedded in another object.
Except if a lexeme is rare.

##### Hint
> Have a look at
[start]({{repoBase}}/tutorial/start.ipynb).
so see how you could exploit this object type to find
lexemes that are unique to books or chapters very easily.

##### Caution
> Precisely because of the non-embedding of lexemes in other object types, its use
in MQL queries is limited. In Text-Fabric there are no problems.
See the note in [gloss](gloss.md).

# Linguistic types

Linguistic types correspond to syntactical entities such as sentences, clauses and phrases.
The BHSA distinguishes between *functional* and *distributional* variants of them.
The functional object types are `sentence`, `clause`, and `phrase`.
They correspond to possibly discontinuous stretches of text that function as a unit.
The distributional object types are `sentence_atom`, `clause_atom`, and `phrase_atom`.
They are continuous stretches of text within their functional counterparts.
So the functional objects consist of sequences of the corresponding distributional objects, and any gaps in
the functional object fall neatly between their distributional atoms.

##### Note by Cody Kingham (on the etcbc-vu slack)
> If you are looking for a sort of neat and tidy definition of
what constitutes a “phrase” or “clause” in the ETCBC,
you will probably come away disappointed.
In its database methodology, the ETCBC purposely avoided strict linguistic definitions
and sought to build up phrase and clause boundaries with a bottom-up method.
There are a handful of helpful formal rules that were discovered and integrated into the programs.
For instance, one rule used by the data creation programs for detecting clause endings is
to examine parts of speech on either side of a waw conjunction.
If the part of speech to the left of the conjunction was different than the one to the right,
it likely indicates a clause boundary.
For both clause and phrase segmentation, there is a kind of default list of part of speech patterns
called a phrase set.
As new patterns are found in the text during an encoding,
they were added to the phrase set to be utilized in the next analysis.
> But with all of that said, here is my best try at summarizing a kind of definition of
clauses and phrases for the etcbc:
> Clauses and phrases are functional linguistic units made up of their distributional parts,
i.e. atoms, which are themselves recognizable through regular patterns in the language
that can be detected through computer-assisted cataloguing and analysis.
> The most comprehensive and informative summary on how clause/phrases are defined and identified in the ETCBC
is Eep Talstra 2003 [Text segmentation and linguistic levels - Preparing data for SESB](https://etcbc.github.io/bhsa/references#talstra-eep-2003).
> Cody Kingham (Slack message)

##### Note
> More explanation needed about the distributional and functional objects hierarchies and how they hang together.
* Is `subphrase` functional or distributional?
* Are atoms always *maximal* continous stretches, or can you have two adjacent atoms of the same type?

See the [AtomsAndMothers notebook]({{repoBase}}/programs/AtomsAndMothers.ipynb)
which makes some basic explorations into these matters.

##### Note
> If you are writing an MQL query, there is not a feature as such in which the type is stored.
Rather you refer to the type when you write the building blocks such as `[word ...]` or
`[clause_atom [phrase ]]`. 

The *otype* feature has the same values as the possible names of the MQL blocks.

##### Hint
> In Text-Fabric we have developed a new way of querying.
Read more in
[search]({{repoBase}}/tutorial/search.ipynb).
