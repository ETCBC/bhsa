
# coding: utf-8

# <img align="right" src="tf-small.png"/>
# 
# # Lexicon
# 
# This notebook can read lexicon info in files issued by the etcbc and transform them 
# into new features.
# There will be features at the word level and a new level will be made: lexeme.
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
# ### Lexical consistency
# It is quite possible that some occurrences have got a different value for a lexical feature than its lexeme.
# A trivial case are adjectives, whose lexical gender is `NA`, but whose occurrences usually have a distinct gender.
# 
# Other features really should be fully consistent, for example the *vocalized lexeme*.
# We encounter this feature in the text (`g_voc_lex` and also its hebrew version `g_voc_lex_utf8`), 
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
# ## Varia
# 1. `lex` contains the lexeme (in transcription) with disambiguation marks (`[/=`) appended.
#    For text transformations we prefer the bare lexeme
# 1. `lex_utf` has frills at the end of many values. Probably they have arisen by transforming the lexeme plus
#    disambiguation marks into unicode. We overwrite this feature with the transform of the bare lexeme.
# 1. `language` has values `Hebrew` and `Aramaic`. We prefer ISO language codes: `hbo` and `arc` instead.
#    By adding `language` for lexeme nodes we already have switched to ISO codes. Here we do the rest.
# 
# --to do
# 
# otext aanpassen
# 
# otype aanpassen: lex erin
# 
# features g_voc_lex en g_voc_lex_utf8 weghalen
# 
# feature lex0 maken

# In[1]:


import os,sys,re,collections
from tf.fabric import Fabric
from tf.transcription import Transcription
from utils import startNow, tprint, checkDiffs, deliverFeatures


# In[2]:


if 'SCRIPT' not in locals():
    SCRIPT = False
    CORE_NAME = 'bhsa'
    VERSION= 'c'
    CORE_MODULE ='core' 

def stop(good=False):
    if SCRIPT: sys.exit(0 if good else 1)


# # Setting up the context: source file and target directories
# 
# The conversion is executed in an environment of directories, so that sources, temp files and
# results are in convenient places and do not have to be shifted around.

# In[3]:


module = CORE_MODULE
repoBase = os.path.expanduser('~/github/etcbc')
thisRepo = '{}/{}'.format(repoBase, CORE_NAME)

thisSource = '{}/source/{}'.format(thisRepo, VERSION)

thisTemp = '{}/_temp/{}'.format(thisRepo, VERSION)
thisSave = '{}/{}'.format(thisTemp, module)

thisTf = '{}/tf/{}'.format(thisRepo, VERSION)
thisDeliver = '{}/{}'.format(thisTf, module)


# In[4]:


testFeature = 'lex0'


# # Test
# 
# Check whether this conversion is needed in the first place.
# Only when run as a script.

# In[5]:


if SCRIPT:
    (good, work) = MUSTRUN(None, '{}/.tf/{}.tfx'.format(thisDeliver, testFeature))
    if not good: stop(good=False)
    if not work: stop(good=True)


# # TF Settings
# 
# * a piece of metadata that will go into these features; the time will be added automatically
# * new text formats for the `otext` feature of TF, based on lexical features.
# 
# We do not do this for the older versions 4 and 4b.

# In[6]:


provenanceMetadata = dict(
    dataset='BHSA',
    datasetName='Biblia Hebraica Stuttgartensia Amstelodamensis',
    author='Eep Talstra Centre for Bible and Computer',
    encoders='Constantijn Sikkel (QDF), and Dirk Roorda (TF)',
    website='https://shebanq.ancient-data.org',
    email='shebanq@ancient-data.org',
)

lexType = 'lex'

oText = {
    'c': '''
@fmt:lex-trans-plain={lex0} 
''',
}


# The next function selects the proper otext material, falling back on a default if nothing 
# appropriate has been specified in `oText`.

# In[7]:


def getOtext():
    thisOtext = oText.get(VERSION, '')
    otextInfo = dict(line[1:].split('=', 1) for line in thisOtext.strip('\n').split('\n'))

    if thisOtext is '':
        print('No additional text formats provided') 
    else:
        print('New text formats')
    for x in sorted(otextInfo.items()):
        print('{:<20} = "{}"'.format(*x))
    return otextInfo


# # Stage: Lexicon preparation
# We add lexical data.
# The lexical data will not be added as features of words, but as features of lexemes.
# The lexemes will be added as fresh nodes, of a new type `lex`.

# In[8]:


TF = Fabric(locations=thisTf, modules=module)
api = TF.load('lex lex_utf8 language sp ls gn ps nu st g_voc_lex g_voc_lex_utf8 oslots')
F = api.F
Fs = api.Fs
E = api.E
T = api.T
N = api.N


