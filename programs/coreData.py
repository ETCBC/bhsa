#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# <img align="right" src="images/dans-small.png"/>
# <img align="right" src="images/tf-small.png"/>
# <img align="right" src="images/etcbc.png"/>
# 
# 
# ![mql](images/emdros.png)
# 
# # TF from MQL
# 
# This notebook can read an
# [MQL](https://emdros.org/mql.html)
# dump of a version of the [BHSA](https://github.com/ETCBC/bhsa) Hebrew Text Database
# and transform it in a Text-Fabric
# [Text-Fabric](https://github.com/Dans-labs/text-fabric)
# resource.
# 
# ## Discussion
# 
# The principled way of going about such a conversion is to import the MQL source into
# an [Emdros](https://emdros.org) database, and use it to retrieve objects and features from there.
# 
# Because the syntax of an MQL file leaves some freedom, it is error prone to do a text-to-text conversion from
# MQL to something else.
# 
# Yet this is what we do, the error-prone thing. We then avoid installing and configuring and managing Emdros, MYSQL/SQLite3.
# Aside the upfront work to get this going, the going after that would also be much slower.
# 
# So here you are, a smallish script to do an awful lot of work, mostly correct, if careful used.
# 
# # Caveat
# 
# This notebook makes use of a new feature of text-fabric, first present in 2.3.12.
# Make sure to upgrade first.
# 
# ```sudo -H pip3 install --upgrade text-fabric
# ```

# In[19]:


import os
import sys
from shutil import rmtree
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
    RENAME = (
        ("g_suffix", "trailer"),
        ("g_suffix_utf8", "trailer_utf8"),
    )


# In[3]:


def stop(good=False):
    if SCRIPT:
        sys.exit(0 if good else 1)


# # Setting up the context: source file and target directories
# 
# The conversion is executed in an environment of directories, so that sources, temp files and
# results are in convenient places and do not have to be shifted around.

# In[4]:


repoBase = os.path.expanduser("~/github/etcbc")
thisRepo = "{}/{}".format(repoBase, CORE_NAME)


# In[5]:


thisSource = "{}/source/{}".format(thisRepo, VERSION)
mqlzFile = "{}/{}.mql.bz2".format(thisSource, CORE_NAME)


# In[6]:


thisTemp = "{}/_temp/{}".format(thisRepo, VERSION)
thisTempSource = "{}/source".format(thisTemp)
mqlFile = "{}/{}.mql".format(thisTempSource, CORE_NAME)
thisTempTf = "{}/tf".format(thisTemp)


# In[7]:


thisTf = "{}/tf/{}".format(thisRepo, VERSION)


# # Test
# 
# Check whether this conversion is needed in the first place.
# Only when run as a script.

# In[8]:


if SCRIPT:
    testFile = "{}/.tf/otype.tfx".format(thisTf)
    (good, work) = utils.mustRun(
        mqlzFile, "{}/.tf/otype.tfx".format(thisTf), force=FORCE
    )
    if not good:
        stop(good=False)
    if not work:
        stop(good=True)


# # TF Settings
# 
# We add some custom information here.
# 
# * the MQL object type that corresponds to the Text-Fabric slot type, typically `word`;
# * a piece of metadata that will go into every feature; the time will be added automatically
# * suitable text formats for the `otext` feature of TF.
# 
# The oText feature is very sensitive to what is available in the source MQL.
# It needs to be configured here.
# We save the configs we need per source and version.
# And we define a stripped down default version to start with.

# In[9]:


slotType = "word"


# In[10]:


featureMetaData = dict(
    dataset="BHSA",
    version=VERSION,
    datasetName="Biblia Hebraica Stuttgartensia Amstelodamensis",
    author="Eep Talstra Centre for Bible and Computer",
    encoders="Constantijn Sikkel (QDF), Ulrik Petersen (MQL) and Dirk Roorda (TF)",
    website="https://shebanq.ancient-data.org",
    email="shebanq@ancient-data.org",
)


# In[11]:


oText = {
    "": {
        "": """
@sectionFeatures=book,chapter,verse
@sectionTypes=book,chapter,verse
@fmt:text-orig-full={g_word_utf8}{g_suffix_utf8}
""",
    },
    "_temp": """
@fmt:lex-orig-full={g_lex_utf8} 
@fmt:lex-orig-plain={lex_utf8} 
@fmt:lex-trans-full={g_lex} 
@fmt:lex-trans-plain={lex} 
@fmt:text-orig-full={g_word_utf8}{trailer_utf8}
@fmt:text-orig-plain={g_cons_utf8}{trailer_utf8}
@fmt:text-trans-full={g_word}{trailer}
@fmt:text-trans-plain={g_cons}{trailer}
@sectionFeatures=book,chapter,verse
@sectionTypes=book,chapter,verse
""",  # noqa W291
    "2021": """
@fmt:lex-orig-full={g_lex_utf8} 
@fmt:lex-orig-plain={lex_utf8} 
@fmt:lex-trans-full={g_lex} 
@fmt:lex-trans-plain={lex} 
@fmt:text-orig-full={g_word_utf8}{trailer_utf8}
@fmt:text-orig-plain={g_cons_utf8}{trailer_utf8}
@fmt:text-trans-full={g_word}{trailer}
@fmt:text-trans-plain={g_cons}{trailer}
@sectionFeatures=book,chapter,verse
@sectionTypes=book,chapter,verse
""",  # noqa W291
    "2017": """
@fmt:lex-orig-full={g_lex_utf8} 
@fmt:lex-orig-plain={lex_utf8} 
@fmt:lex-trans-full={g_lex} 
@fmt:lex-trans-plain={lex} 
@fmt:text-orig-full={g_word_utf8}{trailer_utf8}
@fmt:text-orig-plain={g_cons_utf8}{trailer_utf8}
@fmt:text-trans-full={g_word}{trailer}
@fmt:text-trans-plain={g_cons}{trailer}
@sectionFeatures=book,chapter,verse
@sectionTypes=book,chapter,verse
""",  # noqa W291
    "2016": """
@fmt:lex-orig-full={g_lex_utf8} 
@fmt:lex-orig-plain={lex_utf8} 
@fmt:lex-trans-full={g_lex} 
@fmt:lex-trans-plain={lex} 
@fmt:text-orig-full={g_word_utf8}{trailer_utf8}
@fmt:text-orig-plain={g_cons_utf8}{trailer_utf8}
@fmt:text-trans-full={g_word}{trailer}
@fmt:text-trans-plain={g_cons}{trailer}
@sectionFeatures=book,chapter,verse
@sectionTypes=book,chapter,verse
""",  # noqa W291
    "4b": """
@fmt:lex-orig-full={g_lex_utf8} 
@fmt:lex-orig-plain={lex_utf8} 
@fmt:lex-trans-full={g_lex} 
@fmt:lex-trans-plain={lex} 
@fmt:text-orig-full={g_word_utf8}{trailer_utf8}
@fmt:text-orig-full-ketiv={g_word_utf8}{trailer_utf8}
@fmt:text-orig-plain={g_cons_utf8}{trailer_utf8}
@fmt:text-trans-full={g_word} 
@fmt:text-trans-full-ketiv={g_word} 
@fmt:text-trans-plain={g_cons} 
@sectionFeatures=book,chapter,verse
@sectionTypes=book,chapter,verse
""",  # noqa W291
    "4": """
@fmt:lex-orig-full={g_lex_utf8} 
@fmt:lex-orig-plain={lex_utf8} 
@fmt:lex-trans-full={g_lex} 
@fmt:lex-trans-plain={lex} 
@fmt:text-orig-full={g_word_utf8}{trailer_utf8}
@fmt:text-orig-full-ketiv={g_word_utf8}{trailer_utf8}
@fmt:text-orig-plain={g_cons_utf8}{trailer_utf8}
@fmt:text-trans-full={g_word} 
@fmt:text-trans-full-ketiv={g_word} 
@fmt:text-trans-plain={g_cons} 
@sectionFeatures=book,chapter,verse
@sectionTypes=book,chapter,verse
""",  # noqa W291
    "3": """
@fmt:lex-orig-full={graphical_lexeme_utf8} 
@fmt:lex-orig-plain={lexeme_utf8} 
@fmt:lex-trans-full={graphical_lexeme} 
@fmt:lex-trans-plain={lexeme} 
@fmt:text-orig-full={text}{suffix}
@fmt:text-orig-plain={surface_consonants_utf8}{suffix}
@fmt:text-trans-full={graphical_word} 
@fmt:text-trans-plain={surface_consonants} 
@sectionFeatures=book,chapter,verse
@sectionTypes=book,chapter,verse
""",  # noqa W291
    "c": """
@fmt:lex-orig-full={g_lex_utf8} 
@fmt:lex-orig-plain={lex_utf8} 
@fmt:lex-trans-full={g_lex} 
@fmt:lex-trans-plain={lex} 
@fmt:text-orig-full={g_word_utf8}{trailer_utf8}
@fmt:text-orig-plain={g_cons_utf8}{trailer_utf8}
@fmt:text-trans-full={g_word}{trailer}
@fmt:text-trans-plain={g_cons}{trailer}
@sectionFeatures=book,chapter,verse
@sectionTypes=book,chapter,verse
""",  # noqa W291
}


