---
title: label
---

**(half-)verse label**


This feature occurs on objects of type [*verse* and *half-verse*](otype).

# Half-verse

Many verses consist of two parts.
Those parts are called half-verses, and the first one is indicated with *A*, and the second one with *B*.
There are only a few verses with three parts, and the third part is indicated, unsurprisingly, by *C*. 

##### Note
> The half-verse object has no features that specify the verse it occurs in.

When working in Text-Fabric, you can go from verses `v` to half-verses `h` and vice versa by means of

```python
L.d(v, 'half_verse')
```

and

```python
L.u(h, 'verse')
```

respectively.

# Verse

A small string of fixed with with an abbreviation of the book name, the chapter number and the verse number
of the verse in question.

##### Hint
> This feature is a bit tricky to use for searches,
because there are sometimes leading spaces and sometimes not;
sometimes there is a space between book and chapter, and sometimes not.
the abbreviation of the name of the book is not the abbreviation of the latin name of the book.
We recommend to use the *book*, *chapter*, and *verse* features.

If you are in Text-Fabric, use the [`T.sectionFromNode`](/text-data/wiki/Api#sectioning) function.

The main use of this function is in cases where you want to combine data in this set with other files
from the ETCBC.
These files often refer to data by means of these verse labels.
