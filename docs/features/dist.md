---
title: `dist`
---

**distance to mother**

The distance between the present object (daughter) and its mother object.

This feature is present on objects of types
[`subphrase`, `phrase_atom`, `phrase`, `clause_atom`, `clause`](otype.md).

For explanation of what the *mother* of an object is, see [`mother`](mother.md).
The interpretation of the value of *dist* is dependent on the type of the mother, which can be read off
the value of [`dist_unit`](dist_unit.md) of this object.
The rules are a bit involved, but here we go.

The mother is always a *word*, a *phrase* or a *clause* and we measure distances between mothers and daughters in
*words*, `phrase_atoms` and `clause_atoms` respectively.

If we measure in words, we take the difference between the max [`oslot`](oslots.md) values of the mother and the daughter. 
If we measure in *clause/phrase-atoms*, we take the difference of the [`number`](number.md) values
of the mother and the daughter.

##### Note
> Or must we take the [`number`](number.md) of the clause/phrase-atom that the daughter occurs in?

Why is distance useful?
Examples needed.

Incomplete *dist* information.
Inspection has shown that many clause atoms lack values for *dist*.
Workaround: use the difference between between the *number* features directly.
