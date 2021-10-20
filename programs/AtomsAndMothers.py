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

# <img align="right" src="images/dans-small.png"/>
# <img align="right" src="images/tf-small.png"/>
# <img align="right" src="images/etcbc.png"/>
#
#
# # Atoms and Mothers
#
# One of the trickiest bits in the
# [ETCBC database of the Hebrew Bible](https://etcbc.github.io/bhsa/features/hebrew/2016/0_home.html)
# are the
# [*atoms*](https://etcbc.github.io/bhsa/features/hebrew/2016/otype.html#linguistic-types)
# within sentences, clauses and phrases, and the
# [*mother*](https://etcbc.github.io/bhsa/features/hebrew/2016/mother.html)
# relationship between objects.
#
# Yet a lot of the coding effort of the ETCBC is located in precisely these concepts, especially in the treatment of *clause*-atoms.
# For example, there is a specific feature
# [code](https://etcbc.github.io/bhsa/features/hebrew/2016/code.html)
# defined on clause atoms that provides a refined categorization of clauses.
#
# In this notebook, we will explore and highlight what you can do with mothers and clause_atoms.
#
# # Acknowledgment
#
# This notebook owes a lot to the eager questions of Joshua Grauman and the prompt answers by Hendrik-Jan Bosman, spiced with additional insights of Cody Kingham and David van Acker.

import collections
from tf.fabric import Fabric

locations = "~/github/etcbc"
BHSA = "bhsa/tf/2017"
TF = Fabric(locations=locations, modules=[BHSA])

api = TF.load(
    """
    typ function
    mother
"""
)
api.makeAvailableIn(globals())

# # clause and clause_atom
#
# The ETCBC does not work with *embedded* clauses. In the clause
#
# `we'll see whether this works out later`
#
# there is an inner clause `whether this works out`, and an outer clause `we'll see ... later`.
#
# In many types of linguistic analysis, the inner clause is part of the outer clause, in the role of
# direct object. The word `works` belongs both to the inner and outer clause.
#
# Not so in the ETCBC analysis of things.
# The inner clause *interrupts* the outer clause, and the outer clause has a *gap*.
# The word `works` belongs to the inner clause only.
#
# Because of the gap, the outer clause splits into two segments, one before the gap, and one after the gap.
# These parts are called the *clause_atoms*.
#
# The clause_atom before the gap is rather complete, it has a subject and a predicate.
# The clause_atom after the gap is, well, defective.
#
# ## Explore
#
# Let us see some clauses that consist of multiple clause atoms.

# +
results = list(
    S.search(
        """
clause
  clause_atom
  < clause_atom
"""
    )
)

mClauses = N.sortNodes(set(x[0] for x in results))
TF.info("{} multiple atom clauses".format(len(mClauses)))
# -

for r in results[0:5]:
    print(S.glean(r))

# Now count the how many clauses have how many atoms.

caCount = collections.Counter()
for c in mClauses:
    caCount[len(L.d(c, "clause_atom"))] += 1
for (nca, nc) in sorted(caCount.items(), key=lambda x: (-x[1], x[0])):
    print("{:>2} atoms: {:>5} clauses".format(nca, nc))

# The next thing is: we want to see every multi-atom clause, and for each atom at which slot it starts and end, and whether its
# [clause type](https://etcbc.github.io/bhsa/features/hebrew/2016/typ.html)
# is defective or not.

# +
chunks = []
for c in mClauses:
    cas = L.d(c, "clause_atom")
    cwords = L.d(c, otype="word")
    rep = ["{}-{}".format(cwords[0], cwords[-1])]
    for ca in cas:
        defc = F.typ.v(ca) == "Defc"
        slots = L.d(ca, otype="word")
        bs = slots[0]
        es = slots[-1]
        rep.append("\t{}-{}-{}".format(bs, "D" if defc else "-", es))
    chunks.append(rep)

for ch in chunks[0:10]:
    print("\n".join(ch))
# -

# Is it the case that every clause splits into exactly one non-defective atom and the rest defective?
# Lets count the profiles of clauses. A profile is a sequence of `-` and `D` characters, corresponding to the
# defectiveness of its successive clause_atoms.

profiles = collections.Counter()
for c in F.otype.s("clause"):
    cas = L.d(c, "clause_atom")
    profile = "".join(
        "D" if F.typ.v(ca) == "Defc" else "-" for ca in L.d(c, otype="clause_atom")
    )
    profiles[profile] += 1