# # Text pass
# We map the values in the language feature to standardized iso values: `arc` and `hbo`.
# We run over all word occurrences, grab the language and lexeme identifier, and create for each
# unique pair a new lexeme node.
# 
# We remember the mapping between nodes and lexemes.
# 
# This stage does not yet involve the lexical files.

# In[9]:


langMap = {
    'hbo': 'hbo',
    'Hebrew': 'hbo',
    'Aramaic': 'arc',
    'arc': 'arc',
}

maxNode = F.otype.maxNode
maxSlot = F.otype.maxSlot
slotType = F.otype.slotType

lexNode = maxNode
lexOccs = {}
nodeFromLex = {}
lexFromNode = {}
otypeData = {}
oslotsData = {}

for n in F.otype.s('word'):
    lex = F.lex.v(n)
    lan = langMap[F.language.v(n)]
    lexId = (lan, lex)
    lexOccs.setdefault(lexId, []).append(n)
    if lexId not in nodeFromLex:
        lexNode += 1
        nodeFromLex[lexId] = lexNode
        lexFromNode[lexNode] = lexId
print('added {} lexemes\nmaxNode is now {}'.format(len(nodeFromLex), lexNode))

for n in range(maxNode+1, lexNode+1):
    otypeData[n] = 'lex'
    oslotsData[n] = lexOccs[lexFromNode[n]]


# # Lexicon pass
# Here we are going to read the lexicons, one for Aramaic, and one for Hebrew.

# In[10]:


langs = set(langMap.values())
lexFile = dict((lan, '{}/lexicon_{}.txt'.format(thisSource, lan)) for lan in langs)

def readLex(lan):
    lexInfile = open(lexFile[lan], encoding='utf-8')
    errors = []

    lexItems = {}
    ln = 0
    for line in lexInfile:
        ln += 1
        line = line.rstrip()
        line = line.split('#')[0]
        if line == '': continue
        (entry, featurestr) = line.split(sep=None, maxsplit=1)
        entry = entry.strip('"')
        if entry in lexItems:
            errors.append('duplicate lexical entry {} in line {}.\n'.format(entry, ln))
            continue
        featurestr = featurestr.strip(':')
        featurestr = featurestr.replace('\\:', chr(254))
        featurelst = featurestr.split(':')
        features = {}
        for feature in featurelst:
            comps = feature.split('=', maxsplit=1)
            if len(comps) == 1:
                if feature.strip().isnumeric():
                    comps = ('_n', feature.strip())
                else:
                    errors.append('feature without value for lexical entry {} in line {}: {}\n'.format(
                            entry, ln, feature,
                    ))
                    continue
            (key, value) = comps
            value = value.replace(chr(254), ':')
            if key in features:
                errors.append('duplicate feature for lexical entry {} in line {}: {}={}\n'.format(
                        entry, ln, key, value,
                ))
                continue
            features[key] = value.replace('\\', '/')
        if 'sp' in features and features['sp'] == 'verb':
            if 'gl' in features:
                gloss = features['gl']
                if gloss.startswith('to '):
                    features['gl'] = gloss[3:]
        lexItems[entry] = features
        
    lexInfile.close()
    nErrors = len(errors)
    if len(errors):
        print('Lexicon [{}]: {} error{}'.format(nErrors, '' if nErrors == 1 else 's'))
    return lexItems

print("Reading lexicon ...")
lexEntries = dict((lan, readLex(lan)) for lan in sorted(langs))
for lan in sorted(lexEntries):
    print('Lexicon {} has {:>5} entries'.format(lan, len(lexEntries[lan])))
print("Done")


# # Tests
# 
# ## Matching of text and lexicon
# 
# We inspect all word occurrences of the BHSA core database, inspect their language and lexeme values, and construct sets of lexemes that belong to each of the two languages, ``hbo`` and ``arc``.

# In[11]:


lexText = {}
doValueCompare = {'sp', 'ls', 'gn', 'ps', 'nu', 'st'}
nodeLex = {}

print('Reading the BHSA core data ...')
textLangs = set()
for n in F.otype.s('word'):
    lan = langMap[F.language.v(n)]
    textLangs.add(lan)
    lex = F.lex.v(n)
    nodeLex[n] = (lan,lex)
    for ft in doValueCompare:
        val = Fs(ft).v(n)        
        lexText.setdefault(lan, {}).setdefault(lex, {}).setdefault(ft, set()).add(val)

print("Done")
for lan in sorted(lexText):
    print('Language {} has {:>5} lexemes in the text'.format(lan, len(lexText[lan])))


# Let us now check whether all lexemes in the text occur in the lexicon and vice versa.

# In[12]:


arcLex = set(lexEntries['arc'])
hboLex = set(lexEntries['hbo'])

print('{} arc lexemes'.format(len(arcLex)))
print('{} hbo lexemes'.format(len(hboLex)))

arcText = set(lexText['arc'])
hboText = set(lexText['hbo'])

hboAndArcText = arcText & hboText
hboAndArcLex = arcLex & hboLex

lexMinText = hboAndArcLex - hboAndArcText
textMinLex = hboAndArcText - hboAndArcLex

print('Equal lex values in hbo and arc in the BHSA   text contains {} lexemes'.format(len(hboAndArcText)))
print('Equal lex values in hbo and arc in the lexicon     contains {} lexemes'.format(len(hboAndArcLex)))
print("Common values in the lexicon but not in the text: {}x: {}".format(
    len(lexMinText), lexMinText)
)
print("Common values in the text but not in the lexicon: {}x: {}".format(
    len(textMinLex), textMinLex)
)

arcTextMinLex = arcText - arcLex
arcLexMinText = arcLex - arcText

hboTextMinLex = hboText - hboLex
hboLexMinText = hboLex - hboText

for (myset, mymsg) in (
    (arcTextMinLex, 'arc: lexemes in text but not in lexicon'),
    (arcLexMinText, 'arc: lexemes in lexicon but not in text'),
    (hboTextMinLex, 'hbo: lexemes in text but not in lexicon'),
    (hboLexMinText, 'hbo: lexemes in lexicon but not in text'),
):
    print('{}: {}x{}'.format(mymsg, len(myset), '' if not myset else '\n\t{}'.format(', '.join(sorted(myset)))))


# ## Consistency of vocalized lexeme
# 
# The lexicon file provides an attribute `vc` for each lexeme, which is the vocalized lexeme.
# The ETCBC core data also has features `g_voc_lex` and `g_voc_lex_utf8` for each occurrence.
# 
# We investigate whether the latter features are *consistent*, i.e. a property of the lexeme and lexeme only.
# If they are somehow dependent on the word occurrence, they are not consistent.
# 
# When they are consistent, we can omit them on the occurrences and use them on the lexemes.
# We'll also check whether the `vc` property found in the lexicon coincides with the `g_voc_lex` on the occurrences.
# 
# Supposing it is all consistent, we will call the new lexeme features `voc_lex` and `voc_lex_utf8`.

# In[13]:


vocFeatures = dict(voc_lex={}, voc_lex_utf8={})

exceptions = dict(incons=dict((f, {}) for f in vocFeatures), deviating=dict())

missing = {}

def showExceptions(cases):
    nCases = len(cases)
    if nCases == 0:
        print('Fully consistent')
    else:
        print('{} inconsistent cases'.format(nCases))
        limit = 10
        for (i, (lan, lex)) in enumerate(cases):
            if i == limit:
                print('...and {} more.'.format(nCases - limit))
                break
            print('{}-{}: {}'.format(lan, lex, ', '.join(sorted(cases[(lan, lex)]))))

for w in F.otype.s('word'):
    lan = langMap[F.language.v(w)]
    lex = F.lex.v(w)
    for (f, values) in vocFeatures.items():
        current = values.get((lan, lex), None)
        new = Fs('g_{}'.format(f)).v(w)
        if current == None:
            values[(lan, lex)] = new
            if f == 'voc_lex':
                lexical = lexEntries[lan][lex].get('vc', None)
                if lexical == None:
                    missing[(lan, lex)] = new
                else:
                    if lexical != new: exceptions['deviating'].setdefault((lan, lex), {lexical}).add(new)
        else:
            if current != new:
                exceptions['incons'][f].setdefault((lan, lex), {current}).add(new)

nMissing = len(missing)
print('lexemes with missing vc property: {}x'.format(nMissing))
for (lan, lex) in sorted(missing)[0:20]:
    print('\t{}-{} supplied from occurrence: {}'.format(lan, lex, vocFeatures['voc_lex'][(lan, lex)]))
for f in vocFeatures:
    print('Have all occurrences of a lexeme the same {} value?'.format(f))
    showExceptions(exceptions['incons'][f])
print('Are the voc_lex values of the lexeme consistent with the vc value of the lexeme?')
showExceptions(exceptions['deviating'])                          


# # Prepare TF features
# 
# We now collect the lexical information into the features for nodes of type `lex`.

# In[14]:


nodeFeatures = {}

lexFields = (
    ('rt', 'root'),
    ('sp', 'sp'),
    ('sm', 'nametype'),
    ('ls', 'ls'),
    ('gl', 'gloss'),
)

