---
title: `txt`
---

**text type**


This feature contains property at the level of text.

This feature is present on objects of type
[`clause`](otype.md).

The values of this feature are strings consisting of

code|description
---|---
`?`|Unknown
`N`|Narrative
`D`|Discursive
`Q`|Quotation

##### See also

* [`domain`](domain.md)
* [`instruction`](instruction.md)
* A presentation about [text type](../assets/img/txt.pdf)

Text type is a feature of a *clause*, and not of an object type higher 
in that hierarchy, because sometimes sentences are built from
clauses of distinct text types. So a text type transition does not imply 
a new (sub-)paragraph. Nor does a new (sub-)paragraph imply a text type transition.

Within one and the same *clause*, every `clause_atom` must have the 
same value for text type. The sequence of characters corresponds with embedding, 
so a *clause* having the value `QND`, for example, stands for a discursive piece within 
a narrative, enclosed in direct speech.

****Discursive****
In a discursive text the author addresses the reader directly to
supply him with a piece of background information. It is marked by
the use of a yiqtol (not wayyiqtol) in a narrative environment.

****Quotation****
A `Q` may, but does not always have to be indicated by a *verbum dicendi*: אָמַר or דָּבַר. 

##### Note
> What exactly is the connection with [`domain`](domain.md)?

