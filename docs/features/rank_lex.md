---
title: `rank_lex`
---

**rank-lexeme**

The rank of a lexeme, a measure related to its frequency.

This feature is present on objects of type
[`lex`](otype.md).

The rank of an item is the number of items that have a higher frequency.
So items with rank 0 have the highest frequency.
If two or more items have identical frequency, they have the same rank, but the rank immediately below is not one lower, but `n` lower,
where `n` is the amount of items with that same frequency.

##### Note
> The BHSA lexicon makes distinctions between homonyms, i.e. distinct lexemes that are spelled identically.
This feature respects that distinction.

##### Hint
> The measures *frequency* and *rank* have been computed for *lexemes* and *occurrences*.
    
##### See also
 
* [`freq_lex`](freq_lex.md)
* [`rank_lex`](rank_lex.md)
* [`freq_occ`](freq_occ.md)
* [`rank_occ`](rank_occ.md)

