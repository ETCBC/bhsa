---
title: `mother`
---

**edge feature, indicating linguistic dependency between elements that do not
necessarily have an embedding relationship.**

An ETCBC interactive encoding program `sy04types` presents for each clause one or more mother clauses in
which it could be anchored. A clause’s possible mother clauses are ranked in order of probability. This
ranking is based on multiple types of observations:

* grammatical and lexical correspondences between a clause and its possible mother clause;
* the number of earlier occurrences of a similar clause connection;
* the distance (in clause atoms) between the two clauses. 

Eventually, it is the analyst who has to decide which of the proposed clause connections is the most adequate one. His or her decisions are tabulated in different levels of indentations reflecting parallel or dependent relations between
connected clauses. (Kalkman, *Verbal Forms in Biblical Hebrew Poetry*, 2015, p. 118)

The mother relation exists between objects of many different kinds. The feature
[`code`](code.md) refers to it a lot.

See the
[`AtomsAndMothers` notebook]({{repoBase}}/programs/AtomsAndMothers.ipynb)
which makes some basic explorations into these matters.

##### Caution #####

> This description needs more body: what objects can be mothers, what daughters?
> What is the linguistic meaning of mother in all those cases? Are there formal
> characteristics indicating a mother relationship? Examples needed!

Examples
========

MQL Implementation
------------------

In MQL, *mother* is not a feature, but it is possible to query with conditions
involving the *mother*.

Here is a query that looks up occurrences of the word *swear* (`CB<`) if it
occurs in a clause atom that is the mother of a following clause which is a
quotation (`txt = 'Q'`):

```
select all objects where
[verse
    [clause_atom as c1
        [word focus lex = "CB<["
        ]
    ]
    ..
    [clause txt = 'Q'
        [clause_atom mother has c1.self
        ]
    ]
]
```

**N.B.:** Note the usage of `has` here. In previous versions (up to 4b) the MQL
data has been modelled in such a way that every object can have it most one
mother. Users of that version of the data base have learned to write

`clause_atom mother = c1.self`

which will lead to an error in the current version.

Text-Fabric implementation
--------------------------

In the Text-Fabric representation of the BHSA dataset, *mother* is an *edge*
feature. The nodes correspond to the objects, and the edges to relationships
between nodes. The edges that belong to the *mother* feature, correspond to the
*mother* relationship.

We count how many mothers nodes can have (it turns to be 0 or 1). We walk
through all nodes (`for c in N()`) and per node we retrieve the mother nodes
(`E.mother.v(c)`), and we store the lengths (if non-zero) in a dictionary
(`mother_len`):

```python
mother_len = {}
for c in N():
    lms = E.mother.f(c) or []
    nms = len(lms)
    if nms: mother_len[c] = nms
```

##### See also #####

*   [`code`](code.md)
