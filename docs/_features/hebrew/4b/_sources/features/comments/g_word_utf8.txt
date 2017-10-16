Word -pointed-Hebrew ``g_word_utf8``
-----------------------------------------------------------------
:doc:`frequency table of values <../index/g_word_utf8>`

The pointed representation of a word occurrence in Hebrew script.

This feature is present on objects of type *word*.

All characters of the word occurrence are present: consonants, vowel pointing and other diacritical marks.

.. caution::
    When there is a ketiv-qere discrepancy, this feature contains the *unvocalized* **ketiv**.
    In those cases, SHEBANQ does not use this feature, but takes the *vocalized* **qere** from
    :doc:`g_qere_utf8 <g_qere_utf8>`,
    which is not in the ETCBC database proper. It has been added as an extra annotation package to LAF-Fabric and SHEBANQ.
    Nevertheless you can also use the vocalized qere in MQL queries.
    The value of ``g_word_utf8`` is retained in a pseudo feature :doc:`ketiv <ketiv>`, and can be inspected in SHEBANQ
    through the data view.
    See for example `Genesis 12:8 <https://shebanq.ancient-data.org/hebrew/text?book=Genesis&chapter=12&verse=8&tp=txt_p>`_

.. hint::
    It is hazardous to use this feature for queries. From how a Hebrew word looks in printing, it cannot be determined what the
    order of the various diacritics of one and the same consonant is.
    The order, chosen in the ETCBC4 database is such that the rendering gives optimal results for most applications.
    The ETCBC4 is not committed to maintain a definite ordering here.

    In order not to miss search results, it might be helpful to compare the results with those obtained by using
    :doc:`g_cons_utf8 <g_cons_utf8>` instead.

.. hint::
    It is difficult to enter Hebrew text. One of the handiest ways to get Hebrew text into a query is to copy and paste it
    from some other Hebrew text, e.g. from the `SHEBANQ <http://shebanq.ancient-data.org>`_.
    However, the shebanq application has inserted blank spaces inside some words in order to work around some font rendering
    problems. See `this notebook <https://shebanq.ancient-data.org/shebanq/static/docs/tools/shebanq/font-rendering.html>`_
    for more information.

    You could try to copy and paste Hebrew text into a word processor, then remove all diacritics, and paste the result into
    your query as a value for :doc:`g_cons <g_cons>`.

See also:

* :doc:`ketiv <ketiv>`. 
* :doc:`g_qere_utf8 <g_qere_utf8>`. 
* :doc:`trailer_utf8 <trailer_utf8>`. 
* :doc:`qtrailer_utf8 <qtrailer_utf8>`. 
