Ketiv
-----
The unpointed representation of a ketiv word occurrence in Hebrew script when there is a divergent qere.

This feature is present on objects of type *word*.

When there is a ketiv-qere discrepancy, this feature contains the *unvocalized* **ketiv**.
In those cases, *but only in those cases*, it is identical to the contents of :doc:`g_word_utf8 <g_word_utf8>` feature.

See for an example `Genesis 12:8 <https://shebanq.ancient-data.org/hebrew/text?book=Genesis&chapter=12&verse=8&tp=txt_p>`_

.. caution::
    In cases where the ketiv is different from the qere, the qere is not present as a real feature that you can query in SHEBANQ.
    You can find ketivs in the :doc:`g_word_utf8 <g_word_utf8>` - feature of words that have a masora sign.
    So query for::
    
        [word g_word ~ '\*']

See also:

* :doc:`g_qere_utf8 <g_qere_utf8>`. 
* :doc:`g_word_utf8 <g_word_utf8>`. 
* :doc:`trailer_utf8 <trailer_utf8>`. 
* :doc:`qtrailer_utf8 <qtrailer_utf8>`. 
