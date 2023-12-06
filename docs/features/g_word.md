---
title: `g_word`
---

**word -pointed-transliterated**


The pointed representation of a word occurrence in
[BHSA transliteration]({{tfd}}/writing/hebrew.html).

This feature is present on objects of type
[`word`](otype.md).

All characters of the word occurrence are present:
consonants, vowel pointing and other diacritical marks.

??? hint
    It is hazardous to use this feature for queries.
    From how a Hebrew word looks in printing,
    it cannot be determined what the
    order of the various diacritics of one and the same consonant is.
    The order, chosen in the BHSA dataset is such that the rendering
    gives optimal results for most applications.
    The BHSA is not committed to maintain a definite ordering here.

    In order not to miss search results,
    it might be helpful to compare the results with those obtained by using
    [`g_cons`](g_cons.md) instead.

??? caution "Paseq"
    Some accents in a word can interact with a *paseq*
    in the following `trailer`.
    See [Cantillation](../cantillation.md).

??? example "example query"
    Here is an example query:
    [setumah and petuhah]({{shebanq}}/hebrew/text?mr=r&qw=q&iid=499) .
