Gloss ``gloss``
---------------
A short English translation of a single word, disregarding context.

This feature is present on objects of type *word*.

The *gloss* cannot be used to generate a proper translation.
Many words have multiple meanings and a good translation chooses between them.
The glosses are not guaranteed to mention all possible meanings, and they 
do not contain heuristics which meanings should be selected in which contexts.

The *gloss* is useful for users with limited knowledge of Hebrew to get an impression
of what the text they are reading is about.

This feature has been added to the database in a later stage as package called ``lexicon``.

You can use it in SHEBANQ queries.

If you want to use it in LAF-Fabric, you have to load ``lexicon`` as *annox*.
Consult the `LAF-Fabric API reference on annoxes <http://laf-fabric.readthedocs.io/en/latest/texts/API-reference.html#extra-annotation-packages>`_.

.. note:: 
    This is not a feature of the ETCBC4 Hebrew Text Database.
    Every word occurrence in the database is linked to a lexicon entry.

.. hint::
    In LAF-Fabric, the lexicon material is added, rather uneconomically, as extra features 
    of the word occurrences. 
