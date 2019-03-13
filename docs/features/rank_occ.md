---
title: rank_occ
---

**rank-occurrence**

The rank of a word occurrence, a measure related to its frequency.

This feature is present on objects of type [*word*](otype.md).

What is counted is the consonantal representation of the words, without accents.

The rank of an item is the number of items that have a higher frequency.
So items with rank 0 have the highest frequency.
If two or more items have identical frequency, they have the same rank, but the rank immediately below is not one lower, but *n* lower,
where *n* is the amount of items with that same frequency.

##### Note
> This feature does not distinguish between homonyms, i.e. it counts representations and lexeme distinctions
are not taken into account.

##### Hint
> The measures *frequency* and *rank* have been computed for *lexemes* and *occurrences*.
    
##### See also
 
* [freq_lex](freq_lex.md)
* [rank_lex](rank_lex.md)
* [freq_occ](freq_occ.md)
* [rank_occ](rank_occ.md)

