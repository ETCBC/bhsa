Rank-occurrence ``rank_occ``
-------------------------------------------------------------------------------
The rank of a word occurrence, a measure related to its frequency.

This feature is present on objects of type *word*.

What is counted is the consonantal representation of the words, without accents.

The rank of an item is the number of items that have a higher frequency.
So items with rank 0 have the highest frequency.
If two or more items have identical frequency, they have the same rank, but the rank immediately below is not one lower, but *n* lower,
where *n* is the amount of items with that same frequency.

.. note::
    This feature does not distinguish between homonyms, i.e. it counts representations and lexeme distinctions
    are not taken into account.

.. hint::
    The measures *frequency* and *rank* have been computed for *lexemes* and *occurrences*.
    
This feature has been added to the database in a later stage as package called ``lexicon``.

You can use it in SHEBANQ queries.

If you want to use it in LAF-Fabric, you have to load ``lexicon`` as *annox*.
Consult the `LAF-Fabric API reference on annoxes <http://laf-fabric.readthedocs.io/en/latest/texts/API-reference.html#extra-annotation-packages>`_.

See also:
 
* :doc:`freq_lex <freq_lex>`
* :doc:`rank_lex <rank_lex>`
* :doc:`freq_occ <freq_occ>`
* :doc:`rank_occ <rank_occ>`

