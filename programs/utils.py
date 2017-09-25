import os,collections,time,bz2

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

