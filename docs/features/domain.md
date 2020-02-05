---
title: domain
---

**domain**


This feature contains property at the level of text.

This feature is present on objects of type [*clause*](otype.md).

code|description
---|---
`?`|Unknown
`N`|Narrative
`D`|Discursive
`Q`|Quotation

##### See also

* [txt](txt.md)


The domain feature is the most embedded (i.e. the last letter of the) value returned by the feature [txt](txt.md).
Example: The sequence of characters corresponds with embedding, so a clause having the txt value “QND”, will return the domain “D”. 

##### Definition 

A domain is characterised by the four main participants that constitute the communication. In theory there are two sets of ‘owners’, one viewed from the outside (Speaker and Audience), and one viewed from the inside of the domain (Sender and Addressee).

* *speaker*: Actor who is the source of the communication, viewed from **outside** the domain.
* *audience*: Actor to whom the communication is directed, viewed from **outside** the domain.
* *sender*: Actor who is the source of the communication, viewed from **within** the domain.
* *addressee*: Actor to whom the communication is directed, viewed from **within** the domain.

##### Note
> The connection with [txt](txt.md) needs more clarification. 

##### Hint
> Here is a sophisticated query by Oliver Glanz that makes use of this
feature. It detects deviations in a discourse pattern. See the query
on [SHEBANQ]({{shebanq}}/hebrew/query?id=491).

