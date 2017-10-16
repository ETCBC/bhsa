Vocalized lexeme -pointed-hebrew ``g_entry_heb``
------------------------------------------------
The pointed representation of the lexeme of a word occurrence in Hebrew script.

This feature is present on objects of type *word*.

Only the consonants and vowels of the word lexeme are present: no other diacritical marks.

The values of *vocalized lexeme* look like the values of the :doc:`g_lex_utf8 <g_lex_utf8>` feature
of word occurrences, but they are not the same.
The *vocalized lexeme* is an idealized (aka *paradigmatic*), pointed representation of the lexeme,
which may or may not occur in the text.
The :doc:`g_lex_utf8 <g_lex_utf8>` is the realized lexeme in a concrete occurrence, of which it may be a part.

.. note:: 
    This is not a feature of the ETCBC4 Hebrew Text Database.
    Every word occurrence in the database is linked to a lexicon entry.
    The values of *vocalized lexeme* are given in the lexicon only.

.. hint::
    In LAF-Fabric, the lexicon material is added, rather uneconomically, as extra features 
    of the word occurrences. 
    You can load these features by invoking the extra annotation package *lexicon*, and after
    that the vocalized lexeme can be used under the name ``g_entry_heb``.

