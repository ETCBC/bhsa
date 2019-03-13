---
title: g_word_utf8
---

**word -pointed-Hebrew**


The pointed representation of a word occurrence in Hebrew script.

This feature is present on objects of type [*word*](otype.md).

All characters of the word occurrence are present: consonants, vowel pointing and other diacritical marks.

##### Note
> When there is a ketiv-qere discrepancy, this feature contains the *unvocalized* **ketiv**.
In those cases, SHEBANQ does not use this feature, but takes the *vocalized* **qere** from
[qere_utf8](qere_utf8.md).

##### Hint
> It is hazardous to use this feature for queries. From how a Hebrew word looks in printing, it cannot be determined what the
order of the various diacritics of one and the same consonant is.
The order, chosen in the BHSA dataset is such that the rendering gives optimal results for most applications.
The BHSA is not committed to maintain a definite ordering here.

In order not to miss search results, it might be helpful to compare the results with those obtained by using
[g_cons_utf8](g_cons_utf8.md) instead.

##### Hint
> It is difficult to enter Hebrew text. One of the handiest ways to get Hebrew text into a query is to copy and paste it
from some other Hebrew text, e.g. from the [SHEBANQ]({{shebanq}}).
However, the shebanq application has inserted blank spaces inside some words in order to work around some font rendering
problems.

You could try to copy and paste Hebrew text into a word processor, then remove all diacritics, and paste the result into
your query as a value for [g_cons](g_cons.md).

##### See also

* [qere](qere.md). 
* [qere_utf8](qere_utf8.md). 
* [trailer_utf8](trailer_utf8.md). 
