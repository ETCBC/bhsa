---
title: lex
---

**lexeme -consonantal-transliterated**


The consonantal representation of the lexeme of a word occurrence in
[BHSA transliteration]({{tfd}}/Writing/Hebrew.html).

This feature is present on objects of type [*word* and *lex*](otype.md).

Only the consonants of the word lexeme are present: no vowel pointing and no other diacritical marks.

##### Note
> If you need to distinguish between them, you can use the feature [language](language.md).
 
##### Note
> There is disambiguation material at the end of the value.
If the lexeme is a verb, a `[` is added, if it is a noun, a `/` is added.
If there are more than one lexemes with the same consonants, they are disambiguated by adding
zero or more `=` s to the values.

There is also a feature [lex0](lex0.md) where the disambiguation material is stripped of.

##### Hint
> Generally, this is a handy feature to search for specific words.
If you are unsure how exactly the lexeme of a particular word is spelled, it is handy to search in the
frequency table of values: `F.lex.freqList()`

##### Hint
> Try also regular expression matching of features, which is supported by MQL. Example::

    [word lex ~ '.*RMW?N.*']

>finds the following lexemes::

        >RMWN/     (x 32)
        RMWN/      (x 32)
        XRMWN/     (x 13)
        RMWN=/     (x  7)
        GT_RMWN/   (x  4)
        <JN_RMWN/  (x  3)
        RMWN==/    (x  3)
        RMWN===/   (x  3)
        <RMWN/     (x  2)
        B<L_XRMWN/ (x  2)
        RMWN_PRY/  (x  2)
        >RMNJ/     (x  1)
        HDD_RMWN/  (x  1)
        HRMWN/     (x  1)
        RMWNW/     (x  1)
        VBRMN/     (x  1)
        XRMWNJM/   (x  1)


