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

# # Word sets by accents
#
# We make some classes of words, defined by the accents they contain, and save them as sets, to be used in queries.

import re

from tf.app import use
from tf.lib import writeSets

A = use("bhsa:clone", hoist=globals())

# We define the accents and create a regular expression out of them.

A_ACCENTS = set("04 24 33 63 70 71 72 73 74 93 94".split())

A_PAT = "|".join(A_ACCENTS)
A_RE = re.compile(f"(?:{A_PAT})")
A_RE

# We make two sets of words: words that contain one or more accents in `A_ACCENTS` and words that don't.
#
# The first set we call `word_a` and the other set `word_non_a`.
#
# We go through all words of the whole corpus.

# +
wordA = set()
wordNonA = set()

A.indent(reset=True)
A.info("Classifying words")

for w in F.otype.s("word"):
    translit = F.g_word.v(w)
    if A_RE.search(translit):
        wordA.add(w)
    else:
        wordNonA.add(w)

A.info(f"word_a has {len(wordA):>6} members")
A.info(f"word_non_a has {len(wordNonA):>6} members")
# -

# Collect the sets in a dictionary that assigns names to them:

accents = dict(
    word_a=wordA,
    word_non_a=wordNonA,
)

# Test the set in a query:

query = """
book book=Genesis
  word_a
    g_cons~^(?![KL]$)
    trailer~[^&]
"""
results = A.search(query, sets=accents)
A.table(results, end=5)
A.table(results, end=5, fmt="text-trans-full")

query = """
book book=Genesis
  word_non_a
    g_cons~^(?![KL]$)
    trailer~[^&]
"""
results = A.search(query, sets=accents)
A.table(results, end=5)
A.table(results, end=5, fmt="text-trans-full")

# Now save the sets as a TF file in your Downloads folder (if you want it in an other place,
# tweak the variable `SET_DIR` below.
#
# We use the TF helper function
# [`writeSets`](https://annotation.github.io/text-fabric/tf/lib.html#tf.lib.writeSets)
# to do the work.

# +
SET_DIR = "~/Downloads"

writeSets(accents, f"{SET_DIR}/accents")
# -

# Check:

# !ls -l ~/Downloads/accents

# Now you can use this set in the text-fabric browser by saying:
#
# ```sh
# text-fabric bhsa --sets=~/Downloads/accents
# ```

# ![tfbrowser](accentsScreenshot.png)