TF.info("{} profiles".format(len(profiles)))
for (profile, n) in sorted(profiles.items()):
    print("{:<6} : {:>5}x".format(profile, n))

# This gives a pretty good picture of the construction of clauses out of their atoms.
# Note that we have inspected all clauses, including the single atoms clauses, and note that those are never
# defective.
#
# Is it true then, that the defective clause atoms do not contain a predicate, and the others do.
# We'll check. A predicate is a phrase with a `function` that is one of a few values.
# We count the clause_atoms with and without a predicate, separately for defective and complete ones.
#
# We expect the classes `D-` (defective, no predicate) and `-P` (complete, with predicate) to be represented,
# whilst the classes `DP` (defective with predicate) and `--` (complete, without predicate) should be empty.

# +
predicates = {"Pred", "PreO", "PreS", "PrcS", "PtcO", "PreC"}


def classify(clauseSet, predLabels):
    defPred = collections.Counter()

    for c in clauseSet:
        defc = F.typ.v(c) == "Defc"
        pred = any(F.function.v(p) in predLabels for p in L.d(c, otype="phrase"))
        defPred[("D" if defc else "-") + ("P" if pred else "-")] += 1

    for x in sorted(defPred.items()):
        print("{} x {:>5}".format(*x))


classify(F.otype.s("clause_atom"), predicates)
# -

# It is nearly true that defective atoms do not have a predicate, because the class `DP` is very small.
# But there is a fair amount of `--` clause_atoms.
#
# We can determine which function labels of phrases do not occur in defective clause atoms.

allFunctions = {F.function.v(p) for p in F.otype.s("phrase")}
sorted(allFunctions)

defcFunctions = collections.Counter()
completeFunctions = collections.Counter()
for c in F.otype.s("clause_atom"):
    dest = defcFunctions if F.typ.v(c) == "Defc" else completeFunctions
    for p in L.d(c, otype="phrase"):
        dest[F.function.v(p)] += 1

defcFunctions

completeFunctions

# So, there are a few defective clause_atoms with a predicative complement, and there are quite a few
# complete clauses lacking anything that looks like a predicate.
#
# If we restrict ourselves to multiple atom clauses, the picture is this.

mClauseAtoms = set()
for c in mClauses:
    for ca in L.d(c, otype="clause_atom"):
        mClauseAtoms.add(ca)
classify(mClauseAtoms, predicates)

# ## Conclusion (Atoms)
# Defective clause atoms are always part of clauses with multiple atoms.
# Such clauses have exactly one non defective clause_atoms.
# Defective clause_atoms do not have predicates, but may have a predicative complement or adjunct.
# Most non-defective clause atoms have a predicate, but their is a fair collection without.

# # Mothers
#
# The `mother` relationship between nodes tells something about linguistic dependency.
# We first investigate the extent of the `mother` relationship in terms of node types, and then we concentrate on the mothers and daughters of clause atoms.

motherInventory = collections.Counter()
for n in N():
    for m in E.mother.f(n):
        motherInventory[(F.otype.v(n), F.otype.v(m))] += 1

for ((fr, to), n) in sorted(motherInventory.items()):
    print("{:>12} => {:<12} x {:>6}".format(fr, to, n))

# Clearly, the `mother` relationship does a big thing with clause atoms, more than with any other object type.
# Also, mothers and daughters of clause atoms are always clause atoms themselves.
#
# There is also a rich web between subphrases and words.
# We collect the subphrases that have a subphrase as mother and separately those that have a word as mother.
# The `S.search()` command can be put to handy use. It gives an example how to use *edge* features, such as `mother`, in search templates.
#
# However, I forgot the syntax, so first this:

print(S.relationLegend)

resultsW = sorted(
    S.search(
        """
verse
  subphrase
  -mother> word
"""
    )
)

len(resultsW)

# Let peek at the first 10.

for r in resultsW[0:10]:
    print(S.glean(r))


# And now the same for subphrases with subphrase mothers.

# +
def inspectMotherSp():
    results = sorted(
        S.search(
            """
verse
  subphrase
  -mother> subphrase
    """
        )
    )
    print(len(results))
    for r in results[0:10]:
        print(S.glean(r))


inspectMotherSp()