overlapFeatures = {'lex', 'language', 'sp', 'ls'} # both on word- and lex- otypes

for f in overlapFeatures:
    nodeFeatures[f] = dict((n, Fs(f).v(n)) for n in N() if Fs(f).v(n) != None)

newFeatures = [f[1] for f in lexFields]

for (lan, lexemes) in lexEntries.items():
    for (lex, lexValues) in lexemes.items():
        node = nodeFromLex[(lan, lex)]
        nodeFeatures.setdefault('lex', {})[node] = lex
        nodeFeatures.setdefault('language', {})[node] = lan
        for (f, newF) in lexFields:
            value = lexValues.get(f, None)
            if value != None:
                nodeFeatures.setdefault(newF, {})[node] = value
        for (f, vocValues) in vocFeatures.items():
            value = vocValues.get((lan, lex), None)
            if value != None:
                nodeFeatures.setdefault(f, {})[node] = value


# We address the issues listed under varia above.

# In[15]:


nodeFeatures['lex0'] = {}
nodeFeatures['lex_utf8'] = {}

for n in F.otype.s('word'):
    lex = F.lex.v(n).rstrip('[/=')
    lan = F.language.v(n)
    nodeFeatures['lex0'][n] = lex
    nodeFeatures['lex_utf8'][n] = Transcription.to_hebrew(lex)
    nodeFeatures['language'][n] = langMap[lan]


# In[16]:


testNodes = range(maxNode+1, maxNode + 10)
[nodeFeatures['voc_lex_utf8'][n] for n in testNodes]


# We update the `otype`, `otext` and `oslots` features.

# In[17]:


metaData = {}
edgeFeatures = {}

metaData['otext'] = dict()
metaData['otext'].update(T.config)
metaData['otext'].update(getOtext())
metaData['otype'] = dict(valueType='str')
metaData['oslots'] = dict(valueType='str')

for f in nodeFeatures:
    metaData[f] = {}
    metaData[f].update(provenanceMetadata)
    metaData[f]['valueType'] = 'str'

nodeFeatures['otype'] = dict((n, F.otype.v(n)) for n in range(1, maxNode +1))
nodeFeatures['otype'].update(otypeData)
edgeFeatures['oslots'] = dict((n, E.oslots.s(n)) for n in range(maxSlot + 1, maxNode +1))
edgeFeatures['oslots'].update(oslotsData)


# We specify the features to delete and list the new/changed features.

# In[18]:


deleteFeatures = set('''
    g_voc_lex
    g_voc_lex_utf8
'''.strip().split())


# In[19]:


changedDataFeatures = set(nodeFeatures) | set(edgeFeatures)
changedFeatures = changedDataFeatures | {'otext'}


# # Stage: TF generation
# Transform the collected information in feature-like datastructures, and write it all
# out to `.tf` files.

# In[20]:


def tfFromData():
    startNow()
    tprint('write new/changed features to TF ...')
    TF = Fabric(locations=thisSave)
    TF.save(nodeFeatures=nodeFeatures, edgeFeatures=edgeFeatures, metaData=metaData)

tfFromData()


# # Stage: Diffs
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

# In[21]:


checkDiffs(thisSave, thisDeliver, only=changedFeatures)


# # Stage: Deliver 
# 
# Copy the new TF dataset from the temporary location where it has been created to its final destination.

# In[22]:


deliverFeatures(thisSave, thisDeliver, changedFeatures, deleteFeatures=deleteFeatures)


# # Stage: Compile TF
# 
# We load the new features, use the new format, check some values

# In[23]:


startNow()
tprint('load features')
TF = Fabric(locations=thisTf, modules=module)
api = TF.load(' '.join(changedDataFeatures))
F = api.F
Fs = api.Fs
T = api.T
L = api.L


# In[25]:


features = [f[1] for f in lexFields] + ['voc_lex', 'voc_lex_utf8']

def printLex(w):
    info = dict((f, Fs(f).v(w)) for f in features)
    print('\t{} - {} - {}x'.format(
        F.language.v(w),
        F.lex.v(w),
        len(L.d(w, otype='word'))
    ))
    for f in sorted(info):
        print('\t\t{:<15} = {}'.format(f, info[f]))

print('new format (using lex0)')
print(T.text(range(1,12), fmt='lex-trans-plain'))
print('lex_utf8 feature')
print(' '.join(F.lex_utf8.v(w) for w in range(1,12)))
print('language feature')
print(' '.join(F.language.v(w) for w in range(1,12)))
for w in range(1, 12): printLex(L.u(w, otype='lex')[0])


# In[ ]:




