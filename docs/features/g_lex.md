---
title: g_lex
---

**lexeme -pointed-transliterated**


The pointed representation of the lexeme of a word occurrence in 
[BHSA transliteration]({{tfd}}/writing/hebrew.html).

This feature is present on objects of type [*word*](otype.md).

The vowels and consonants of the word lexeme are present; a lexeme does not have other diacritical marks.

##### Note
> There is no disambiguation material at the end of the value such as in [lex](lex.md).

##### Hint
> Generally, this is a handy feature to search for specific words.
If you are unsure how exactly the lexeme of a particular word is spelled, it is handy to search in the
frequency table of values: `F.g_lex.freqList()`

##### Hint
> Try also regular expression matching of features, which is supported by MQL. For an example, see [lex](lex.md).

##### See also

* [voc_lex](voc_lex.md), a related feature defined on object type *lex*.
