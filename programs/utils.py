import sys,os,collections,time,bz2
from shutil import rmtree, copytree, copy
from itertools import zip_longest
from glob import glob

def bunzip(bzFile, uzFile):
    xB = os.path.exists(bzFile)
    xU = os.path.exists(uzFile)
    if not xB:
        if xU:
            print('WARNING: {} is missing. Using existing {}'.format(bzFile, uzFile))
        else:
            print('ERROR: Cannot make {} because {} is missing'.format(uzFile, bzFile))
        return
    if not xU or os.path.getmtime(bzFile) > os.path.getmtime(uzFile):
        with bz2.open(bzFile, mode='rt') as bdata:
            fh = open(uzFile, 'w')
            fh.write(bdata.read())
            fh.close
    else:
        print('NOTE: Using existing {} which is newer than {}'.format(uzFile, bzFile))

timestamp = None

def startNow():
    global timestamp
    timestamp = time.time()

def _duration():
    interval = time.time() - timestamp
    if interval < 10: return "{: 2.2f}s".format(interval)
    interval = int(round(interval))
    if interval < 60: return "{:>2d}s".format(interval)
    if interval < 3600: return "{:>2d}m {:>02d}s".format(interval // 60, interval % 60)
    return "{:>2d}h {:>02d}m {:>02d}s".format(interval // 3600, (interval % 3600) // 60, interval % 60)

def tprint(msg):
    print('{:>11} {}'.format(_duration(), msg))

def checkDiffs(thisSave, thisDeliver, only=None):
    def diffFeature(f):
        sys.stdout.write('{:<25} ... '.format(f))
        existingPath = '{}/{}.tf'.format(thisDeliver, f)
        newPath = '{}/{}.tf'.format(thisSave, f)
        with open(existingPath) as h:
            eLines = h.readlines() if f == 'otext' else (d for d in h.readlines() if not d.startswith('@'))
        with open(newPath) as h:
            nLines = h.readlines() if f == 'otext' else (d for d in h.readlines() if not d.startswith('@'))
        i = 0
        equal = True
        for (e, n) in zip_longest(eLines, nLines, fillvalue='<empty>'):
            i += 1
            if e != n:
                print('First diff in line {} {}'.format(i, '' if f == 'otext' else 'after the metadata'))
                print('OLD -->{}<--'.format(e[0:50]))
                print('NEW -->{}<--'.format(n[0:50]))
                equal = False
                if i > 2: break
        
        print('no changes' if equal else '')

    startNow()
    tprint('checkDiffs')
    existingFiles = glob('{}/*.tf'.format(thisDeliver))
    newFiles = glob('{}/*.tf'.format(thisSave))
    existingFeatures = {os.path.basename(os.path.splitext(f)[0]) for f in existingFiles}
    newFeatures = {os.path.basename(os.path.splitext(f)[0]) for f in newFiles}

    if only != None:
        existingFeatures &= only
        newFeatures &= only

    addedOnes = newFeatures - existingFeatures
    deletedOnes = existingFeatures - newFeatures
    commonOnes = newFeatures & existingFeatures

    if addedOnes:
        print('{} features to add:\n\t{}'.format(len(addedOnes), ' '.join(sorted(addedOnes))))
    else:
        print('no features to add')
    if deletedOnes:
        print('{} features to delete:\n\t{}'.format(len(deletedOnes), ' '.join(sorted(deletedOnes))))
    else:
        print('no features to delete')

    print('{} features in common'.format(len(commonOnes)))
    
    for f in sorted(commonOnes): diffFeature(f)

def deliverDataset(thisSave, thisDeliver):
    print('Copy data set to {}'.format(thisDeliver))
    if os.path.exists(thisDeliver):
        rmtree(thisDeliver)
    copytree(thisSave, thisDeliver)

def deliverFeatures(thisSave, thisDeliver, newFeatures, deleteFeatures=None):
    print('Copy features from {} to {}'.format(thisSave, thisDeliver))
    for feature in newFeatures:
        tempLoc = '{}/{}.tf'.format(thisSave, feature)
        deliverLoc = '{}/{}.tf'.format(thisDeliver, feature)
        print(feature)
        copy(tempLoc, deliverLoc)
    if deleteFeatures != None:
        print('Delete features from {}'.format(thisDeliver))
        for feature in deleteFeatures:
            deliverLoc = '{}/{}.tf'.format(thisDeliver, feature)
            if os.path.exists(deliverLoc):
                os.remove(deliverLoc)




