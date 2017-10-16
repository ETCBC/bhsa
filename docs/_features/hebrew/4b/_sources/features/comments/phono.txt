Word -full-phonetic ``phono``
-----------------------------------------------------------------------------
The phonetic representation of a word occurrence.

This feature is present on objects of type *word*.

There is also a feature ``phono_sep`` which gives the material between the next word and the current word.

If you concatenate the ``phono`` and ``phono_sep`` features of each word, you get the complete text with correct
spacing and newlines in phonetic representation.

The full Hebrew word has been transcribed, and accents have been transformed to primary and secondary stress marks.
For full details, consult the SHEBANQ tool `phono <https://shebanq.ancient-data.org/tools?goto=phono>`_.

This feature has been added to the database in a later stage as package called ``lexicon``.

You can use it in SHEBANQ queries.

If you want to use it in LAF-Fabric, you have to load ``lexicon`` as *annox*.
Consult the `LAF-Fabric API reference on annoxes <http://laf-fabric.readthedocs.io/en/latest/texts/API-reference.html#extra-annotation-packages>`_.

