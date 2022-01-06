# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Named Entities in the BHSA
#
# For prelimanaries, such as installing Text-Fabric and using it, consult the
# [start tutorial](https://nbviewer.jupyter.org/github/annotation/tutorials/blob/master/bhsa/start.ipynb)
#
# We show how to fetch person/place/people/measure names from the BHSA data

import os
from tf.app import use

A = use("bhsa", hoist=globals())

# If you expand the triangle in front of BHSA above, you see which features have been loaded.
#
# We need [nametype](https://etcbc.github.io/bhsa/features/nametype/) specifically.
# It is a mapping from word numbers to types of proper names.
#
# Here is a frequency distribution of its values:

F.nametype.freqList()

# We query the measure names (`mens`):

# +
query = """
word nametype=mens
"""

results = A.search(query)
# -

A.table(results)

# The frequency list promised 30 results but we see only 20. That is because there are also other things that have a name type: lexemes:

# +
queryL = """
lex nametype=mens
"""

resultsL = A.search(queryL)
# -

A.table(resultsL)

# Let's make a data file of all words that have a name type.
# We'll produce a tab-separated file with a bit of extra information.

# +
query = """
word nametype gloss*
"""

results = A.search(query)
# -

A.table(results, end=10)

A.show(results, start=10000, end=10003)

A.export(results, toFile="namedEntities.tsv")

# !head -n 20 ~/Downloads/namedEntities.tsv

# Note that this file is in UTF16 with a byte order that is chosen such that the file opens without issue in Excel.
#
# If you want to read the file by Python, it works like this:

# +
filePath = os.path.expanduser("~/Downloads/namedEntities.tsv")

i = 0
limit = 20

with open(filePath, encoding="utf16") as fh:
    for line in fh:
        i += 1
        cells = line.rstrip("\n").split("\t")
        print(i, cells)
        if i > limit:
            break
# -

# See also the documentation of the
# [export function](https://annotation.github.io/text-fabric/tf/advanced/display.html#tf.advanced.display.export)

# CC-BY Dirk Roorda
