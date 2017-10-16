Object type ``otype``
------------------------------------------------------
:doc:`frequency table of values <../index/otype>`

Database type of the object.

================= ============== ================================================================================
``word``          monad          single word, also known as *monad*. Sometimes words are not separated by a space
``subphrase``     functional     part of a phrase
``phrase``        functional     phrase, maybe with gaps
``phrase_atom``   distributional maximal consecutive part of a phrase
``clause``        functional     clause, maybe with gaps
``clause_atom``   distributional maximal consecutive part of a clause
``sentence``      functional     clause, maybe with gaps
``sentence_atom`` distributional maximal consecutive part of a sentence
``half_verse``    section        main division of the verse, usually into two, somtimes into three parts
``verse``         section        numbered unit of a chapter
``chapter``       section        numbered unit of a book
``book``          section        named part of the Bible
================= ============== ================================================================================

All objects have a type.
The type of an object determines which features are defined for that object.
The description of object types is facilitated by organizing them in groups, but these
groups do not form a formal concept.

======================================   =================================
:ref:`Section types <sectiont>`          division in books, chapters, etc
:ref:`Word type <wordt>`                 all about the individual words
:ref:`Linguistic types <linguisticst>`   phrases, clauses, etc
======================================   =================================

.. _sectiont:

Section types
^^^^^^^^^^^^^
The section types correspond to the various divisional units in the Bible.
The Hebrew Bible is divided in books, books are divided in chapters, chapters are divided in verses, and verses in half-verses.
The sectional types
``book``, ``chapter``, ``verse``, and ``half_verse``
specify features which indicate which book, chapter, verse, half-verse their objects refer to.

A ``book`` object carries the :doc:`book <book>` feature, which contains the name of the book.
A ``chapter`` object carries the :doc:`chapter <chapter>` feature, which contains the number of the chapter.
It carries also the :doc:`book <book>` feature to indicate the book of which it is a chapter.
Analogously, the ``verse`` object carries the :doc:`verse <verse>` feature, which contains the number of the chapter,
and the :doc:`book <book>` and :doc:`chapter <chapter>` features.
Additionally, the ``verse`` object also carries :doc:`label <label>`, which contains a label string indicating the passage.
However, the ``half_verse`` object only carries the :doc:`half_verse <half_verse>` feature, which contains a key for the half-verse.

.. _wordt:

Word type
^^^^^^^^^
There is only one type for words, the ``word`` type.
Word objects correspond to the smallest divisional units in the ETCBC4 database.
They are also called *monads*. Words are not identified with strings, because there are various
string representations of the words, none of which is canonical. All word occurrences are numbered
with a monad number (:doc:`monads <monads>`).

There are many features that have related forms, e.g. ``vbe``, ``g_vbe`` and ``g_vbe_utf8``.
The ``g_`` versions have *graphical* values, meaning that it contains the *pointing*, i.e. all diacritics that occur in the full text.
For the purpose if this documentation, we shall use the contrast *consonantal* (without diacritics) and *pointed* (with diacritics).
The ``_utf8`` versions contain UNICODE representations of the values, using the Hebrew code block.
The non ``_utf8`` versions contain ASCII representations of the values, according to the
`ETCBC transliteration table <http://shebanq.ancient-data.org/shebanq/static/docs/ETCBC4-transcription.pdf>`_. 

The text of a word occurrence is in
:doc:`g_word <g_word>` (pointed, transliterated) and :doc:`g_word_utf8 <g_word_utf8>` (pointed, Hebrew),
:doc:`g_cons <g_cons>` (consonantal, transliterated) and :doc:`g_cons_utf8 <g_cons_utf8>` (consonantal, Hebrew).
None of these features contains material from in between words.
In order to get inter-word material, use 
:doc:`trailer_utf8 <trailer_utf8>`.

Word occurrences corresponds to lexemes, i.e. dictionary entries.
For the textual representation of lexemes we have a variety of features, in order to get their 
consonantal values:
:doc:`lex <lex>` (transcription), 
:doc:`lex_utf8 <lex_utf8>` (Hebrew)
or their vocalized values:
:doc:`g_lex <g_lex>` (transcription),
:doc:`g_lex_utf8 <g_lex_utf8>` (Hebrew).

.. _linguisticst:

Linguistic types
^^^^^^^^^^^^^^^^
Linguistic types correspond to syntactical entities such as sentences, clauses and phrases.
The ETCBC4 distinguishes between *functional* and *distributional* variants of them.
The functional object types are ``sentence``, ``clause``, and ``phrase``.
They correspond to possibly discontinuous stretches of text that function as a unit.
The distributional object types are ``sentence_atom``, ``clause_atom``, and ``phrase_atom``.
They are continuous stretches of text within their functional counterparts.
So the functional objects consist of sequences of the corresponding distributional objects, and any gaps in
the functional object fall neatly between their distributional atoms.

.. caution::
    More explanation needed about the distributional and functional objects hierarchies and how they hang together.
    Is ``subphrase`` functional or distributional?
    Are atoms always *maximal* continous stretches, or can you have two adjacent atoms of the same type?

.. note::
    If you are writing an MQL query, there is not a feature as such in which the type is stored.
    Rather you refer to the type when you write the building blocks such as ``[word ...]`` or
    ``[clause_atom [phrase ]]``. 
    
    But If you are doing LAF processing, there is the feature *otype*.

    The LAF *otype* feature has the same values as the possible names of the MQL blocks.

.. hint::
    If you need the object hierarchy in order to provide context around patterns of interest, you can start with a query in SHEBANQ
    and then turn to LAF-Fabric. Read more in :doc:`/texts/context`.

See the
:doc:`frequency table of values <../index/otype>`
for a quick overview of the number of objects in the ETCBC4 database for each given type. 

