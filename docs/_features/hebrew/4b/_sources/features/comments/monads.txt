Monad set ``monads``
----------------------------------------------------
:doc:`frequency table of values <../index/monads>`

The set of monads associated with an object.

Every object corresponds to exactly one *monad set*,
i.e. the set of *word occurrences* that form the textual representation of that object.
Every word is a monad, and every monad has a unique sequence number. Earlier words have lower numbers than later words.
An object does not have to be consecutive, it may be interrupted at any place.
Different objects may or may not overlap.

The monad set is given as a comma separated list of monad *ranges*, where a range has the form *n* ``-`` *m*,
where *n* is a number smaller than or equal to *m*. The range *n* ``-`` *n* may be abbreviated to *n*.

.. note::
    The value of these feature for word objects is always just one number.
    All word occurrences are numbered from 1 to more than 400,000, in the order as they occur in the Hebrew Bible.

.. caution::
    There might be gaps in the word numbering between books of the Bible.

The
:doc:`frequency table of values <../index/monads>`
does not show all monad sets that the objects of the ETCBC4 data have, because that would be an unwieldingly long list.
It does contain, however, the top of the list, where you see some monad sets that are shared by 8 objects.

If you want to see which objects make up such a case, look at
`this notebook <https://shebanq.ancient-data.org/shebanq/static/docs/tools/shebanq/monadsets.html>`_
which looks up such a case by means of LAF-Fabric.
