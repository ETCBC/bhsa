---
title: number
---

**sequence number**


The sequence number of an object within its context.

This feature is present on objects of type [*sentence(_atom)*, *clause(_atom)*, *phrase(_atom)*, *word*](otype.md).


##### Note
> This feature does not occur on *subphrases*.
However, SHEBANQ shows subphrase numbering in *data view*. 
Subphrases my be nested in intricate ways. 
Shebanq shows for every word the sequence numbers of the subphrases it belongs to.
Subphrases are numbered per containing phrase.

Numbering starts with 1.
The manner of numbering objects differs per object type:

type|numbering
---|---
phrase_atom  |within the book
clause_atom  |within the book
sentence_atom|within the book
word         |within the book
phrase       |within the clause
clause       |within the sentence
sentence     |within the chapter

##### Note
> An explanation of the rationale behind these numbering schemes would be helpful.

As you can see, this feature can be used to find the first or second or third phrase in a clause or clause in a sentence.
However, it is not obvious how to specify the first word in a phrase with the help of the *number* feature.
But if you are in the business of MQL query writing, there is a better way.

##### Hint
> The MQL language contains the keyword `FIRST` by which you can indicate that you mean the first object
in its context. The use of it is nicely demonstrated in this query on 
[SHEBANQ]({{shebanq}}/hebrew/query?id=519) by Reinoud Oosting. The query is also a beautiful
example of establishing whether an anomalous pattern is really exceptional or occurs more often.
For more info about what you can say in MQL, consult the well-written
[reference manual]({{shebanqw}}/Documents/MQL-Query-Guide.pdf)
by the implementor of MQL, Ulrik Petersen.

##### Hint
> You can compute distances between *atoms* by subtracting their *number* features.
