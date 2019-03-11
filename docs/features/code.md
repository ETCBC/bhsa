---
title: code
---

**clause atom relation**


This feature is present on objects of type [*clause_atom*](otype).

##### Note
> This is a complex definition.
The present text is derived from Constantijn's description of the
QUEST II Database format.
The definition needs review.

See the hint at the end to see how you could use this feature.

Clause atom relation is denoted by a code of 1, 2, or 3 digits.

---|---
`0`           | [No relation](#no-relation)
`10` - `16`   | [Relative clause atoms](#relative-clause-atoms)
`50` – `74`   | [Infinitive construct clause atoms](#infinitive-construct-clause-atoms)
`100` – `167` | [Asyndetic clause atoms](#asyndetic-clause-atoms)
`200` - `201` | [Parallel clause atoms](#parallel-clause-atoms)
`220` - `223` | [Defective clause atoms](#defective-clause-atoms)
`300` - `367` | [Conjunctive adverbs](#conjunctive-adverbs)
`400` - `487` | [Coordinate clause atoms](#coordinate-clause-atoms)
`500` - `567` | [Postulational clause atoms](#postulational-clause-atoms)
`600` - `667` | [Conditional clause atoms](#conditional-clause-atoms)
`700` - `767` | [Temporal clause atoms](#temporal-clause-atoms)
`800` - `867` | [Final clause atoms](#final-clause-atoms)
`900` - `967` | [Causal clause atoms](#causal-clause-atoms)
`999`         | [Direct speech](#direct-speech)

These classes are of a distributional, not functional, nature.
They group lexemes which are hypothesised to share one or more functional aspects into tentative sets,
so that the resulting clause atom relations codes constitute a useful collection of data for further research.

See for example
Gino Kalkman's
[analysis of syntax in the poetry of the Psalms]({{shebanqw}}/Tools-Overview)

##### Note
> The notions distributional and functional should be explained somewhere, 
on a separate page.
The meaning of this sentence is difficult to follow.
Which are the tentative sets of lexemes, which are the resulting clause atom relations?
What is the useful collection of data?
An example of research should be given or referred to.
The reference to Gino's work could be more pin-pointed.

# No relation

**`0`**

The value `0` and a [dist](dist) of 0 clause atoms to its mother mark a clause atom as the root of the tree of clause atom relations.

##### Note
> Is the value of `0` sufficient?
Can it occur that the value is `0` and the distance not?
If not, the distance of 0 is not an extra condition, but an additional phenomenon.
The definition should then say something like: (and in that case the [dist](dist) is also `0`).
In order to understand this all, there should be an explanation of the intended model
of clause atom relations. Is it a tree? How is it built up? Maybe a separate page.

##### See also
* [tab](tab).

Examples please.

# Relative clause atoms

**`10` .. `16`**

Clause atoms whose opening phrase (first phrase?)
has [typ](typ) `CP` (conjunctive phrase) and
[function](function) `Rela` (relative).
The second digit denotes the tense of the verbal predicate of the daughter clause:

##### Tenses

---|---|---
`0`| none
`1`| imperfect
`2`| perfect
`3`| imperative
`4`| infinitive construct
`5`| infinitive absolute
`6`| participle            | (active and passive)
`7`| wayyiqtol
`8`| weyiqtol              | !

##### Note
> The ! appears where the QUEST documentation has a cross mark. 
I do not know why these values have been marked.

#  Infinitive construct clause atoms

**`50`– `74`**
Clause atoms of which the verbal predicate is an infinitive construct.
If you subtract 50, the remaining number denotes the class of the preposition used in the construction:

---|---|---
`0` | none
`1` |`>XR/`
`2` |`>L`
`3` |`>YL/`         | !
`4` |`>T`
`5` |`B`, `BMW`
`6` |`BJN/`         | !
`7` |`BL<DJ`        | !
`8` |*not used*
`9` |`B<D/`         | !
`10`|`ZWLH/`        | !
`11`|`J<N/`
`12`|`K, KMW`
`13`|*not used*
`14`|`L, LMW`
`15`|`LM<N`
`16`|*not used*
`17`|`MN`
`18`|*not used*
`19`|*not used*
`20`|`<D`
`21`|`<L`
`22`|`<M`
`23`|*not used*
`24`|`TXT/`

##### Note
> The ! appears where the QUEST documentation has a cross mark. 
I do not know why these values have been marked.

# Asyndetic clause atoms

**`100` – `167`**

Construction without a conjunction.
The second and third digit denote the tense of the verbal predicate of the daughter and
mother clause, respectively. See the [tense table](#tenses).

##### See also

* [mother](mother).

# Parallel clause atoms

**`200` - `201`**

Two clause atoms are parallel if they concur in subject presence
and have equivalent phrases up to the predicate,
provided that the daughter is not subordinated.

##### See also
* [mother](mother).

If either predicate is absent,
the clause atoms must be of the same clause atom type ([typ](typ)).


---|---
`200` | Identical clause atom opening.
`201` | Identical clause atom opening when disregarding the coordinating conjunction(s).

# Defective clause atoms

**`220` - `223`**

A clause atom is defective if there is another clause atom which contains
the predicate (or the main part) of the clause.

---|---
`220`|No verbal predicate in mother or daughter
`221`|Unclassified clause atom relation
`222`|Verbal predicate in daughter clause atom
`223`|Verbal predicate in mother clause atom.

##### See also

* [mother](mother).

# Conjunctive adverbs

**`300` - `367`**

Asyndetic construction, but with a conjunctive adverb.
The second and third digit denote the tense of the verbal predicate of the daughter and
mother clause, respectively. See the [tense table](#tenses).

##### See also

* [mother](mother).

# Coordinate clause atoms

**`400` - `487`**

Construction with a conjunction from class 400, the *coordinating* conjunctions:
The second and third digit denote the tense of the verbal predicate of the daughter and
mother clause, respectively. See the [tense table](#tenses).

##### See also

* [mother](mother).

---|---|---
`400`|coordinating | `>W`, `W`
`500`|postulational| `>CR`, `DJ`, `H`, `ZW`, `KJ`, `C`
`600`|conditional  | `>LW`, `>M`, `HN`, `LHN=`, `LW`, `LWL>`
`800`|final        | `PN`

The conjunction class is determined by the conjunction opening conjunction phrase.

##### Note
> Too terse:
"the conjunction opening conjunction phrase".
Expand or give an example.

code 800 also occurs in the table of
[Temporal clause atoms](#temporal-clause-atoms)

# Postulational clause atoms

**`500` - `567`**

Construction with a conjunction from class 500, the *postulational* conjunctions:
The second and third digit denote the tense of the verbal predicate of the daughter and
mother clause, respectively. See the [tense table](#tenses).

##### See also

* [mother](mother).

# Conditional clause atoms

**`600` - `667`**

Construction with a conjunction from class 600, the *conditional* conjunctions:
The second and third digit denote the tense of the verbal predicate of the daughter and
mother clause, respectively. See the [tense table](#tenses).

##### See also

* [mother](mother).

# Temporal clause atoms

**`700` - `767`**

Construction with a conjunction from class 700, the *conditional* conjunctions:
The second and third digit denote the tense of the verbal predicate of the daughter and
mother clause, respectively. See the [tense table](#tenses).

##### See also

* [mother](mother).

---|---
`700`| `>XR/`, `>L`, `B`, `BMW`, `VRM/`, `K`, `KMW`, `L`, `LMW`, `<D`
`800`| `BLT/`, `ZWLH/`, `LM<N`, `MN`
`900`| `J<N/`, `<L`, `<QB/`

This preposition class is determined by the preposition that heads the clause opening conjunction phrase.

##### Note
> Too terse:
"that heads the clause opening conjunction phrase".
Expand or give an example.

code `800` also occurs in the table of
[Conjunction classes of clause atom opening](#coordinate-clause-atoms)

# Final clause atoms

**`800` - `867`**

Construction with a conjunction from class 800, the *final* conjunctions:
The second and third digit denote the tense of the verbal predicate of the daughter and
mother clause, respectively. See the [tense table](#tenses).

##### See also

* [mother](mother).

# Causal clause atoms

**`900` - `967`**

Construction with a conjunction from class 900, the *causal* conjunctions:
The second and third digit denote the tense of the verbal predicate of the daughter and
mother clause, respectively. See the [tense table](#tenses).

##### See also

* [mother](mother).

# Direct speech

**`999`**

The clause atom in question starts a direct speech section.

A section of direct speech is usually introduced by a clause atom
with a verbum dicendi. In this case, the direct speech section
depends on the introductory clause atom in terms of clause atom
relations. The daughter clause atom (the main clause atom of the
direct speech section) carries the [instruction](instruction)
'q' and has a
relation 999 with its mother, the introductory clause atom.

But there are other cases, in which the the direct speech section
is not introduced at all (Jes 14:16) or in which it is declared by
an embedded clause atom (Mal 3:17). In such cases, the main clause
atom of the direct speech section still carries the [instruction](instruction)
'q', but no longer has a relation 999 with its mother. If there is
a declarative clause atom, it will have a relation 999 with _its_
mother, which is not necessarily the main clause atom of the direct
speech section, as an example like Mal 3:17 shows.

In all cases, the [instruction](instruction) 'q' means the start of a clause atom
hierarchy of direct speech. In view of the above, however, we can
no longer maintain a direct coupling between 'q' and relation 999.
We propose to extend the interpretation of relation 999 as follows.
The meaning of relation 999 is that of a declaration of direct
speech. Either before the facts, if the daughter starts the direct
speech, or after the facts, if the daughter has the verbum dicendi.
In case of the latter, the daughter carries the [instruction](instruction) '#' for
a new embedded paragraph, but pops the Q from the Text Type.

##### See also

* [mother](mother).

##### Note
> Is the "daughter" clause the object in question?

What if a direct speech clause also fits the pattern of one of the other cases?

##### Hint
> Here is a public MQL query by Martijn Naaijer that detects chunks of direct speech.
It uses the combined information carried by the `code` feature and the 
[txt](txt) feature. View the query on
[SHEBANQ]({{shebanq}}/hebrew/query?id=518).
