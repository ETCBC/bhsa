---
title: dist_unit
---

**distance to mother unit**


The unit of measuring the distance between the present object (daughter) and its mother object.

This feature is present on objects of types [*subphrase*, *phrase_atom*, *phrase*, *clause_atom*, *clause*](otype.md).

code|description
---|---
`words`       |distance measured in words
`phrase_atoms`|distance measured in phrase_atoms
`clause_atoms`|distance measured in clause_atoms

For explanation of what the *mother* of an object is, see [mother](mother.md).
The mother is always a *word*, a *phrase* or a *clause* and we measure distances between mothers and daughters in
*words*, *phrase_atoms* and *clause_atoms* respectively.

##### See also

* [dist](dist.md)

