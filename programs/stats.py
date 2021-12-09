#!/usr/bin/env python
# coding: utf-8

# <img align="right" src="images/dans-small.png"/>
# <img align="right" src="images/tf-small.png"/>
# <img align="right" src="images/etcbc.png"/>
# 
# 
# #  Statistics
# 
# This notebook adds statistical features to a
# [BHSA](https://github.com/ETCBC/bhsa) dataset in
# [text-Fabric](https://github.com/Dans-labs/text-fabric)
# format.
# 
# ## Discussion
# 
# We add the features
# `freq_occ freq_lex rank_occ rank_lex`.
# 
# We assume that the dataset has these features present:
# 
# * LANG_FEATURE (typically `languageISO`) for determining if the word is Hebrew or Aramaic
# * OCC_FEATURE (typically `g_cons`) to get the word string in consonantal transcription
# * LEX_FEATURE (typically `lex`) to get the lexical identifier in consonantal transcription
# 
# This program works for all datasets and versions that have these features with the
# intended meanings. The exact names of these features can be passed as parameters.
# Note that the old version `3` uses very different names for many features.
# 
# #### Languages
# We will not identify lexemes and word occurrences across language.
# So if two occurrences or lexemes exhibit the same string, but they are categorized as belonging
# to different languages, they will not be identified.
# 
# #### Occurrences
# We group occurrences by their consonantal transcriptions.
# So if two occurrences differ only in pointing, we count them as two occurrences of the same value.
# 
# #### Lexemes
# Lexemes are identified by the `lex` feature within a biblical language.
# We will not identify lexemes across language.

# In[9]:


import os
import sys
import collections
import yaml
import utils
from tf.fabric import Fabric
from tf.core.helpers import formatMeta


# # Pipeline
# See [operation](https://github.com/ETCBC/pipeline/blob/master/README.md#operation)
# for how to run this script in the pipeline.

# In[2]:


if "SCRIPT" not in locals():
    SCRIPT = False
    FORCE = True
    CORE_NAME = "bhsa"
    VERSION = "2021"
    LANG_FEATURE = "languageISO"
    OCC_FEATURE = "g_cons"
    LEX_FEATURE = "lex"


def stop(good=False):
    if SCRIPT:
        sys.exit(0 if good else 1)


# # Setting up the context: source file and target directories
# 
# The conversion is executed in an environment of directories, so that sources, temp files and
# results are in convenient places and do not have to be shifted around.

# In[3]:


repoBase = os.path.expanduser("~/github/etcbc")
thisRepo = "{}/{}".format(repoBase, CORE_NAME)

thisTemp = "{}/_temp/{}".format(thisRepo, VERSION)
thisTempTf = "{}/tf".format(thisTemp)

thisTf = "{}/tf/{}".format(thisRepo, VERSION)


# In[4]:


newFeaturesStr = """
    freq_occ
    freq_lex
    rank_occ
    rank_lex
"""
newFeatures = newFeaturesStr.strip().split()


# # Test
# 
# Check whether this conversion is needed in the first place.
# Only when run as a script.

# In[5]:


if SCRIPT:
    (good, work) = utils.mustRun(
        None, "{}/.tf/{}.tfx".format(thisTf, newFeatures[0]), force=FORCE
    )
    if not good:
        stop(good=False)
    if not work:
        stop(good=True)


# # Collect
# 
# We collect the statistics.

# In[6]:


utils.caption(4, "Loading relevant features")

TF = Fabric(locations=thisTf, modules=[""])
api = TF.load("{} {} {}".format(LANG_FEATURE, LEX_FEATURE, OCC_FEATURE))
api.makeAvailableIn(globals())

hasLex = "lex" in set(F.otype.all)


# In[7]:


utils.caption(0, "Counting occurrences")
wstats = {
    "freqs": {
        "lex": collections.defaultdict(lambda: collections.Counter()),
        "occ": collections.defaultdict(lambda: collections.Counter()),
    },
    "ranks": {
        "lex": collections.defaultdict(lambda: {}),
        "occ": collections.defaultdict(lambda: {}),
    },
}
langs = set()

for w in F.otype.s("word"):
    occ = Fs(OCC_FEATURE).v(w)
    lex = Fs(LEX_FEATURE).v(w)
    lan = Fs(LANG_FEATURE).v(w)
    wstats["freqs"]["lex"][lan][lex] += 1
    wstats["freqs"]["occ"][lan][occ] += 1
    langs.add(lan)
for lan in langs:
    for tp in ["lex", "occ"]:
        rank = -1
        prev_n = -1
        amount = 1
        for (x, n) in sorted(
            wstats["freqs"][tp][lan].items(), key=lambda y: (-y[1], y[0])
        ):
            if n == prev_n:
                amount += 1
            else:
                rank += amount
                amount = 1
            prev_n = n
            wstats["ranks"][tp][lan][x] = rank


# In[15]:


utils.caption(0, "Making statistical features")

genericMetaPath = f"{thisRepo}/yaml/generic.yaml"
statsMetaPath = f"{thisRepo}/yaml/stats.yaml"

with open(genericMetaPath) as fh:
    genericMeta = yaml.load(fh, Loader=yaml.FullLoader)
    genericMeta["version"] = VERSION
with open(statsMetaPath) as fh:
    statsMeta = formatMeta(yaml.load(fh, Loader=yaml.FullLoader))

metaData = {"": genericMeta}

nodeFeatures = {}
edgeFeatures = {}

for f in newFeatures:
    nodeFeatures[f] = {}
    metaData[f] = statsMeta[f]
    metaData[f]["valueType"] = "int"
    metaData[f]["provenance"] = "computed on the basis of the ETCBC core set of features"

for w in F.otype.s("word"):
    lan = Fs(LANG_FEATURE).v(w)
    occ = Fs(OCC_FEATURE).v(w)
    lex = Fs(LEX_FEATURE).v(w)
    nodeFeatures["freq_occ"][w] = str(wstats["freqs"]["occ"][lan][occ])
    nodeFeatures["rank_occ"][w] = str(wstats["ranks"]["occ"][lan][occ])
    nodeFeatures["freq_lex"][w] = str(wstats["freqs"]["lex"][lan][lex])
    nodeFeatures["rank_lex"][w] = str(wstats["ranks"]["lex"][lan][lex])

if hasLex:
    for lx in F.otype.s("lex"):
        firstOcc = L.d(lx, otype="word")[0]
        nodeFeatures["freq_lex"][lx] = nodeFeatures["freq_lex"][firstOcc]
        nodeFeatures["rank_lex"][lx] = nodeFeatures["rank_lex"][firstOcc]


# In[16]:


utils.caption(4, "Write statistical features as TF")
TF = Fabric(locations=thisTempTf, silent=True)
TF.save(nodeFeatures=nodeFeatures, edgeFeatures=edgeFeatures, metaData=metaData)


# # Diffs
# 
# Check differences with previous versions.

# In[17]:


utils.checkDiffs(thisTempTf, thisTf, only=set(newFeatures))


# # Deliver
# 
# Copy the new TF features from the temporary location where they have been created to their final destination.

# In[18]:


utils.deliverFeatures(thisTempTf, thisTf, newFeatures)


# # Compile TF

# In[19]:


utils.caption(4, "Load and compile the new TF features")

TF = Fabric(locations=thisTf, modules=[""])
api = TF.load("{} {}".format(LEX_FEATURE, newFeaturesStr))
api.makeAvailableIn(globals())


# # Examples

# In[20]:


utils.caption(4, "Basic test")

mostFrequent = set()

topX = 10

lexIndex = {}

utils.caption(0, "Top {} freqent lexemes (computed on otype=word)".format(topX))
for w in sorted(F.otype.s("word"), key=lambda w: -F.freq_lex.v(w)):
    lex = Fs(LEX_FEATURE).v(w)
    mostFrequent.add(lex)
    lexIndex[lex] = w
    if len(mostFrequent) == topX:
        break

mostFrequentWord = sorted((-F.freq_lex.v(lexIndex[lex]), lex) for lex in mostFrequent)
for (freq, lex) in mostFrequentWord:
    utils.caption(0, "{:<10} {:>6}x".format(lex, -freq))

if hasLex:
    utils.caption(4, "Top {} freqent lexemes (computed on otype=lex)".format(topX))
    mostFrequentLex = sorted(
        (-F.freq_lex.v(lx), F.lex.v(lx)) for lx in F.otype.s("lex")
    )[0:10]
    for (freq, lex) in mostFrequentLex:
        utils.caption(0, "{:<10} {:>6}x".format(lex, -freq))

    if mostFrequentWord != mostFrequentLex:
        utils.caption(
            0, "\tWARNING: Mismatch in lexeme frequencies computed by lex vs by word"
        )
    else:
        utils.caption(0, "\tINFO: Same lexeme frequencies computed by lex vs by word")
utils.caption(0, "Done")


# In[14]:


if SCRIPT:
    stop(good=True)

