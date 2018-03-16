---
title: BHSA API
feat: false
---

About
-----

The module [bhsa.py](https://github.com/ETCBC/bhsa/blob/master/programs/bhsa.py)
contains a number of handy functions on top of Text-Fabric and especially
[Search](https://github.com/Dans-labs/text-fabric/wiki/Api#search).

Set up
------

In this repository, *bhsa.py* resides in the *programs* directory. In order to
import it into a Jupyter notebook in a completely different directory, we have
to point Python's module path to it:

```python
LOC = ('~/github', 'etcbc/bhsa', 'verseDisplay')
sys.path.append(os.path.expanduser(f'{LOC[0]}/{LOC[1]}/programs'))
from bhsa import Bhsa
B = Bhsa(*LOC)
B.api.makeAvailableIn(globals())
```

It will start Text-Fabric and load a bunch of features for you.

If you need more features, say `vs` and `vt`, you can follow up by

```python
B.load('vs vt')
```

Usage
-----

Now you can call the methods of *bhsa*, as follows. One of the methods is
`pretty(node)`. To call it, say

```python
B.pretty(node)
```

API
---

### load ###

Loads more features.

**Takes**

*   `features` a space separated string of feature names;

**Result**

*   the features are loaded and usable with `F`.

**Implementation details**

Existing features remain in place, the existing TF-api remains undisturbed.

**N.B.:** use this instead of `TF.load()`.

### pretty ###

Displays the material that corresponds to a node in a rich way.

**Takes**

*   `n` a node of arbitrary type;
*   `withNodes=True` whether node numbers should be displayed;

**Returns**

*   the material of the node in rich HTML.

**Details**

If the node is a book or chapter, only the book name (with chapter number) are
displayed. It will be displayed as a link to the same book/chapter in SHEBANQ.

If the node is a verse, the whole verse will be displayed, with some features on
the words.

If the node is a sentence, clause, phrase, etc, then exactly that constituent
will be dislayed.

### prettyTuple ###

Displays the material that corresponds to a node in a rich way.

**Takes**

*   `ns` an iterable (list, tuple, set, etc) of arbitrary nodes;
*   `seqNumber` an arbitrary number which will be displayed in a heading above the
    display; this prepares the way for displaying query results, which are a
    sequence of tuples of nodes;
*   `withNodes=True` whether node numbers should be displayed;

**Returns**

*   the material of the tuple in rich HTML.

**Details**

We examine all nodes in the tuple. The ones of a higher level than verses will
become just links to SHEBANQ. For all other nodes, we collect all verses in
which they occur. We show all verses, with the occurrences of the nodes in the
tuple highlighted.

### search ###

Searches in the same way as `T.search()`.

**Takes**

*   `query` a TF search string;

**Returns**

*   the results of the query as list; hence you can expect the number of results
    with `len()`.

### show ###

Displays a list of query results.

**Takes**

*   `results` a list of tuples of nodes, e.g. obtained by `B.search()`;
*   `start=0` a starting point in the result list;
*   `end=len(results)` an end point in the result list;
*   `withNodes=True` whether node numbers should be displayed;

**Returns**

* a rich display of all results from `start` to `end` but never more than 100 at a time.

**Details**

Every result will be preceded by a heading indicating the sequence number of the
result and summary of the tuple of nodes, with or without the node numbers.