# The next function selects the proper otext material, falling back on a default if nothing
# appropriate has been specified in `oText`.

# In[12]:


thisOtext = oText.get(VERSION, oText[""])


# In[13]:


if thisOtext is oText[""]:
    utils.caption(
        0, "WARNING: no otext feature info provided, using a meager default value"
    )
    otextInfo = {}
else:
    utils.caption(0, "INFO: otext feature information found")
    otextInfo = dict(
        line[1:].split("=", 1) for line in thisOtext.strip("\n").split("\n")
    )
    for x in sorted(otextInfo.items()):
        utils.caption(0, '\t{:<20} = "{}"'.format(*x))


# # Overview
# 
# The program has several stages:
# 
# 1. **prepare** the source (utils.bunzip if needed)
# 1. **convert** convert the MQL file into a text-fabric dataset
# 1. **differences** (informational)
# 1. **deliver** the TF data at its destination directory
# 1. **compile** all TF features to binary format

# # Prepare
# 
# Check the source, utils.bunzip it if needed, empty the result directory.

# In[14]:


if not os.path.exists(thisTempSource):
    os.makedirs(thisTempSource)


# In[15]:


utils.caption(0, "bunzipping {} ...".format(mqlzFile))
utils.bunzip(mqlzFile, mqlFile)
utils.caption(0, "Done")


# In[16]:


if os.path.exists(thisTempTf):
    rmtree(thisTempTf)
os.makedirs(thisTempTf)


# # MQL to Text-Fabric
# Transform the collected information in feature-like data-structures, and write it all
# out to `.tf` files.

# In[17]:


TF = Fabric(locations=thisTempTf, silent=True)
TF.importMQL(mqlFile, slotType=slotType, otext=otextInfo, meta=featureMetaData)


# # Rename features
# We rename the features mentioned in the RENAME dictionary.

# In[18]:


if RENAME is None:
    utils.caption(4, "Rename features: nothing to do")
else:
    utils.caption(4, "Renaming {} features in {}".format(len(RENAME), thisTempTf))
    for (srcFeature, dstFeature) in RENAME:
        srcPath = "{}/{}.tf".format(thisTempTf, srcFeature)
        dstPath = "{}/{}.tf".format(thisTempTf, dstFeature)
        if os.path.exists(srcPath):
            os.rename(srcPath, dstPath)
            utils.caption(0, "\trenamed {} to {}".format(srcFeature, dstFeature))
        else:
            utils.caption(0, "\tsource feature {} does not exist.".format(srcFeature))
            utils.caption(
                0, "\tdestination feature {} will not be created.".format(dstFeature)
            )


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

# In[19]:


utils.checkDiffs(thisTempTf, thisTf)


# # Deliver
# 
# Copy the new TF dataset from the temporary location where it has been created to its final destination.

# In[20]:


utils.deliverDataset(thisTempTf, thisTf)


# # Compile TF
# 
# Just to see whether everything loads and the pre-computing of extra information works out.
# Moreover, if you want to work with these features, then the pre-computing has already been done, and everything is quicker in subsequent runs.
# 
# We issue load statement to trigger the pre-computing of extra data.
# Note that all features specified text formats in the `otext` config feature,
# will be loaded, as well as the features for sections.
# 
# At that point we have access to the full list of features.
# We grab them and are going to load them all!

# In[14]:


utils.caption(4, "Load and compile standard TF features")
TF = Fabric(locations=thisTf, modules=[""])
api = TF.load("")


# In[15]:


utils.caption(4, "Load and compile all other TF features")
allFeatures = TF.explore(silent=False, show=True)
loadableFeatures = allFeatures["nodes"] + allFeatures["edges"]
api = TF.load(loadableFeatures)
api.makeAvailableIn(globals())


# # Examples

# In[17]:


utils.caption(4, "Basic test")
utils.caption(4, "First verse in all formats")
for fmt in T.formats:
    utils.caption(0, "{}".format(fmt), continuation=True)
    utils.caption(0, "\t{}".format(T.text(range(1, 12), fmt=fmt)), continuation=True)


# In[18]:


if SCRIPT:
    stop(good=True)


# In[16]:


f = "subphrase_type"
print("`" + "` `".join(sorted(str(x[0]) for x in Fs(f).freqList())) + "`")


# In[ ]:




