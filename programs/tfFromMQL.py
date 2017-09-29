
# coding: utf-8

# <img align="right" src="tf-small.png"/>
# 
# # TF from MQL
# 
# This notebook can read an
# [MQL](https://emdros.org/mql.html)
# dump of a version of the [BHSA](https://github.com/ETCBC/bhsa) Hebrew Text Database
# and transform it in a Text-Fabric
# [Text-Fabric](https://github.com/ETCBC/text-fabric)
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
# Yet this is what we do, the error-prone thing. We then avoid installing and configuring and managing Emdros, MySQL/sqLite3.
# Aside the upfront work to get this going, the going after that is also much slower.
# 
# So here you are, a smallish script to do an awful lot of work, mostly correct, if careful used.
# 
# # Caveat
# 
# This notebook makes use of a new feature of text-fabric, first present in 2.3.12.
# Make sure to upgrade first.
# 
# ```sudo -H pip3 install text-fabric
# ```
# 
# # Buffer function
# The ETCBC does not yet produce an MQL file that satisfies all the requirements.
# Some features are still missing, some values seem to have been mangled somewhere in the creation workflow.
# 
# This pipeline implements workarounds for those issues.
# The source data, as delivered by the ETCBC on a weekly basis, may change suddenly in minor details,
# which could break applications further down the line.
# 
# This pipeline, with and in particular this repository is a useful tool to work around those issues
# temporarily and to provide feedback to the ETCBC, which will hopefully lead to a more 
# consistent data interface over time.

# In[1]:


import os,sys,re,collections
from shutil import rmtree
from tf.fabric import Fabric
from tf.helpers import setFromSpec
import utils
from blang import bookLangs, bookNames


# # Pipeline
# See [operation](https://github.com/ETCBC/pipeline/blob/master/README.md#operation) 
# for how to run this script in the pipeline.

# In[2]:


if 'SCRIPT' not in locals():
    SCRIPT = False
    FORCE = True
    CORE_NAME = 'bhsa'
    VERSION = 'c'
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
mqlzFile = '{}/{}.mql.bz2'.format(thisSource, CORE_NAME)

thisTemp = '{}/_temp/{}'.format(thisRepo, VERSION)
mqlFile = '{}/{}.mql'.format(thisTemp, CORE_NAME)
thisSave = '{}/{}'.format(thisTemp, module)

thisTf = '{}/tf/{}'.format(thisRepo, VERSION)
thisDeliver = '{}/{}'.format(thisTf, module)


# # Test
# 
# Check whether this conversion is needed in the first place.
# Only when run as a script.

# In[4]:


if SCRIPT:
    testFile = '{}/.tf/otype.tfx'.format(thisDeliver)
    (good, work) = utils.mustRun(mqlzFile, '{}/.tf/otype.tfx'.format(thisDeliver), force=FORCE)
    if not good: stop(good=False)
    if not work: stop(good=True)


# # TF Settings
# 
# We add some custom information here.
# 
# * the MQL object type that corresponds to the TF slot type, typically `word`;
# * a piece of metadata that will go into every feature; the time will be added automatically
# * suitable text formats for the `otext` feature of TF.
# 
# The oText feature is very sensitive to what is available in the source MQL.
# It needs to be configured here.
# We save the configs we need per source and version.
# And we define a stripped down default version to start with.

# In[5]:


slotType = 'word'

featureMetadata = dict(
    dataset='BHSA',
    datasetName='Biblia Hebraica Stuttgartensia Amstelodamensis',
    author='Eep Talstra Centre for Bible and Computer',
    encoders='Constantijn Sikkel (QDF), Ulrik Petersen (MQL) and Dirk Roorda (TF)',
    website='https://shebanq.ancient-data.org',
    email='shebanq@ancient-data.org',
)

oText = {
    '': {
        '': '''
@sectionFeatures=book,chapter,verse
@sectionTypes=book,chapter,verse
@fmt:text-orig-full={g_word_utf8}{g_suffix_utf8}
''',
    },
    '4': '''
@fmt:lex-orig-full={g_lex_utf8} 
@fmt:lex-orig-plain={lex_utf8} 
@fmt:lex-trans-full={g_lex} 
@fmt:lex-trans-plain={lex} 
@fmt:text-orig-full={g_qere_utf8/g_word_utf8}{qtrailer_utf8/trailer_utf8}
@fmt:text-orig-full-ketiv={g_word_utf8}{trailer_utf8}
@fmt:text-orig-plain={g_cons_utf8}{trailer_utf8}
@fmt:text-trans-full={g_word} 
@fmt:text-trans-full-ketiv={g_word} 
@fmt:text-trans-plain={g_cons} 
@sectionFeatures=book,chapter,verse
@sectionTypes=book,chapter,verse
''',
    '4b': '''
@fmt:lex-orig-full={g_lex_utf8} 
@fmt:lex-orig-plain={lex_utf8} 
@fmt:lex-trans-full={g_lex} 
@fmt:lex-trans-plain={lex} 
@fmt:text-orig-full={g_qere_utf8/g_word_utf8}{qtrailer_utf8/trailer_utf8}
@fmt:text-orig-full-ketiv={g_word_utf8}{trailer_utf8}
@fmt:text-orig-plain={g_cons_utf8}{trailer_utf8}
@fmt:text-trans-full={g_word} 
@fmt:text-trans-full-ketiv={g_word} 
@fmt:text-trans-plain={g_cons} 
@sectionFeatures=book,chapter,verse
@sectionTypes=book,chapter,verse
''',
    'c': '''
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
''',
    '2017': '''
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
''',
}


# The next function selects the proper otext material, falling back on a default if nothing 
# appropriate has been specified in `oText`.

# In[6]:


def getOtext():
    thisOtext = oText.get(VERSION, oText[''])
    otextInfo = dict(line[1:].split('=', 1) for line in thisOtext.strip('\n').split('\n'))

    if thisOtext is oText['']:
        utils.caption(0, 'WARNING: no otext feature info provided, using a meager default value') 
    else:
        utils.caption(0, 'INFO: otext feature information found')
    for x in sorted(otextInfo.items()):
        utils.caption(0, '\t{:<20} = "{}"'.format(*x))
    return otextInfo


# # Overview
# 
# The program has several stages:
#    
# 1. **prepare** the source (utils.bunzip if needed)
# 1. **parse MQL** and collect information in datastructures
# 1. **transform to TF** write the datastructures as TF features
# 1. **differences** (informational)
# 1. **deliver** the tf data at its destination directory
# 1. **compile** all tf features to binary format
# 
# Stages **parseMQL** and **transform to TF** communicate with the help of several global variables:
# 
# * data containers for the MQL kinds of data
#   * enumerations
#   * object types
#   * tables
# 
# * data containers for the TF features to be generated,
#   * node features
#   * edge features.

# In[7]:


objectTypes = dict()
tables = dict()

edgeF = dict()
nodeF = dict()


# # Stage: Prepare
# 
# Check the source, utils.bunzip it if needed, empty the result directory.

# In[8]:


def prepare():
    global thisoText

    if not os.path.exists(thisTemp):
        os.makedirs(thisTemp)

    utils.caption(0, 'bunzipping {} ...'.format(mqlzFile))
    utils.bunzip(mqlzFile, mqlFile)
    utils.caption(0, 'Done')

    if os.path.exists(thisSave): rmtree(thisSave)
    os.makedirs(thisSave)

    thisoText = getOtext()


# Convert a monads specification (a comma separated sequence of numbers and number ranges)
# into a set of integers.

# # Stage: MQL parsing
# Plough through the MQL file and grab all relevant information
# and put it into the dedicated data structure.

# In[13]:


uniscan = re.compile(r'(?:\\x..)+')

def makeuni(match):
    ''' Make proper unicode of a text that contains byte escape codes such as backslash xb6
    '''
    byts = eval('"' + match.group(0) + '"')
    return byts.encode('latin1').decode('utf-8')

def uni(line): return uniscan.sub(makeuni, line)
    
def parseMql():
    utils.caption(4, 'Parsing mql source ...')
    fh = open(mqlFile)

    curId = None
    curEnum = None
    curObjectType = None
    curTable = None
    curObject = None
    curValue = None
    curFeature = None

    STRING_TYPES = {'ascii', 'string'}

    enums = dict()

    chunkSize = 1000000
    inThisChunk = 0

    good = True

    for (ln, line) in enumerate(fh):
        inThisChunk += 1
        if inThisChunk == chunkSize:
            utils.caption(0, '\tline {:>9}'.format(ln + 1))
            inThisChunk = 0
        if line.startswith('CREATE OBJECTS WITH OBJECT TYPE') or line.startswith('WITH OBJECT TYPE'):
            comps = line.rstrip().rstrip(']').split('[', 1)
            curTable = comps[1]
            utils.caption(0, '\t\tobjects in {}'.format(curTable))
            curObject = None
            if not curTable in tables:
                tables[curTable] = dict()
        elif curEnum != None:
            if line.startswith('}'):
                curEnum = None
                continue
            comps = line.strip().rstrip(',').split('=', 1)
            comp = comps[0].strip()
            words = comp.split()
            if words[0] == 'DEFAULT':
                enums[curEnum]['default'] = uni(words[1])
                value = words[1]
            else:
                value = words[0]
            enums[curEnum]['values'].append(value)
        elif curObjectType != None:
            if line.startswith(']'):
                curObjectType = None
                continue
            if curObjectType == True:
                if line.startswith('['):
                    curObjectType = line.rstrip()[1:]
                    objectTypes[curObjectType] = dict()
                    utils.caption(0, '\t\totype {}'.format(curObjectType))
                    continue
            comps = line.strip().rstrip(';').split(':', 1)
            feature = comps[0].strip()
            fInfo = comps[1].strip()
            fCleanInfo = fInfo.replace('FROM SET', '')
            fInfoComps = fCleanInfo.split(' ', 1)
            fMQLType = fInfoComps[0]
            fDefault = fInfoComps[1].strip().split(' ', 1)[1] if len(fInfoComps) == 2 else None
            if fDefault != None and fMQLType in STRING_TYPES:
                fDefault = uni(fDefault[1:-1])
            default = enums.get(fMQLType, {}).get('default', fDefault)
            ftype = 'str' if fMQLType in enums else                    'int' if fMQLType == 'integer' else                    'str' if fMQLType in STRING_TYPES else                    'int' if fInfo == 'id_d' else                    'str'
            isEdge = fMQLType == 'id_d'
            if isEdge:
                edgeF.setdefault(curObjectType, set()).add(feature)
            else:
                nodeF.setdefault(curObjectType, set()).add(feature)

            objectTypes[curObjectType][feature] = (ftype, default)
            utils.caption(0, '\t\t\tfeature {} ({}) =def= {} : {}'.format(feature, ftype, default, 'edge' if isEdge else 'node'))
        elif curTable != None:
            if curObject != None:
                if line.startswith(']'):
                    objectType = objectTypes[curTable]
                    for (feature, (ftype, default)) in objectType.items():
                        if feature not in curObject['feats'] and default != None:
                            curObject['feats'][feature] = default
                    tables[curTable][curId] = curObject
                    curObject = None
                    continue
                elif line.startswith('['):
                    continue
                elif line.startswith('FROM MONADS'):
                    monads = line.split('=', 1)[1].replace('{', '').replace('}', '').replace(' ','').strip()
                    curObject['monads'] = setFromSpec(monads)
                elif line.startswith('WITH ID_D'):
                    comps = line.replace('[', '').rstrip().split('=', 1)
                    curId = int(comps[1])
                elif line.startswith('GO'):
                    continue
                elif line.strip() == '':
                    continue
                else:
                    if curValue != None:
                        toBeContinued = not line.rstrip().endswith('";')
                        if toBeContinued:
                            curValue += line
                        else:
                            curValue += line.rstrip().rstrip(';').rstrip('"')
                            curObject['feats'][curFeature] = uni(curValue)
                            curValue = None
                            curFeature = None
                        continue
                    if ':=' in line:
                        (featurePart, valuePart) = line.split('=', 1)
                        feature = featurePart[0:-1].strip()
                        isText = ':="' in line
                        toBeContinued = isText and not line.rstrip().endswith('";')
                        if toBeContinued:
                            # this happens if a feature value contains a new line
                            # we must continue scanning lines until we meet the ned of the value
                            curFeature = feature
                            curValue = valuePart.lstrip('"')
                        else:
                            value = valuePart.rstrip().rstrip(';').strip('"')
                            curObject['feats'][feature] = uni(value) if isText else value
                    else:
                        utils.caption(0, 'ERROR: line {}: unrecognized line -->{}<--'.format(ln, line))
                        good = False
                        break
            else:
                if line.startswith('CREATE OBJECT'):
                    curObject = dict(feats=dict(), monads=None)
                    curId = None
        else:
            if line.startswith('CREATE ENUMERATION'):
                words = line.split()
                curEnum = words[2]
                enums[curEnum] = dict(default=None, values=[])
                utils.caption(0, '\t\tenum {}'.format(curEnum))
            elif line.startswith('CREATE OBJECT TYPE'):
                curObjectType = True
    utils.caption(0, '{} lines parsed'.format(ln + 1))
    fh.close()
    for table in tables:
        utils.caption(0, '{} objects of type {}'.format(len(tables[table]), table))
    if not good:
        stop(good=False)


# # Stage: TF generation
# Transform the collected information in feature-like datastructures, and write it all
# out to `.tf` files.

# In[14]:


def tfFromData():
    utils.caption(4, 'Making TF data ...')
    
    NIL = {'nil', 'NIL', 'Nil'}

    tableOrder = [slotType]+[t for t in sorted(tables) if t != slotType]

    nodeFromIdd = dict()
    iddFromNode = dict()

    nodeFeatures = dict()
    edgeFeatures = dict()
    metaData = dict()

    # metadata that ends up in every feature
    metaData[''] = featureMetadata

    # the config feature otext
    metaData['otext'] = thisoText

    # multilingual book names
    for (langCode, (langEnglish, langName)) in bookLangs.items():
        metaData['book@{}'.format(langCode)] = {
            'valueType': 'str',
            'language': langName,
            'languageCode': langCode,
            'languageEnglish': langEnglish,
        }

    utils.caption(0, 'Monad - idd mapping ...')
    otype = dict()
    for idd in tables.get(slotType, {}):
        monad = list(tables[slotType][idd]['monads'])[0]
        nodeFromIdd[idd] = monad
        iddFromNode[monad] = idd
        otype[monad] = slotType

    maxSlot = max(nodeFromIdd.values()) if len(nodeFromIdd) else 0
    utils.caption(0, 'maxSlot={}'.format(maxSlot))

    utils.caption(0, 'Node mapping and otype ...')
    node = maxSlot
    for t in tableOrder[1:]:
        for idd in sorted(tables[t]):
            node += 1
            nodeFromIdd[idd] = node
            iddFromNode[node] = idd
            otype[node] = t

    nodeFeatures['otype'] = otype
    metaData['otype'] = dict(
        valueType='str',
    )

    utils.caption(0, 'oslots ...')
    oslots = dict()
    for t in tableOrder[1:]:
        for idd in tables.get(t, {}):
            node = nodeFromIdd[idd]
            monads = tables[t][idd]['monads']
            oslots[node] = monads
    edgeFeatures['oslots'] = oslots
    metaData['oslots'] = dict(
        valueType='str',
    )

    utils.caption(0, 'metadata ...')
    for t in nodeF:
        for f in nodeF[t]:
            ftype = objectTypes[t][f][0]
            metaData.setdefault(f, {})['valueType'] = ftype
    for t in edgeF:
        for f in edgeF[t]:
            metaData.setdefault(f, {})['valueType'] = 'str'

    utils.caption(4, 'features ...')
    chunkSize = 100000
    for t in tableOrder:
        utils.caption(0, '\tfeatures from {}s'.format(t))
        inThisChunk = 0
        for (i, idd) in enumerate(tables.get(t, {})):
            inThisChunk += 1
            if inThisChunk == chunkSize:
                utils.caption(0, '\t{:>9} {}s'.format(i + 1, t))
                inThisChunk = 0
            node = nodeFromIdd[idd]
            features = tables[t][idd]['feats']
            for (f, v) in features.items():
                isEdge = f in edgeF.get(t, set())
                if isEdge:
                    if v not in NIL:
                        edgeFeatures.setdefault(f, {}).setdefault(node, set()).add(nodeFromIdd[int(v)])
                else:
                    nodeFeatures.setdefault(f, {})[node] = v
        utils.caption(0, '\t{:>9} {}s'.format(i + 1, t))

    utils.caption(0, 'book names ...')
    nodeFeatures['book@la'] = nodeFeatures.get('book', {})
    bookNodes = sorted(nodeFeatures.get('book', {}))
    for (langCode, langBookNames) in bookNames.items():
        nodeFeatures['book@{}'.format(langCode)] = dict(zip(bookNodes, langBookNames))

    utils.caption(4, 'write data set to TF ...')

    TF = Fabric(locations=thisSave, silent=True)
    TF.save(nodeFeatures=nodeFeatures, edgeFeatures=edgeFeatures, metaData=metaData)


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

# # Stage: Deliver 
# 
# Copy the new TF dataset from the temporary location where it has been created to its final destination.

# # Stage: Compile TF
# 
# Just to see whether everything loads and the precomputing of extra information works out.
# Moreover, if you want to work with these features, then the precomputing has already been done, and everything is quicker in subsequent runs.
# 
# We issue load statement to trigger the precomputing of extra data.
# Note that all features specified text formats in the `otext` config feature,
# will be loaded, as well as the features for sections.
# 
# At that point we have access to the full list of features.
# We grab them and are going to load them all! 

# In[15]:


def compileTfData():
    utils.caption(4, 'Load and compile standard TF features')
    TF = Fabric(locations=thisTf, modules=module)
    api = TF.load('')

    utils.caption(4, 'Load and compile all other TF features')
    allFeatures = TF.explore(silent=False, show=True)
    loadableFeatures = allFeatures['nodes'] + allFeatures['edges']
    api = TF.load(loadableFeatures)
    T = api.T
    
    utils.caption(4, 'Basic test')
    utils.caption(4, 'First verse in all formats')
    for fmt in T.formats:
        utils.caption(0, '{}'.format(fmt), continuation=True)
        utils.caption(0, '\t{}'.format(T.text(range(1,12), fmt=fmt)), continuation=True)


# # Run it!

# In[16]:


prepare()


# In[17]:


parseMql()


# In[18]:


tfFromData()


# In[19]:


utils.checkDiffs(thisSave, thisDeliver)


# In[20]:


utils.deliverDataset(thisSave, thisDeliver)


# In[21]:


compileTfData()


# In[ ]:




