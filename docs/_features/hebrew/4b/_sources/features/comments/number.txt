Sequence number ``number``
-------------------------------------------------
:doc:`frequency table of values <../index/number>`

The sequence number of an object within its context.

This feature is present on objects of type *sentence(_atom)*, *clause(_atom)*, *phrase(_atom)*, *word*.


.. note::
    This feature does not occur on *subphrases*.
    However, SHEBANQ shows subphrase numbering in *data view*. 
    Subphrases my be nested in intricate ways. 
    Shebanq shows for every word the sequence numbers of the subphrases it belongs to.
    Subphrases are numbered per containing phrase.

Numbering starts with 1.
The manner of numbering objects differs per object type:

============= =====================
phrase_atom   within the book
clause_atom   within the book
sentence_atom within the book
word          within the book
phrase        within the clause
clause        within the sentence
sentence      within the chapter
============= =====================

.. caution::
    An explanation of the rationale behind these numbering schemes would be helpful.

As you can see, this feature can be used to find the first or second or third phrase in a clause or clause in a sentence.
However, it is not obvious how to specify the first word in a phrase with the help of the *number* feature.
But if you are in the business of MQL query writing, there is a better way.

.. hint::
    The MQL language contains the keyword ``FIRST`` by which you can indicate that you mean the first object
    in its context. The use of it is nicely demonstrated in this query on 
    `SHEBANQ <http://shebanq.ancient-data.org/hebrew/query?id=519>`_ by Reinoud Oosting. The query is also a beautiful
    example of establishing whether an anomalous pattern is really exceptional or occurs more often.
    For more info about what you can say in MQL, consult the well-written
    `reference manual <https://shebanq.ancient-data.org/shebanq/static/docs/MQL-Query-Guide.pdf>`_
    by the implementor of MQL, Ulrik Petersen.

.. hint::
    You can compute distances between *atoms* by subtracting their *number* features.
