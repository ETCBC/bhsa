#!/usr/bin/env python
# coding: utf-8

# <img align="right" src="images/dans-small.png"/>
# <img align="right" src="images/tf-small.png"/>
# <img align="right" src="images/etcbc.png"/>
# 
# 
# # Paragraphs
# 
# This notebook can read ETCBC `.px` files with information
# about *paragraphs* in it.
# We distill a bunch of extra features at the `clause_atom` level, namely:
# * `pargr`
# * `instruction`
# 
# **NB** This conversion will not work for versions `4` and `4b`.
# 
# ## Discussion
# Somebody should tell in more detail what they are, and document it in the feature documentation.

# In[1]:


import os
import sys
import re
from tf.fabric import Fabric
import utils


# # Pipeline
# See [operation](https://github.com/ETCBC/pipeline/blob/master/README.md#operation)
# for how to run this script in the pipeline.

# In[2]:


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

# In[3]:


repoBase = os.path.expanduser("~/github/etcbc")
thisRepo = "{}/{}".format(repoBase, CORE_NAME)

thisSource = "{}/source/{}".format(thisRepo, VERSION)

thisTemp = "{}/_temp/{}".format(thisRepo, VERSION)
thisTempSource = "{}/source".format(thisTemp)
thisTempTf = "{}/tf".format(thisTemp)

thisTf = "{}/tf/{}".format(thisRepo, VERSION)


# In[4]:


testFeature = "pargr"


# # Test
# 
# Check whether this conversion is needed in the first place.
# Only when run as a script.

# In[5]:


if SCRIPT:
    (good, work) = utils.mustRun(
        None, "{}/.tf/{}.tfx".format(thisTf, testFeature), force=FORCE
    )
    if not good:
        stop(good=False)
    if not work:
        stop(good=True)


# # TF Settings
# 
# * a piece of metadata that will go into these features; the time will be added automatically
# * new text formats for the `otext` feature of TF, based on lexical features.
#   We select the version specific otext material,
#   falling back on a default if nothing appropriate has been specified in oText.
# 
# We do not do this for the older versions `4` and `4b`.

# In[6]:


provenanceMetadata = dict(
    dataset="BHSA",
    datasetName="Biblia Hebraica Stuttgartensia Amstelodamensis",
    version=VERSION,
    author="Eep Talstra Centre for Bible and Computer",
    encoders="Constantijn Sikkel (QDF), and Dirk Roorda (TF)",
    website="https://shebanq.ancient-data.org",
    email="shebanq@ancient-data.org",
)


# In[7]:


utils.caption(4, "Load the existing TF dataset")
TF = Fabric(locations=thisTf, modules=[""])
api = TF.load("label number")
api.makeAvailableIn(globals())


# # Clause atom identifiers in .px
# We must map the way the clause_atoms are identified in the `.px` files
# to nodes in TF.

# In[8]:


utils.caption(0, "\tLabeling clause_atoms")

labelNumberFromNode = {}
nodeFromLabelNumber = {}
for n in N.walk():
    otype = F.otype.v(n)
    if otype == "book":
        curSubtract = 0
        curChapterSeq = 0
    elif otype == "chapter":
        curSubtract += curChapterSeq
        curChapterSeq = 0
    elif otype == "verse":
        curLabel = F.label.v(n)
    elif otype == "clause_atom":
        curChapterSeq += 1
        nm = int(F.number.v(n)) - curSubtract
        nodeFromLabelNumber[(curLabel, nm)] = n
        labelNumberFromNode[n] = (curLabel, nm)

nLabs = len(nodeFromLabelNumber)
nNodes = len(labelNumberFromNode)

if nLabs == nNodes:
    utils.caption(0, "\tOK: clause atoms succesfully labeled")
    utils.caption(0, "\t{} clause atoms".format(nNodes))
else:
    utils.caption(0, "\tWARNING: clause atoms not uniquely labeled")
    utils.caption(0, "\t{} labels =/= {} nodes".format(nLabs, nNodes))


# # Read the PX files

# In[9]:


utils.caption(4, "Parsing paragraph data in PX")

pxFile = "{}/paragraphs.txt".format(thisTempSource)
pxzFile = "{}/paragraphs.txt.bz2".format(thisSource)
utils.caption(0, "bunzipping {} ...".format(pxzFile))
utils.bunzip(pxzFile, pxFile)
pxHandle = open(pxFile)

