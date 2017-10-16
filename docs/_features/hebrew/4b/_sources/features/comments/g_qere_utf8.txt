Word -pointed-Hebrew (qere) ``g_qere_utf8``
-----------------------------------------------------------------

The pointed representation of a qere word occurrence in Hebrew script when there is a divergent ketiv.

This feature is present on objects of type *word*.

When there is a ketiv-qere discrepancy, this feature contains the *vocalized* **qere**.
In all other cases this feature is empty.

See for an example `Genesis 12:8 <https://shebanq.ancient-data.org/hebrew/text?book=Genesis&chapter=12&verse=8&tp=txt_p>`_

.. note::
    In cases where the ketiv is different from the qere, the qere has been added to the ETCBC database in a later stage.
    Nevertheless, you can use this feature in queries in SHEBANQ.

This feature has been added to the database in a later stage as package called ``lexicon``.

You can use it in SHEBANQ queries.

If you want to use it in LAF-Fabric, you have to load ``lexicon`` as *annox*.
Consult the `LAF-Fabric API reference on annoxes <http://laf-fabric.readthedocs.io/en/latest/texts/API-reference.html#extra-annotation-packages>`_.

See also:

* :doc:`ketiv <ketiv>`. 
* :doc:`g_word_utf8 <g_word_utf8>`. 
* :doc:`trailer_utf8 <trailer_utf8>`. 
* :doc:`qtrailer_utf8 <qtrailer_utf8>`. 
