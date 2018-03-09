---
title: distributional_parent
---

**Edge feature**.

Linguistic types correspond to syntactical entities such as sentences, clauses
and phrases. The BHSA distinguishes between *functional* and *distributional*
variants of them. The functional object types are `sentence`, `clause`, and
`phrase`. They correspond to possibly discontinuous stretches of text that
function as a unit. The distributional object types are `sentence_atom`,
`clause_atom`, and `phrase_atom`. They are continuous stretches of text within
their functional counterparts. So the functional objects consist of sequences of
the corresponding distributional objects, and any gaps in the functional object
fall neatly between their distributional atoms.

The distributional parent of a node is the embedding node in the distributional
hierarchy.

##### Note #####

> More explanation needed about the distributional and functional objects
> hierarchies and how they hang together.

##### See also #####

*   [functional_parent](functional_parent)
*   [mother](mother)