data = []
notFound = set()

ln = 0
can = 0
featurescan = re.compile(r"0 0 (..) [0-9]+ LineNr\s*([0-9]+).*?Pargr:\s*([0-9.]+)")
curLabel = None

for line in pxHandle:
    ln += 1
    if line.strip()[0] != "*":
        curLabel = line[0:10]
        continue
    can += 1
    features = featurescan.findall(line)
    if len(features) == 0:
        utils.caption(
            0, "\tWarning: line {}: no instruction, LineNr, Pargr found".format(ln)
        )
    elif len(features) > 1:
        utils.caption(
            0,
            "\tWarning: line {}: multiple instruction, LineNr, Pargr found".format(ln),
        )
    else:
        feature = features[0]
        theIns = feature[0]
        theN = feature[1]
        thePara = feature[2]
        labNum = (curLabel, int(theN))
        if labNum not in nodeFromLabelNumber:
            notFound.add(labNum)
            continue
        data.append((nodeFromLabelNumber[labNum], theIns, theN, thePara))
pxHandle.close()
utils.caption(0, "\tRead {} paragraph annotations".format(len(data)))

if notFound:
    utils.caption(
        0,
        "\tWARNING: Could not find {} label/line entries in index: {}".format(
            len(notFound),
            sorted({lab for lab in notFound}),
        ),
    )
else:
    utils.caption(0, "\tOK: All label/line entries found in index")


# In[10]:


if not SCRIPT:
    print("\n".join(repr(d) for d in data[0:10]))


# # Prepare TF features

# In[11]:


utils.caption(0, "Prepare TF paragraph features")

metaData = {
    "": provenanceMetadata,
}
nodeFeatures = {}

newFeatures = """
    pargr
    instruction
""".strip().split()

nodeFeatures = dict(
    instruction=dict(((x[0], x[1]) for x in data)),
    pargr=dict(((x[0], x[3]) for x in data)),
)

for f in nodeFeatures:
    metaData[f] = {}
    metaData[f]["valueType"] = "str"


# In[12]:


changedFeatures = set(nodeFeatures)


# # Write new features
# Transform the collected information in feature-like data-structures, and write it all
# out to `.tf` files.

# In[13]:


utils.caption(4, "write new/changed features to TF ...")
TF = Fabric(locations=thisTempTf, silent=True)
TF.save(nodeFeatures=nodeFeatures, edgeFeatures={}, metaData=metaData)


# # Diffs
# 
# Check differences with previous versions.
# 
# The new dataset has been created in a temporary directory,
# and has not yet been copied to its destination.
# 
# Here is your opportunity to compare the newly created features with the older features.
# You expect some differences in some features.
# 
# We check the differences between the previous version of the features and what has been generated.
# We list features that will be added and deleted and changed.
# For each changed feature we show the first line where the new feature differs from the old one.
# We ignore changes in the metadata, because the timestamp in the metadata will always change.

# In[14]:


utils.checkDiffs(thisTempTf, thisTf, only=changedFeatures)


# # Deliver
# 
# Copy the new TF dataset from the temporary location where it has been created to its final destination.

# In[15]:


utils.deliverFeatures(thisTempTf, thisTf, changedFeatures)


# # Compile TF
# 
# We load the new features, use the new format, check some values

# In[16]:


utils.caption(4, "Load and compile the new TF features")

TF = Fabric(locations=thisTf, modules=[""])
api = TF.load(" ".join(changedFeatures))
api.makeAvailableIn(globals())


# # Examples

# In[17]:


utils.caption(4, "Test: paragraphs of the first verses")


def showParagraphs(verseNode):
    clause_atoms = L.d(verseNode, otype="clause_atom")
    for ca in clause_atoms:
        utils.caption(
            0,
            "\t\t{:<3} {:>12} {}".format(
                F.instruction.v(ca), F.pargr.v(ca), T.text(L.d(ca, otype="word"))
            ),
            continuation=True,
        )


for (i, verseNode) in enumerate(F.otype.s("verse")[0:10]):
    verseLabel = T.sectionFromNode(verseNode)
    verseHeading = "{} {}:{}".format(*verseLabel) if i == 0 or True else verseLabel[2]
    utils.caption(0, "\t{}".format(verseHeading), continuation=True)
    showParagraphs(verseNode)


# In[14]:


if SCRIPT:
    stop(good=True)

