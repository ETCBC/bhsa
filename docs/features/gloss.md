---
title: gloss
---

**gloss**

A short English translation of a single word, disregarding context.

This feature is present on objects of type [*word* and *lex*](otype.md).
(Only in version 2021 it is present on *word* nodes as well).

The *gloss* cannot be used to generate a proper translation.
Many words have multiple meanings and a good translation chooses between them.
The glosses are not guaranteed to mention all possible meanings, and they 
do not contain heuristics which meanings should be selected in which contexts.

The *gloss* is useful for users with limited knowledge of Hebrew to get an impression
of what the text they are reading is about.

This feature has been added to the dataset in a later stage as package called `lexicon`.

You can use it in SHEBANQ queries.

##### Note
> In version 2021 the `gloss` feature is also present on objects of type [*word*](otype.md)

> In pre 2021 versions This feature is not available on *words*, only on nodes of type *lex*.
That makes it difficult to use in MQL queries, because something like this will generally not work

```
select all objects where
[phrase
    [lex gloss ~ 'make'
        [word]
    ]
]
```

> because lexemes may have many occurrences all over the place,
so lexemes tend to be not contained in any other object type.
