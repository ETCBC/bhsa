---
title: `pdp`
---

**phrase dependent part-of-speech**

This feature is present on objects of type
[`word`](otype.md).

The part of speech that is assigned to a word based on its phrase context rather than on its lexical identity.

For example, in

    "**The** is a very frequent word in English."

the word **The** acts as a noun and not as an article, so its `pdp` would be `subst` instead of `art`.


The values consist of an abbreviation, here is the explanation:

code|description
---|---
`art`  |article
`verb` |verb
`subs` |noun
`nmpr` |proper noun
`advb` |adverb
`prep` |preposition
`conj` |conjunction
`prps` |personal pronoun
`prde` |demonstrative pronoun
`prin` |interrogative pronoun
`intj` |interjection
`nega` |negative particle
`inrg` |interrogative particle
`adjv` |adjective
