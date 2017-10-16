Text type ``txt``
----------------------------------------------------
:doc:`frequency table of values <../index/txt>`

This feature contains property at the level of text.

This feature is present on objects of type *clause*.

The values of this feature are strings consisting of

===== ==============
``?`` Unknown
``N`` Narrative
``D`` Discursive
``Q`` Quotation
===== ==============

See also :doc:`domain <domain>`.

Text type is a feature of a *clause*.
That means that within one and the same clause, every *clause_atom* must have the same value for text type.
The sequence of characters corresponds with embedding, so a clause having NQQ means that it is a quotation
in a quotation in a narrative.

.. caution::
    What exactly is the connection with :doc:`domain <domain>`?

