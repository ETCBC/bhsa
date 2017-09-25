
# coding: utf-8

# <img align="right" src="tf-small.png"/>
# 
# # Add Statistics
# 
# This notebook can add statistical features to a 
# [BHSA](https://github.com/ETCBC/bhsa) dataset in
# [text-Fabric](https://github.com/ETCBC/text-fabric)
# format.
# 
# ## Discussion
# 
# We add the features
# `freq_occ freq_lex rank_occ rank_lex`.
# 
# We assume that the dataset has these features present:
# 
# * `language` for determining if the word is Hebrew or Aramaic 
# * `g_cons` to get the word string in consonantal transcription
# * `lex` to get the lexical identifier in consonantal transcription
# 
# This program works for all datasets and versions that have these features with the
# intended meanings.
# 
# #### Languages
# We will not identify lexemes and word occurrences across language.
# So if two occurrences or lexemes exhibit the same string, but htey are categorized as belonging
# to different languages, they will not be identified.
# 
# #### Occurrences
# We group occurrences by their consonantal transcriptions. 
# So if two occurrences differ only in pointing, we count them as two occurrences of the same value.
# 
# #### Lexemes
# Lexemes are identified by the `lex` feature within a biblical language.
# We will not identify lexemes across language.
# 
# # Execution mode
# See the notebook tfFromMQL in this directory for an explantion of the `SCRIPT` variable below.

# In[1]:


import os,sys,re,collections
from glob import glob
from shutil import rmtree, copytree
from tf.fabric import Fabric
from utils import bunzip, startNow, tprint
from blang import bookLangs, bookNames


# In[2]:


if 'SCRIPT' not in locals():
    SCRIPT = False
    SOURCE_NAME = 'bhsa'
    VERSION= 'd'
    TF_MODULE ='core' 


# # Setting up the context: source file and target directories
# 
# The conversion is executed in an environment of directories, so that sources, temp files and
# results are in convenient places and do not have to be shifted around.

# In[3]:


repoBase = os.path.expanduser('~/github/bhsa')

sourceBase = '{}/source'.format(repoBase)
targetBase = '{}/tf'.format(repoBase)

tfLocation = '{}/{}'.format(targetBase, VERSION)
tfSave = '{}/{}/{}'.format(targetBase, VERSION, TF_MODULE)
tfDeliver = '{}/{}'.format(tfLocation, TF_MODULE)


# In[4]:


newFeaturesStr = '''
    freq_occ
    freq_lex
    rank_occ
    rank_lex
'''
newFeatures = newFeaturesStr.strip().split()


# # Test
# 
# Check whether this conversion is needed in the first place.
# Only when run as a script.

# In[5]:


if SCRIPT:
    (good, work) = MUSTRUN(None, '{}/.tf/{}.tfx'.format(tfDeliver, newFeatures[0]))
    if not good: sys.exit(1)
    if not work: sys.exit(0)


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

# # Stage: Collect
# 
# We collect the statistics.

# In[11]:


def collect():
    startNow()
    tprint('Computing statistics')

    TF = Fabric(locations=tfLocation, modules=TF_MODULE)
    api = TF.load('language lex g_cons')
    F = api.F
    
    tprint('Counting')
    wstats = {
        'freqs': {
            'lex': collections.defaultdict(lambda: collections.Counter()),
            'occ': collections.defaultdict(lambda: collections.Counter()),
        },
        'ranks': {
            'lex': collections.defaultdict(lambda: {}),
            'occ': collections.defaultdict(lambda: {}),
        },
    }
    langs = set()

    for w in F.otype.s('word'):
        occ = F.g_cons.v(w)
        lex = F.lex.v(w)
        lan = F.language.v(w)
        wstats['freqs']['lex'][lan][lex] += 1
        wstats['freqs']['occ'][lan][occ] += 1
        langs.add(lan)
    for lan in langs:
        for tp in ['lex', 'occ']:
            rank = -1
            prev_n = -1
            amount = 1
            for (x, n) in sorted(wstats['freqs'][tp][lan].items(), key=lambda y: (-y[1], y[0])):
                if n == prev_n:
                    amount += 1
                else:
                    rank += amount
                    amount = 1
                prev_n = n
                wstats['ranks'][tp][lan][x] = rank

    tprint('Making features')
    metaData={}
    nodeFeatures = {}
    edgeFeatures = {}
    
    for ft in (newFeatures):
        nodeFeatures[ft] = {}
        metaData.setdefault(ft, {})['valueType'] = 'int'

    for w in F.otype.s('word'):
        lan = F.language.v(w)
        occ = F.g_cons.v(w)
        lex = F.lex.v(w)
        nodeFeatures['freq_occ'][w] = str(wstats['freqs']['occ'][lan][occ])
        nodeFeatures['rank_occ'][w] = str(wstats['ranks']['occ'][lan][occ])
        nodeFeatures['freq_lex'][w] = str(wstats['freqs']['lex'][lan][lex])
        nodeFeatures['rank_lex'][w] = str(wstats['ranks']['lex'][lan][lex])

    tprint('Write out')
    TF = Fabric(locations=tfSave)
    TF.save(nodeFeatures=nodeFeatures, edgeFeatures=edgeFeatures, metaData=metaData)
    
    tprint('Compile and test')
    TF = Fabric(locations=tfLocation, modules=TF_MODULE)
    api = TF.load('lex '+newFeaturesStr)
    F = api.F
    mostFrequent = set()
    
    topX = 10
    for w in sorted(F.otype.s('word'), key=lambda w: -F.freq_lex.v(w)):
        mostFrequent.add(F.lex.v(w))
        if len(mostFrequent) == topX: break
            
    print('Top {} freqent lexemes = {}'.format(
        topX,
        '\n\t'.join(mostFrequent),
    ))
    tprint('Done')


# # Run it!

# In[12]:


collect()


# If in script mode, we should tell whether the execution was successful or not.

# In[8]:


if SCRIPT: sys.exit(0 if good else 1)

