#!/usr/bin/env python
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc" style="margin-top: 1em;"><ul class="toc-item"><li><span><a href="#Discussion" data-toc-modified-id="Discussion-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Discussion</a></span></li></ul></div>

# <img align="right" src="images/dans-small.png"/>
# <img align="right" src="images/tf-small.png"/>
# <img align="right" src="images/etcbc.png"/>
# 
# 
# # Booknames (multilingual)
# 
# This notebook adds multilingual book names to a
# [BHSA](https://github.com/ETCBC/bhsa) dataset in
# [text-Fabric](https://github.com/Dans-labs/text-fabric)
# format.
# 
# ## Discussion
# 
# We add the features
# `book@`*iso*
# where *iso* is a
# [two letter ISO-639](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)
# language code of a modern language.
# We use a source file `blang.py` that contains the names of the books of the bible
# in modern languages (around 20, most big languages are covered).
# This data has been gleaned mostly from Wikipedia.
# 
# We assume that the dataset has the `book` feature present, holding *Latin* book names.
# 
# This program works for all datasets and versions that have this feature with the
# intended meaning.

# In[3]:


import os
import sys
import utils
import yaml
from tf.fabric import Fabric
from blang import bookLangs, bookNames


# # Pipeline
# See [operation](https://github.com/ETCBC/pipeline/blob/master/README.md#operation)
# for how to run this script in the pipeline.

# In[4]:


if "SCRIPT" not in locals():
    SCRIPT = False
    FORCE = True
    CORE_NAME = "bhsa"
    VERSION = "2021"


def stop(good=False):
    if SCRIPT:
        sys.exit(0 if good else 1)


# # Setting up the context: source file and target directories
# 
# The conversion is executed in an environment of directories, so that sources, temp files and
# results are in convenient places and do not have to be shifted around.

# In[5]:


repoBase = os.path.expanduser("~/github/etcbc")
thisRepo = "{}/{}".format(repoBase, CORE_NAME)

thisTemp = "{}/_temp/{}".format(thisRepo, VERSION)
thisTempTf = "{}/tf".format(thisTemp)

thisTf = "{}/tf/{}".format(thisRepo, VERSION)


# # Collect
# 
# We collect the book names.

# In[8]:


utils.caption(4, "Book names")

genericMetaPath = f"{thisRepo}/yaml/generic.yaml"
with open(genericMetaPath) as fh:
    genericMeta = yaml.load(fh, Loader=yaml.FullLoader)
    genericMeta["version"] = VERSION

metaData = {"": genericMeta}

for (langCode, (langEnglish, langName)) in bookLangs.items():
    metaData["book@{}".format(langCode)] = dict(
        valueType="str",
        language=langName,
        languageCode=langCode,
        languageEnglish=langEnglish,
        provenance="book names from wikipedia and other sources",
        encoders="Dirk Roorda (TF)",
        description=f"✅ book name in {langEnglish} ({langName})",
    )

newFeatures = sorted(m for m in metaData if m != "")
newFeaturesStr = " ".join(newFeatures)

utils.caption(0, "{} languages ...".format(len(newFeatures)))


# # Test
# 
# Check whether this conversion is needed in the first place.
# Only when run as a script.

# In[10]:


if SCRIPT:
    (good, work) = utils.mustRun(
        None, "{}/.tf/{}.tfx".format(thisTf, newFeatures[0]), force=FORCE
    )
    if not good:
        stop(good=False)
    if not work:
        stop(good=True)


# # Load existing data

# In[11]:


utils.caption(4, "Loading relevant features")

TF = Fabric(locations=thisTf, modules=[""])
api = TF.load("book")
api.makeAvailableIn(globals())

nodeFeatures = {}
nodeFeatures["book@la"] = {}

bookNodes = []
for b in F.otype.s("book"):
    bookNodes.append(b)
    nodeFeatures["book@la"][b] = F.book.v(b)

for (langCode, langBookNames) in bookNames.items():
    nodeFeatures["book@{}".format(langCode)] = dict(zip(bookNodes, langBookNames))
utils.caption(0, "{} book name features created".format(len(nodeFeatures)))


# # Write new features

# In[12]:


utils.caption(4, "Write book name features as TF")
TF = Fabric(locations=thisTempTf, silent=True)
TF.save(nodeFeatures=nodeFeatures, edgeFeatures={}, metaData=metaData)


# # Diffs
# 
# Check differences with previous versions.

# In[13]:


utils.checkDiffs(thisTempTf, thisTf, only=set(newFeatures))


# # Deliver
# 
# Copy the new Text-Fabric features from the temporary location where they have been created to their final destination.

# In[14]:


utils.deliverFeatures(thisTempTf, thisTf, newFeatures)


# # Compile TF

# In[15]:


utils.caption(4, "Load and compile the new TF features")

TF = Fabric(locations=thisTf, modules=[""])
api = TF.load("")
api.makeAvailableIn(globals())


# # Examples

# In[16]:


utils.caption(4, "Genesis in all languages")
genesisNode = F.otype.s("book")[0]

for (lang, langInfo) in sorted(T.languages.items()):
    language = langInfo["language"]
    langEng = langInfo["languageEnglish"]
    book = T.sectionFromNode(genesisNode, lang=lang)[0]
    utils.caption(
        0,
        "{:<2} = {:<20} Genesis is {:<20} in {:<20}".format(
            lang, langEng, book, language
        ),
    )

utils.caption(0, "Done")


# In[ ]:




