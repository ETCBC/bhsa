#!/usr/bin/env python
# coding: utf-8

# <img align="right" src="images/dans-small.png"/>
# <img align="right" src="images/tf-small.png"/>
# <img align="right" src="images/etcbc.png"/>
# 
# 
# # Lexicon
# 
# This notebook can read lexicon info in files issued by the ETCBC and transform them
# into new features.
# There will be new features at the word level and a new level will be made: lexeme.
# 
# Most lexical features do not go to the word nodes but to the lexeme nodes.
# 
# **NB** This conversion will not work for versions `4` and `4b`.
# 
# ## Discussion
# There are several issues that we deal with here.
# 
# Language: are an Aramaic lexeme and a Hebrew lexeme with the same value identical?
# In short: no.
# 
# The lexicon is a piece of data not conceptually contained in the text.
# So where do we leave that data?
# 
# The lexicon contains information about lexemes. Some of that information is also present
# on individual occurrences.
# The question arises, should a lexical feature have consistent values across its occurrences.
# 
# And of course: does the lexicon *match* the text?
# Do all lexemes in the text have a lexical entry, and does every lexical entry have actual
# occurrences in the text?
# 
# ### Lexeme language
# Lexemes do not cross languages, so the set of Aramaic and Hebrew lexemes are disjoint.
# Whenever we index lexemes, we have to specify it as a pair of its language and lex values.
# 
# ### Lexeme node type
# The answer where to leave the lexical information in a text-fabric data set is surprisingly simple:
# on nodes of a new type `lex`.
# Nodes of type lex will be connected via the `oslots` feature to all its occurrences, so lexemes *contain* there
# occurrences.
# All features encountered in the lexicon, we will store on these `lex` nodes.
# 
# However, experience has taught us that it is very convenient to duplicate feature values of lexeme nodes to all
# corresponding word nodes.
# This is what we will do.
# 
# ### Lexical consistency
# It is quite possible that some occurrences have got a different value for a lexical feature than its lexeme.
# A trivial case are adjectives, whose lexical gender is `NA`, but whose occurrences usually have a distinct gender.
# 
# Other features really should be fully consistent, for example the *vocalized lexeme*.
# We encounter this feature in the text (`g_voc_lex` and also its Hebrew version `g_voc_lex_utf8`),
# and in the lexicon it is present as feature `vc`.
# In this case we observe a deficiency in the lexicon: `vc` is often absent.
# Apart from that, the textual features `g_voc_lex` and `g_voc_lex_utf8` are fully consistent, so I take their values
# and put them in the lexicon, and I remove the `g_voc_lex` and `g_voc_lex_utf8` from the dataset.
# 
# ## Match between lexicon and text
# We perform quite a number of checks.
# The match should be perfect.
# If not, then quite possible the MQL core data has been exported at an other time the the lexical data.
# 
# ## Various issues
# 1. `lex` contains the lexeme (in transcription) with disambiguation marks (`[/=`) appended.
#    For text transformations we prefer the bare lexeme, and we store that in a new feature `lex0`
# 1. `lex_utf` has frills at the end of many values.
#    They occur where the final consonant as an alternative form. See analysis below.
# 1. `language` has values `Hebrew` and `Aramaic`. We prefer ISO language codes: `hbo` and `arc` instead.
#    By adding `language` for lexeme nodes we already have switched to ISO codes. Here we do the rest.
# 1. the feature lex_utf8 occurs only on word nodes, but is consistent across lexemes. We add it to lexeme nodes
#    as well, together with `lex0`.
# 
# We are going to deal with these issues [later](#Deal-with-various-issues).

# In[1]:


import os
import sys
import re
import yaml
from tf.fabric import Fabric
from tf.core.helpers import formatMeta
import utils


# # Pipeline
# See [operation](https://github.com/ETCBC/pipeline/blob/master/README.md#operation)
# for how to run this script in the pipeline.

# In[2]:


if "SCRIPT" not in locals():
    SCRIPT = False
    FORCE = True
    CORE_NAME = "bhsa"
    EXTRA_OVERLAP = ""
    #    EXTRA_OVERLAP='gloss nametype'
    DO_VOCALIZED_LEXEME = True
    #    DO_VOCALIZED_LEXEME=False
    LEX_FORMATS = "@fmt:lex-trans-plain={lex0} "
    #    LEX_FORMATS='@fmt:lex-trans-plain={lex} '

    VERSION = "2021"


def stop(good=False):
    if SCRIPT:
        sys.exit(0 if good else 1)


# # Analysis of lex_utf8
# 
# Let us focus on a few cases.
# 
# We translate the UTF sequences found in the MQL source into real Unicode characters:

# In[3]:


if not SCRIPT:
    import unicodedata

    uniscan = re.compile(r"(?:\\x..)+")

    def makeuni(match):
        """Make proper unicode of a text that contains byte escape codes such as backslash xb6"""
        byts = eval('"' + match.group(0) + '"')
        return byts.encode("latin1").decode("utf-8")

    def uni(line):
        return uniscan.sub(makeuni, line)

    cases = dict(
        b=r"\xd7\x91",
        rcjt=r"\xd7\xa8\xd7\x90\xd7\xa9\xd7\x81\xd7\x99\xd7\xaa\xd6\x9c",
        rcjt_nme=r"\xd6\x9c",
        lhjm=r"\xd7\x90\xd7\x9c\xd7\x94\xd7\x99\xd7\x9d\xd6\x9c",
        al=r"\xd7\xa2\xd7\x9c",
    )

    for (case, utf8) in sorted(cases.items()):
        uword = uni(utf8)
        uLast = uword[-1]
        uCode = ord(uLast)
        uName = unicodedata.name(uLast)
        print(
            """{:<10}:
        MQL original   = {}
        Unicode        = {}
        Last char id   = {:>4x} {}
        Last char uni  = {}
    """.format(
                case,
                utf8,
                uword,
                uCode,
                uName,
                uLast,
            )
        )


# # Setting up the context: source file and target directories
# 
# The conversion is executed in an environment of directories, so that sources, temp files and
# results are in convenient places and do not have to be shifted around.

# In[4]:


repoBase = os.path.expanduser("~/github/etcbc")
thisRepo = "{}/{}".format(repoBase, CORE_NAME)

thisSource = "{}/source/{}".format(thisRepo, VERSION)

thisTemp = "{}/_temp/{}".format(thisRepo, VERSION)
thisTempSource = "{}/source".format(thisTemp)
thisTempTf = "{}/tf".format(thisTemp)

thisTf = "{}/tf/{}".format(thisRepo, VERSION)


# In[5]:


testFeature = "lex0"


# # Test
# 
# Check whether this conversion is needed in the first place.
# Only when run as a script.

# In[6]:


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


genericMetaPath = f"{thisRepo}/yaml/generic.yaml"
coreMetaPath = f"{thisRepo}/yaml/core.yaml"
lexiconMetaPath = f"{thisRepo}/yaml/lexicon.yaml"

with open(genericMetaPath) as fh:
    genericMeta = yaml.load(fh, Loader=yaml.FullLoader)
    genericMeta["version"] = VERSION
with open(coreMetaPath) as fh:
    coreMeta = formatMeta(yaml.load(fh, Loader=yaml.FullLoader))
with open(lexiconMetaPath) as fh:
    lexiconMeta = formatMeta(yaml.load(fh, Loader=yaml.FullLoader))

metaData = {"": genericMeta}

lexType = "lex"

if LEX_FORMATS == "":
    utils.caption(0, "No additional text formats provided")
    otextInfo = {}
else:
    utils.caption(0, "New text formats")
    otextInfo = dict(
        line[1:].split("=", 1) for line in LEX_FORMATS.strip("\n").split("\n")
    )
    for x in sorted(otextInfo.items()):
        utils.caption(0, '{:<30} = "{}"'.format(*x))


# # Lexicon preparation
# We add lexical data.
# The lexical data will not be added as features of words, but as features of lexemes.
# The lexemes will be added as fresh nodes, of a new type `lex`.

# In[8]:


utils.caption(4, "Load the existing TF dataset")
TF = Fabric(locations=thisTf, modules=[""])
vocLex = " g_voc_lex g_voc_lex_utf8 " if DO_VOCALIZED_LEXEME else ""
api = TF.load(
    "lex lex_utf8 language sp ls gn ps nu st oslots {} {}".format(vocLex, EXTRA_OVERLAP)
)
api.makeAvailableIn(globals())


# # Text pass
# We map the values in the language feature to standardized ISO values: `arc` and `hbo`.
# We run over all word occurrences, grab the language and lexeme identifier, and create for each
# unique pair a new lexeme node.
# 
# We remember the mapping between nodes and lexemes.
# 
# We check whether the word features `lex_utf8` and `g_lex_utf` are consistent between occurrences
# of the same lexeme.
# 
# This stage does not yet involve the lexical files.

# In[9]:


utils.caption(4, "Collect lexemes from the text")

langMap = {
    "hbo": "hbo",
    "Hebrew": "hbo",
    "Aramaic": "arc",
    "arc": "arc",
}
langIMap = {
    "hbo": "Hebrew",
    "Hebrew": "Hebrew",
    "Aramaic": "Aramaic",
    "arc": "Aramaic",
}

doValueCompare = {"sp", "ls", "gn", "ps", "nu", "st"}
doFeatureCheck = {"lex_utf8", "g_lex_utf8"}

lexText = {}

maxNode = F.otype.maxNode
maxSlot = F.otype.maxSlot
slotType = F.otype.slotType

lexNode = maxNode
lexOccs = {}
nodeFromLex = {}
lexFromNode = {}
otypeData = {}
oslotsData = {}

for n in F.otype.s("word"):
    lex = F.lex.v(n)
    lan = langMap[F.language.v(n)]
    lexId = (lan, lex)
    lexOccs.setdefault(lexId, []).append(n)

    for ft in doValueCompare:
        val = Fs(ft).v(n)
        lexText.setdefault(lan, {}).setdefault(lex, {}).setdefault(ft, set()).add(val)

    if lexId not in nodeFromLex:
        lexNode += 1
        nodeFromLex[lexId] = lexNode
        lexFromNode[lexNode] = lexId
        
utils.caption(0, f"Check consistency of {', '.join(doFeatureCheck)}")
inconsistent = {ft: 0 for ft in doFeatureCheck}

for (lexId, ws) in lexOccs.items():
    for ft in doFeatureCheck:
        values = {Fs(ft).v(w) for w in ws}
        if len(values) != 1:
            inconsistent[ft] += 1
for ft in doFeatureCheck:
    nInc = inconsistent[ft]
    utils.caption(0, f"{nInc} inconsistencies in {ft}" if nInc else f"{ft} is consistent over lexeme occurrences")

for n in range(maxNode + 1, lexNode + 1):
    otypeData[n] = "lex"
    oslotsData[n] = lexOccs[lexFromNode[n]]

utils.caption(0, "added {} lexemes".format(len(nodeFromLex)))
utils.caption(0, "maxNode is now {}".format(lexNode))

for lan in sorted(lexText):
    utils.caption(
        0, "language {} has {:>5} lexemes in the text".format(lan, len(lexText[lan]))
    )


# # Lexicon pass
# Here we are going to read the lexicons, one for Aramaic, and one for Hebrew.

# In[10]:


utils.caption(4, "Collect lexeme info from the lexicon")

langs = set(langMap.values())
lexFile = dict((lan, "{}/lexicon_{}.txt".format(thisSource, lan)) for lan in langs)


def readLex(lan):
    lexInfile = open(lexFile[lan], encoding="utf-8")
    errors = []

    lexItems = {}
    ln = 0
    for line in lexInfile:
        ln += 1
        line = line.rstrip()
        line = line.split("#")[0]
        if line == "":
            continue
        (entry, featurestr) = line.split(sep=None, maxsplit=1)
        entry = entry.strip('"')
        if entry in lexItems:
            errors.append("duplicate lexical entry {} in line {}.\n".format(entry, ln))
            continue
        featurestr = featurestr.strip(":")
        featurestr = featurestr.replace("\\:", chr(254))
        featurelst = featurestr.split(":")
        features = {}
        for feature in featurelst:
            comps = feature.split("=", maxsplit=1)
            if len(comps) == 1:
                if feature.strip().isnumeric():
                    comps = ("_n", feature.strip())
                else:
                    errors.append(
                        "feature without value for lexical entry {} in line {}: {}\n".format(
                            entry,
                            ln,
                            feature,
                        )
                    )
                    continue
            (key, value) = comps
            value = value.replace(chr(254), ":")
            if key in features:
                errors.append(
                    "duplicate feature for lexical entry {} in line {}: {}={}\n".format(
                        entry,
                        ln,
                        key,
                        value,
                    )
                )
                continue
            features[key] = value.replace("\\", "/")
        if "sp" in features and features["sp"] == "verb":
            if "gl" in features:
                gloss = features["gl"]
                if gloss.startswith("to "):
                    features["gl"] = gloss[3:]
        lexItems[entry] = features

    lexInfile.close()
    nErrors = len(errors)
    if len(errors):
        utils.caption(
            0,
            "Lexicon [{}]: {} error{}".format(
                lan, nErrors, "" if nErrors == 1 else "s"
            ),
        )
        for error in errors:
            utils.caption(1, error)
    return lexItems


utils.caption(0, "Reading lexicon ...")
lexEntries = dict((lan, readLex(lan)) for lan in sorted(langs))
for lan in sorted(lexEntries):
    utils.caption(0, "Lexicon {} has {:>5} entries".format(lan, len(lexEntries[lan])))
utils.caption(0, "Done")


# # Tests
# 
# ## Matching of text and lexicon
# 
# Let us now check whether all lexemes in the text occur in the lexicon and vice versa.

# In[11]:


utils.caption(4, "Test - Match between text and lexicon")

arcLex = set(lexEntries["arc"])
hboLex = set(lexEntries["hbo"])

utils.caption(0, "{} arc lexemes".format(len(arcLex)))
utils.caption(0, "{} hbo lexemes".format(len(hboLex)))

arcText = set(lexText["arc"])
hboText = set(lexText["hbo"])

hboAndArcText = arcText & hboText
hboAndArcLex = arcLex & hboLex

lexMinText = hboAndArcLex - hboAndArcText
textMinLex = hboAndArcText - hboAndArcLex

utils.caption(
    0,
    "Equal lex values in hbo and arc in the BHSA   text contains {} lexemes".format(
        len(hboAndArcText)
    ),
)
utils.caption(
    0,
    "Equal lex values in hbo and arc in the lexicon     contains {} lexemes".format(
        len(hboAndArcLex)
    ),
)
utils.caption(
    0,
    "Common values in the lexicon but not in the text: {}x: {}".format(
        len(lexMinText), lexMinText
    ),
)
utils.caption(
    0,
    "Common values in the text but not in the lexicon: {}x: {}".format(
        len(textMinLex), textMinLex
    ),
)

arcTextMinLex = arcText - arcLex
arcLexMinText = arcLex - arcText

hboTextMinLex = hboText - hboLex
hboLexMinText = hboLex - hboText

for (myset, mymsg) in (
    (arcTextMinLex, "arc: lexemes in text but not in lexicon"),
    (arcLexMinText, "arc: lexemes in lexicon but not in text"),
    (hboTextMinLex, "hbo: lexemes in text but not in lexicon"),
    (hboLexMinText, "hbo: lexemes in lexicon but not in text"),
):
    utils.caption(
        0,
        "{}: {}x{}".format(
            mymsg,
            len(myset),
            "" if not myset else "\n\t{}".format(", ".join(sorted(myset))),
        ),
    )


# ## Consistency of vocalized lexeme
# 
# The lexicon file provides an attribute `vc` for each lexeme, which is the vocalized lexeme.
# The BHSA core data also has features `g_voc_lex` and `g_voc_lex_utf8` for each occurrence.
# 
# We investigate whether the latter features are *consistent*, i.e. a property of the lexeme and lexeme only.
# If they are somehow dependent on the word occurrence, they are not consistent.
# 
# When they are consistent, we can omit them on the occurrences and use them on the lexemes.
# We'll also check whether the `vc` property found in the lexicon coincides with the `g_voc_lex` on the occurrences.
# 
# Supposing it is all consistent, we will call the new lexeme features `voc_lex` and `voc_lex_utf8`.

# In[12]:


utils.caption(4, "Test - Consistency of vocalized lexeme")

if not DO_VOCALIZED_LEXEME:
    utils.caption(0, "\tSKIPPED in version {}".format(VERSION))
else:
    vocFeatures = dict(voc_lex={}, voc_lex_utf8={})

    exceptions = dict(incons=dict((f, {}) for f in vocFeatures), deviating=dict())

    missing = {}

    def showExceptions(cases):
        nCases = len(cases)
        if nCases == 0:
            utils.caption(0, "\tFully consistent")
        else:
            utils.caption(0, "\t{} inconsistent cases".format(nCases))
            limit = 10
            for (i, (lan, lex)) in enumerate(cases):
                if i == limit:
                    utils.caption(0, "\t\t...and {} more.".format(nCases - limit))
                    break
                utils.caption(
                    0,
                    "\t\t{}-{}: {}".format(
                        lan, lex, ", ".join(sorted(cases[(lan, lex)]))
                    ),
                )

    for w in F.otype.s("word"):
        lan = langMap[F.language.v(w)]
        lex = F.lex.v(w)
        for (f, values) in vocFeatures.items():
            current = values.get((lan, lex), None)
            new = Fs("g_{}".format(f)).v(w)
            if current is None:
                values[(lan, lex)] = new
                if f == "voc_lex":
                    lexical = lexEntries[lan][lex].get("vc", None)
                    if lexical is None:
                        missing[(lan, lex)] = new
                    else:
                        if lexical != new:
                            exceptions["deviating"].setdefault(
                                (lan, lex), {lexical}
                            ).add(new)
            else:
                if current != new:
                    exceptions["incons"][f].setdefault((lan, lex), {current}).add(new)

    nMissing = len(missing)

    utils.caption(0, "lexemes with missing vc property: {}x".format(nMissing))
    for (lan, lex) in sorted(missing)[0:20]:
        utils.caption(
            0,
            "\t{}-{} supplied from occurrence: {}".format(
                lan, lex, vocFeatures["voc_lex"][(lan, lex)]
            ),
        )
    for f in vocFeatures:
        utils.caption(
            0, "Have all occurrences of a lexeme the same {} value?".format(f)
        )
        showExceptions(exceptions["incons"][f])
    utils.caption(
        0,
        "Are the voc_lex values of the lexeme consistent with the vc value of the lexeme?",
    )
    showExceptions(exceptions["deviating"])


# # Prepare TF features
# 
# We now collect the lexical information into the features for nodes of type `lex`.

# In[13]:


utils.caption(4, "Prepare TF lexical features")

nodeFeatures = {}

lexFields = (
    ("rt", "root"),
    ("sp", "sp"),
    ("sm", "nametype"),
    ("ls", "ls"),
    ("gl", "gloss"),
)

overlapFeatures = {"lex", "language", "sp", "ls"} | set(EXTRA_OVERLAP.strip().split())
# these are features that occur both on word- and lex- otypes

extendFeatures = {"root", "nametype", "gloss"}
# these are features coming from the lexicon and not yet present on words
# they will be made present on words

for f in overlapFeatures:
    nodeFeatures[f] = dict((n, Fs(f).v(n)) for n in N.walk() if Fs(f).v(n) is not None)

newFeatures = [f[1] for f in lexFields]

for (lan, lexemes) in lexEntries.items():
    for (lex, lexValues) in lexemes.items():
        lexId = (lan, lex)
        node = nodeFromLex.get(lexId, None)
        if node is None:
            continue
        nodeFeatures.setdefault("lex", {})[node] = lex
        nodeFeatures.setdefault("languageISO", {})[node] = langMap[lan]
        nodeFeatures.setdefault("language", {})[node] = langIMap[lan]
        for (f, newF) in lexFields:
            value = lexValues.get(f, None)
            if value is not None:
                nodeFeatures.setdefault(newF, {})[node] = value
                if newF in extendFeatures:
                    for wordNode in lexOccs[lexId]:
                        nodeFeatures[newF][wordNode] = value
        if DO_VOCALIZED_LEXEME:
            for (f, vocValues) in vocFeatures.items():
                value = vocValues.get((lan, lex), None)
                if value is not None:
                    nodeFeatures.setdefault(f, {})[node] = value
                    for wordNode in lexOccs[lexId]:
                        nodeFeatures[f][wordNode] = value


# ## Deal with various issues
# We address the issues listed under [various issues](#Various-issues) above.

# In[14]:


utils.caption(4, "Various tweaks in features")

nodeFeatures["lex0"] = {}
nodeFeatures["lex_utf8"] = {}
nodeFeatures["languageISO"] = {}

geresh = chr(0x59C)

contractFeatures = dict(lex_utf8=True, lex0=False, languageISO=False)
# these are features that exists already on words, but are not covered by the lexicon
# we have already test their consistency for lexeme nodes.
# We copy their values
# to the relevant lexeme nodes
# lex_utf8 does already exist on word nodes, we can pick it up from F,
# but lex0 must be picked up from nodeFeatures["lex0"]

for n in F.otype.s("word"):
    lex = F.lex.v(n)
    lex_utf8 = F.lex_utf8.v(n)
    if lex_utf8.endswith(geresh):
        lex_utf8 = lex_utf8.rstrip(geresh)
    lan = F.language.v(n)
    nodeFeatures["lex0"][n] = lex.rstrip("/[=")
    nodeFeatures["lex_utf8"][n] = lex_utf8
    nodeFeatures["languageISO"][n] = langMap[lan]
    nodeFeatures["language"][n] = langIMap[lan]
    
for (lexId, lexNode) in nodeFromLex.items():
    wordNodes = lexOccs[lexId]
    wordNode = wordNodes[0]
    for (ft, exists) in contractFeatures.items():
        nodeFeatures[ft][lexNode] = Fs(ft).v(wordNode) if exists else nodeFeatures[ft][wordNode]


# We update the `otype`, `otext` and `oslots` features.

# In[21]:


utils.caption(4, "Update the otype, oslots and otext features")
edgeFeatures = {}

metaData["otext"] = dict()
metaData["otext"].update(T.config)
metaData["otext"].update(otextInfo)
metaData["otype"] = dict(valueType="str")
metaData["oslots"] = dict(valueType="str")

for f in nodeFeatures:
    if f in lexiconMeta:
        metaData[f] = lexiconMeta[f]
    elif f in coreMeta:
        metaData[f] = coreMeta[f]
    else:
        metaData[f] = {}
    metaData[f]["valueType"] = "str"
    metaData[f]["provenance"] = "from additional lexicon file provided by the ETCBC"

