Interword material -pointed-Hebrew ``trailer_utf8``
-------------------------------------------------------------------------------
:doc:`frequency table of values <../index/trailer_utf8>`

The material that follows the word in question, up till the next word.

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

See also:

* :doc:`ketiv <ketiv>`. 
* :doc:`g_qere_utf8 <g_qere_utf8>`. 
* :doc:`g_word_utf8 <g_word_utf8>`. 
* :doc:`qtrailer_utf8 <qtrailer_utf8>`. 
