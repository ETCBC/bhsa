Interword material -pointed-Hebrew (qere) ``qtrailer_utf8``
-------------------------------------------------------------------------------

The material that follows the word in question, up till the next word, but only when occurring in a qere different from the ketiv.

This feature is present on objects of type *word*.

The value consists of spaces, newlines, punctuations and special marks that sometimes occur between verses, such as the
*nun hafukha*, and the *samekh* and *pe* markers.

.. hint::
    Not all words in Hebrew are separated by a space.
    This feature is the only one that gives the information whether there is a
    space between words.

.. note::
    After the last word of a verse, a newline has been inserted in the ETCBC4 working text.
    This newline has become part of the
    :doc:`trailer_utf8 <trailer_utf8>` value of the last word of the verse.

    This feature is only present with values in UNICODE Hebrew.

This feature has been added to the database in a later stage as package called ``lexicon``.

You can use it in SHEBANQ queries.

If you want to use it in LAF-Fabric, you have to load ``lexicon`` as *annox*.
Consult the `LAF-Fabric API reference on annoxes <http://laf-fabric.readthedocs.io/en/latest/texts/API-reference.html#extra-annotation-packages>`_.

See also:

* :doc:`ketiv <ketiv>`. 
* :doc:`g_qere_utf8 <g_qere_utf8>`. 
* :doc:`g_word_utf8 <g_word_utf8>`. 
* :doc:`trailer_utf8 <trailer_utf8>`. 
