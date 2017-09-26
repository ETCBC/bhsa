import sys,os,collections,time,bz2
from glob import glob

def bunzip(bzFile, uzFile):
    with bz2.open(bzFile, mode='rt') as bdata:
        fh = open(uzFile, 'w')
        fh.write(bdata.read())
        fh.close

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
        with open(existingPath) as h: eLines = (d for d in h.readlines() if not d.startswith('@'))
        with open(newPath) as h: nLines = (d for d in h.readlines() if not d.startswith('@'))
        i = 0
        equal = True
        for (e, n) in zip(eLines, nLines):
            i += 1
            if e != n:
                print('First diff in line {} after the  metadata'.format(i))
                equal = False
                continue
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
