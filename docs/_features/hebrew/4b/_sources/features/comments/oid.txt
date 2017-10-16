Object identifier ``oid``
------------------------------------------------------------
:doc:`frequency table of values <../index/oid>`

Database identifier of the object.

This feature is present on objects of any type.

The objects are numbered. No two objects have the same number, so a sentence can not have the same object identifier as a word.
The object identifiers carry no meaning, but various extractions of the data may contain these numbers.
This can help to locate objects found in one extraction of the data in an other extraction.

.. note::
    If you are writing an MQL query, use the feature *self*.

    If you are doing LAF processing, use the feature *oid*.

    The LAF *oid* feature has per object exactly the same value as the MQL *self* value.

We omit the complete list of values for this feature. They are all numbers, and all identifiers occur exactly once.