nodeFeatures["otype"] = dict((n, F.otype.v(n)) for n in range(1, maxNode + 1))
nodeFeatures["otype"].update(otypeData)
edgeFeatures["oslots"] = dict(
    (n, E.oslots.s(n)) for n in range(maxSlot + 1, maxNode + 1)
)
edgeFeatures["oslots"].update(oslotsData)


# In[22]:


utils.caption(0, "Features that have new or modified data")
for f in sorted(nodeFeatures) + sorted(edgeFeatures):
    utils.caption(0, "\t{}".format(f))

if DO_VOCALIZED_LEXEME:
    testNodes = range(maxNode + 1, maxNode + 10)
    utils.caption(
        0,
        "Check voc_lex_utf8: {}".format(
            " ".join(nodeFeatures["voc_lex_utf8"][n] for n in testNodes)
        ),
    )


# We specify the features to delete and list the new/changed features.

# In[23]:


deleteFeatures = (
    set(
        """
    g_voc_lex
    g_voc_lex_utf8
""".strip().split()
    )
    if DO_VOCALIZED_LEXEME
    else set()
)

if deleteFeatures:
    utils.caption(0, "\tFeatures to remove")
    for f in sorted(deleteFeatures):
        utils.caption(0, "\t{}".format(f))
else:
    utils.caption(0, "\tNo features to remove")


# In[24]:


changedDataFeatures = set(nodeFeatures) | set(edgeFeatures)
changedFeatures = changedDataFeatures | {"otext"}


# # Write new features
# Transform the collected information in feature-like data-structures, and write it all
# out to `.tf` files.

# In[25]:


utils.caption(4, "write new/changed features to TF ...")
TF = Fabric(locations=thisTempTf, silent=True)
TF.save(nodeFeatures=nodeFeatures, edgeFeatures=edgeFeatures, metaData=metaData)


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

# In[26]:


utils.checkDiffs(thisTempTf, thisTf, only=changedFeatures)


# # Deliver
# 
# Copy the new TF dataset from the temporary location where it has been created to its final destination.

# In[27]:


utils.deliverFeatures(
    thisTempTf, thisTf, changedFeatures, deleteFeatures=deleteFeatures
)


# # Compile TF
# 
# We load the new features, use the new format, check some values

# In[28]:


utils.caption(4, "Load and compile the new TF features")

TF = Fabric(locations=thisTf, modules=[""])
api = TF.load(" ".join(changedDataFeatures))
api.makeAvailableIn(globals())


# # Examples

# In[30]:


features = [f[1] for f in lexFields] + (
    ["voc_lex", "voc_lex_utf8"] if DO_VOCALIZED_LEXEME else []
)


def showLex(w):
    info = dict((f, Fs(f).v(w)) for f in features)
    utils.caption(
        0,
        "\t{} - {} - {}x".format(
            F.language.v(w),
            F.lex.v(w),
            len(L.d(w, otype="word")),
        ),
    )
    for f in sorted(info):
        utils.caption(0, "\t\t{:<15} = {}".format(f, info[f]))


fmt = "lex-trans-plain"
utils.caption(
    0,
    "{:<30}: {}".format(
        "new format {} (using lex0)".format(fmt),
        T.text(range(1, 12), fmt=fmt),
    ),
)
utils.caption(
    0,
    "{:<30}: {}".format(
        "lex_utf8 feature",
        " ".join(F.lex_utf8.v(w) for w in range(1, 12)),
    ),
)
utils.caption(
    0,
    "{:<30}: {}".format(
        "language feature",
        " ".join(F.language.v(w) for w in range(1, 12)),
    ),
)
utils.caption(4, "Lexeme info for the first verse")

for w in range(1, 12):
    showLex(L.u(w, otype="lex")[0])


# In[14]:


if SCRIPT:
    stop(good=True)

