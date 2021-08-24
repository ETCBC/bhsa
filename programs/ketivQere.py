#!/usr/bin/env python
# coding: utf-8

# <img align="right" src="images/dans-small.png"/>
# <img align="right" src="images/tf-small.png"/>
# <img align="right" src="images/etcbc.png"/>
# 
# 
# # Ketiv Qere
# 
# This notebook can read ketiv-qere info in files issued by the ETCBC and transform them
# into new features.
# There will be new features at the word level.
# 
# **NB** This conversion will not work for versions `4` and `4b`.
# 
# ## Discussion
# There are already `qere` and `qere_utf8` features in the MQL of the core data.
# However, there are several problems with those:
# 
# * features that contain the after-word material, `qere_trailer` and `qere_trailer_utf8`
#   are missing;
# * if there is no qere, both features are filled with the empty string.
#   In this way we can make no distinction between a truly empty `qere` and the absence of a `qere`.
# 
# That is why we reconstruct ketiv and qere from special files that are used by the ETCBC.

# In[1]:


import os
import sys
import collections
from tf.fabric import Fabric
from tf.writing.transcription import Transcription
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
thisTempTf = "{}/tf".format(thisTemp)

thisTf = "{}/tf/{}".format(thisRepo, VERSION)


# In[4]:


testFeature = "qere_trailer"


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

# In[7]:


provenanceMetadata = dict(
    dataset="BHSA",
    version=VERSION,
    datasetName="Biblia Hebraica Stuttgartensia Amstelodamensis",
    author="Eep Talstra Centre for Bible and Computer",
    encoders="Constantijn Sikkel (QDF), and Dirk Roorda (TF)",
    website="https://shebanq.ancient-data.org",
    email="shebanq@ancient-data.org",
)

oText = {
    "_temp": """
@fmt:text-orig-full={qere_utf8/g_word_utf8}{qere_trailer_utf8/trailer_utf8}
@fmt:text-orig-full-ketiv={g_word_utf8}{trailer_utf8}
@fmt:text-trans-full={qere/g_word}{qere_trailer/trailer}
@fmt:text-trans-full-ketiv={g_word}{trailer}""",
    "2021": """
@fmt:text-orig-full={qere_utf8/g_word_utf8}{qere_trailer_utf8/trailer_utf8}
@fmt:text-orig-full-ketiv={g_word_utf8}{trailer_utf8}
@fmt:text-trans-full={qere/g_word}{qere_trailer/trailer}
@fmt:text-trans-full-ketiv={g_word}{trailer}""",
    "2017": """
@fmt:text-orig-full={qere_utf8/g_word_utf8}{qere_trailer_utf8/trailer_utf8}
@fmt:text-orig-full-ketiv={g_word_utf8}{trailer_utf8}
@fmt:text-trans-full={qere/g_word}{qere_trailer/trailer}
@fmt:text-trans-full-ketiv={g_word}{trailer}""",
    "2016": """
@fmt:text-orig-full={qere_utf8/g_word_utf8}{qere_trailer_utf8/trailer_utf8}
@fmt:text-orig-full-ketiv={g_word_utf8}{trailer_utf8}
@fmt:text-trans-full={qere/g_word}{qere_trailer/trailer}
@fmt:text-trans-full-ketiv={g_word}{trailer}""",
    "c": """
@fmt:text-orig-full={qere_utf8/g_word_utf8}{qere_trailer_utf8/trailer_utf8}
@fmt:text-orig-full-ketiv={g_word_utf8}{trailer_utf8}
@fmt:text-trans-full={qere/g_word}{qere_trailer/trailer}
@fmt:text-trans-full-ketiv={g_word}{trailer}""",
}

thisOtext = oText.get(VERSION, "")

if thisOtext == "":
    utils.caption(0, "No additional text formats provided")
    otextInfo = {}
else:
    utils.caption(0, "New text formats")
    otextInfo = dict(
        line[1:].split("=", 1) for line in thisOtext.strip("\n").split("\n")
    )
    for x in sorted(otextInfo.items()):
        utils.caption(0, '{:<30} = "{}"'.format(*x))


# In[8]:


utils.caption(4, "Load the existing TF dataset")
TF = Fabric(locations=thisTf, modules=[""])
api = TF.load("label g_word g_cons trailer_utf8")
api.makeAvailableIn(globals())


# # Verse labels
# The ketiv-qere files deal with different verse labels.
# We make a mapping between verse labels and nodes.

# In[9]:


utils.caption(0, "Mapping between verse labels and verse nodes")
nodeFromLabel = {}
for vs in F.otype.s("verse"):
    lab = F.label.v(vs)
    nodeFromLabel[lab] = vs
utils.caption(0, "{} verses".format(len(nodeFromLabel)))


# # Read the Ketiv-Qere file

# In[10]:


utils.caption(4, "Parsing Ketiv-Qere data")

verseInfo = collections.defaultdict(lambda: [])
notFound = set()
missing = collections.defaultdict(lambda: [])
missed = collections.defaultdict(lambda: [])

error_limit = 10

kqFile = "{}/ketivqere.txt".format(thisSource)
kqHandle = open(kqFile)

ln = 0
can = 0
cur_label = None
for line in kqHandle:
    ln += 1
    can += 1
    vlab = line[0:10]
    fields = line.rstrip("\n")[10:].split()
    (ketiv, qere) = fields[0:2]
    (qtrim, qtrailer) = Transcription.suffix_and_finales(qere)
    vnode = nodeFromLabel.get(vlab, None)
    if vnode is None:
        notFound.add(vlab)
        continue
    verseInfo[vnode].append((ketiv, qtrim, qtrailer))
kqHandle.close()
utils.caption(0, "\tRead {} ketiv-qere annotations".format(ln))


# In[11]:


data = []

for vnode in verseInfo:
    wlookup = collections.defaultdict(lambda: [])
    wvisited = collections.defaultdict(lambda: -1)
    wnodes = L.d(vnode, otype="word")
    for w in wnodes:
        gw = F.g_word.v(w)
        if "*" in gw:
            gw = F.g_cons.v(w)
            if gw == "":
                gw = "."
            if F.trailer_utf8.v(w) == "":
                gw += "-"
            wlookup[gw].append(w)
    for (ketiv, qere, qtrailer) in verseInfo[vnode]:
        wvisited[ketiv] += 1
        windex = wvisited[ketiv]
        ws = wlookup.get(ketiv, None)
        if ws is None or windex > len(ws) - 1:
            missing[vnode].append((windex, ketiv, qere))
            continue
        w = ws[windex]
        qereU = Transcription.to_hebrew(qere)
        qtrailerU = Transcription.to_hebrew(qtrailer)
        data.append(
            (
                w,
                ketiv,
                qere,
                qtrailer.replace("\n", ""),
                qereU,
                qtrailerU.replace("\n", ""),
            )
        )
    for ketiv in wlookup:
        if ketiv not in wvisited or len(wlookup[ketiv]) - 1 > wvisited[ketiv]:
            missed[vnode].append(
                (len(wlookup[ketiv]) - (wvisited.get(ketiv, -1) + 1), ketiv)
            )
utils.caption(0, "\tParsed {} ketiv-qere annotations".format(len(data)))


# In[12]:


if not SCRIPT:
    print("\n".join(repr(d) for d in data[0:10]))


# In[13]:


if notFound:
    utils.caption(
        0,
        "\tWARNING: Could not find {} verses: {}".format(
            len(notFound), sorted(notFound)
        ),
    )
else:
    utils.caption(0, "\tAll verses entries found in index")
if missing:
    utils.caption(
        0,
        "\tWARNING: Could not locate ketivs in the text: {} verses".format(
            len(missing)
        ),
    )
    e = 0
    for vnode in sorted(missing):
        if e > error_limit:
            break
        vlab = F.label.v(vnode)
        for (windex, ketiv, qere) in missing[vnode]:
            e += 1
            if e > error_limit:
                break
            utils.caption(
                0,
                "\t\tNOT IN TEXT: {:<10} {:<20} #{} {}".format(
                    vlab, ketiv, windex, qere
                ),
            )
else:
    utils.caption(0, "\tAll ketivs found in the text")
if missed:
    utils.caption(
        0, "\tCould not lookup qeres in the data: {} verses".format(len(missed))
    )
    e = 0
    for vnode in sorted(missed):
        if e > error_limit:
            break
        vlab = F.label.v(vnode)
        for (windex, ketiv) in missed[vnode]:
            e += 1
            if e > error_limit:
                break
            utils.caption(
                0, "\t\tNOT IN DATA: {:<10} {:<20} #{}".format(vlab, ketiv, windex)
            )
else:
    utils.caption(0, "\tAll ketivs found in the data")


# # Prepare TF features

# In[14]:


utils.caption(0, "Prepare TF ketiv qere features")

nodeFeatures = {}

newFeatures = """
    qere
    qere_trailer
    qere_utf8
    qere_trailer_utf8
""".strip().split()

nodeFeatures = dict(
    qere=dict(((x[0], x[2]) for x in data)),
    qere_trailer=dict(((x[0], x[3]) for x in data)),
    qere_utf8=dict(((x[0], x[4]) for x in data)),
    qere_trailer_utf8=dict(((x[0], x[5]) for x in data)),
)


# We update the `otext` feature with new/changed formats

# In[15]:


utils.caption(0, "Update the otext feature")

metaData = {
    "": provenanceMetadata,
}

metaData["otext"] = dict()
metaData["otext"].update(T.config)
metaData["otext"].update(otextInfo)

for f in nodeFeatures:
    metaData[f] = {}
    metaData[f]["valueType"] = "str"


# In[16]:


changedDataFeatures = set(nodeFeatures)
changedFeatures = changedDataFeatures | {"otext"}


# # Write new features
# Transform the collected information in feature-like datastructures, and write it all
# out to `.tf` files.

# In[17]:


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

# In[18]:


utils.checkDiffs(thisTempTf, thisTf, only=changedFeatures)


# # Deliver
# 
# Copy the new TF dataset from the temporary location where it has been created to its final destination.

# In[19]:


utils.deliverFeatures(thisTempTf, thisTf, changedFeatures)


# # Compile TF
# 
# We load the new features, use the new format, check some values

# In[20]:


utils.caption(4, "Load and compile the new TF features")

TF = Fabric(locations=thisTf, modules=[""])
api = TF.load(
    "g_word_utf8 g_word trailer_utf8 trailer {}".format(" ".join(changedDataFeatures))
)
api.makeAvailableIn(globals())


# # Examples

# In[21]:


utils.caption(4, "Basic tests")


def showKq(w):
    hw = F.g_word_utf8.v(w)
    tw = F.g_word.v(w)
    ht = F.trailer_utf8.v(w)
    tt = F.trailer.v(w)

    qhw = F.qere_utf8.v(w)
    qtw = F.qere.v(w)
    qht = F.qere_trailer_utf8.v(w)
    qtt = F.qere_trailer.v(w)

    utils.caption(0, "{:<20} {}".format("hebrew", hw + ht))
    utils.caption(0, "{:<20} {}".format("hebrew qere", qhw + qht))
    utils.caption(0, "{:<20} {}".format("transcription", tw + tt))
    utils.caption(0, "{:<20} {}".format("transcription qere", qtw + qtt))


utils.caption(
    0,
    "{:<30}: {}".format(
        "absence of qere",
        " ".join(
            "NA" if F.qere.v(w) is None else F.qere.v(w) for w in (range(24700, 24710))
        ),
    ),
)
utils.caption(
    0,
    "{:<30}: {}".format(
        "presence of qere trailer",
        " ".join(
            "NA" if F.qere_trailer.v(w) is None else F.qere_trailer.v(w)
            for w in (range(30190, 30195))
        ),
    ),
)

showNode = L.u(122073, otype="verse")[0]
showVerse = T.sectionFromNode(showNode)

utils.caption(4, "{} {}:{} in all formats".format(*showVerse))
for fmt in T.formats:
    utils.caption(
        0, "{:<30} {}".format(fmt, T.text(L.d(showNode, otype="word"), fmt=fmt))
    )


# In[14]:


if SCRIPT:
    stop(good=True)

