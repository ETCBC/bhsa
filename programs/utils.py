# WARNING: DO NOT EDIT if this file is not in the pipeline repo !!!
# FILE WILL BE OVERWRITTEN

# The master copy of this file is the one in the pipeline repo.
# When the pipeline runs, the master copy is copied into
# all involved repos, overwriting the copy existing there.


import sys
import os
import time
import bz2
import gzip as gz
from shutil import rmtree, copytree, copy
from itertools import zip_longest
from glob import glob


def bzip(uzFile, bzFile):
    xB = os.path.exists(bzFile)
    xU = os.path.exists(uzFile)
    if not xU:
        if xB:
            caption(
                0, "\tWARNING: unzipped file is missing. Using existing bzipped file"
            )
        else:
            caption(0, "\tERROR: Cannot bzip because unzipped file is missing")
        return
    if not xB or os.path.getmtime(uzFile) > os.path.getmtime(bzFile):
        with bz2.open(bzFile, mode="wt") as bdata:
            with open(uzFile, "r") as udata:
                bdata.write(udata.read())
    else:
        caption(
            0, "\tNOTE: Using existing bzipped file which is newer than unzipped one"
        )


def bunzip(bzFile, uzFile):
    xB = os.path.exists(bzFile)
    xU = os.path.exists(uzFile)
    if not xB:
        if xU:
            caption(
                0, "\tWARNING: bzipped file is missing. Using existing unzipped file"
            )
        else:
            caption(0, "\tERROR: Cannot unzip because bzipped file is missing")
        return
    if not xU or os.path.getmtime(bzFile) > os.path.getmtime(uzFile):
        with bz2.open(bzFile, mode="rt") as bdata:
            with open(uzFile, "w") as udata:
                udata.write(bdata.read())
    else:
        caption(
            0, "\tNOTE: Using existing unzipped file which is newer than bzipped one"
        )


def gzip(uzFile, gzFile):
    xB = os.path.exists(gzFile)
    xU = os.path.exists(uzFile)
    if not xU:
        if xB:
            caption(
                0, "\tWARNING: unzipped file is missing. Using existing gzipped file"
            )
        else:
            caption(0, "\tERROR: Cannot gzip because unzipped file is missing")
        return
    if not xB or os.path.getmtime(uzFile) > os.path.getmtime(gzFile):
        with gz.open(gzFile, mode="wt") as gdata:
            with open(uzFile, "rt") as udata:
                gdata.write(udata.read())
    else:
        caption(
            0, "\tNOTE: Using existing gzipped file which is newer than unzipped one"
        )


def gunzip(gzFile, uzFile):
    xB = os.path.exists(gzFile)
    xU = os.path.exists(uzFile)
    if not xB:
        if xU:
            caption(
                0, "\tWARNING: gzipped file is missing. Using existing unzipped file"
            )
        else:
            caption(0, "\tERROR: Cannot unzip because gzipped file is missing")
        return
    if not xU or os.path.getmtime(gzFile) > os.path.getmtime(uzFile):
        with gz.open(gzFile, mode="rt") as gdata:
            with open(uzFile, "w") as udata:
                udata.write(gdata.read())
    else:
        caption(
            0, "\tNOTE: Using existing unzipped file which is newer than gzipped one"
        )


timestamp = None


def _duration():
    global timestamp
    if timestamp is None:
        timestamp = time.time()

    interval = time.time() - timestamp
    if interval < 10:
        return "{: 2.2f}s".format(interval)
    interval = int(round(interval))
    if interval < 60:
        return "{:>2d}s".format(interval)
    if interval < 3600:
        return "{:>2d}m {:>02d}s".format(interval // 60, interval % 60)
    return "{:>2d}h {:>02d}m {:>02d}s".format(
        interval // 3600, (interval % 3600) // 60, interval % 60
    )


def caption(level, heading, good=None, newLine=True, continuation=False):
    channel = sys.stdout if good is None or good else sys.stderr
    prefix = "" if good is None else "SUCCES " if good else "FAILURE "
    duration = "" if continuation else "{:>11} ".format(_duration())
    reportHeading = "{}{}{}".format(duration, prefix, heading)

    if level == 0:  # non-heading message
        decoration = "" if continuation else "| "
        formattedString = """{}{}""".format(decoration, reportHeading)
    elif level == 1:  # pipeline level
        formattedString = """
##{}##
# {} #
# {} #
# {} #
##{}##
""".format(
            "#" * 90,
            " " * 90,
            "{:<90}".format(reportHeading),
            " " * 90,
            "#" * 90,
        )
    elif level == 2:  # repo level
        formattedString = """
**{}**
* {} *
* {} *
* {} *
**{}**
""".format(
            "*" * 90,
            " " * 90,
            "{:<90}".format(reportHeading),
            " " * 90,
            "*" * 90,
        )
    elif level == 3:  # task level
        formattedString = """
--{}--
- {} -
--{}--
""".format(
            "-" * 90,
            "{:<90}".format(reportHeading),
            "-" * 90,
        )
    elif level == 4:  # caption within task execution
        formattedString = """..{}..
. {} .
..{}..""".format(
            "." * 90,
            "{:<90}".format(reportHeading),
            "." * 90,
        )
    if newLine:
        channel.write(formattedString + "\n")
    else:
        channel.write(formattedString)
    channel.flush()


def mustRun(fileIn, fileOut, force=False):
    xFileIn = None if fileIn is None else os.path.exists(fileIn)
    xFileOut = os.path.exists(fileOut)
    tFileIn = os.path.getmtime(fileIn) if xFileIn else None
    tFileOut = os.path.getmtime(fileOut) if xFileOut else None
    good = True
    work = True
    if fileIn is None:
        if xFileOut:
            caption(0, "\tDestination {} exists".format(fileOut))
            work = False
        else:
            caption(0, "\tDestination {} does not exist".format(fileOut))
            work = True
    elif xFileIn:
        caption(0, "\tSource {} exists".format(fileIn))
        if xFileOut:
            caption(0, "\tDestination {} exists".format(fileOut))
            if tFileOut >= tFileIn:
                caption(0, "\tDestination {} up to date".format(fileOut))
                work = False
            else:
                caption(0, "\tDestination {} is outdated".format(fileOut))
        else:
            caption(0, "\tDestination {} does not exist".format(fileOut))
    else:
        caption(0, "\tSource {} does not exist".format(fileIn))
        if xFileOut:
            caption(0, "\tDestination {} exists".format(fileOut))
            caption(0, "\tDestination {} counts as up to date".format(fileOut))
            work = False
        else:
            caption(0, "\tDestination {} does not exist".format(fileOut))
            caption(
                0, "\tDestination {} cannot be made: source is missing".format(fileOut)
            )
            good = False
            work = False

    if good and force and not work:
        caption(0, 'NOTE: repo seems up to date. Will be run because of "force=True"')
        work = True
    return (good, work or force)


def checkDiffs(thisSave, thisDeliver, only=None):
    def diffFeature(f):
        caption(0, "{:<25} ... ".format(f), newLine=False)
        existingPath = "{}/{}.tf".format(thisDeliver, f)
        newPath = "{}/{}.tf".format(thisSave, f)
        with open(existingPath) as h:
            eLines = (
                h.readlines()
                if f == "otext"
                else (d for d in h.readlines() if not d.startswith("@"))
            )
        with open(newPath) as h:
            nLines = (
                h.readlines()
                if f == "otext"
                else (d for d in h.readlines() if not d.startswith("@"))
            )
        i = 0
        equal = True
        cutOff = 40
        limit = 4
        nUnequal = 0
        for (e, n) in zip_longest(eLines, nLines, fillvalue="<empty>"):
            i += 1
            if e != n:
                if nUnequal == 0:
                    caption(
                        0,
                        "differences{}".format(
                            "" if f == "otext" else " after the metadata"
                        ),
                        continuation=True,
                    )
                shortE = e[0:cutOff] + (" ..." if len(e) > cutOff else "")
                shortN = n[0:cutOff] + (" ..." if len(n) > cutOff else "")
                caption(0, "\tline {:>6} OLD -->{}<--".format(i, shortE.rstrip("\n")))
                caption(0, "\tline {:>6} NEW -->{}<--".format(i, shortN.rstrip("\n")))
                equal = False
                nUnequal += 1
                if nUnequal >= limit:
                    break

        caption(0, "no changes" if equal else "", continuation=True)

    caption(4, "Check differences with previous version")
    existingFiles = glob("{}/*.tf".format(thisDeliver))
    newFiles = glob("{}/*.tf".format(thisSave))
    existingFeatures = {os.path.basename(os.path.splitext(f)[0]) for f in existingFiles}
    newFeatures = {os.path.basename(os.path.splitext(f)[0]) for f in newFiles}

    if only is not None:
        existingFeatures &= only
        newFeatures &= only

    addedOnes = newFeatures - existingFeatures
    deletedOnes = existingFeatures - newFeatures
    commonOnes = newFeatures & existingFeatures

    if addedOnes:
        caption(0, "\t{} features to add".format(len(addedOnes)))
        for f in sorted(addedOnes):
            caption(0, "\t\t{}".format(f))
    else:
        caption(0, "\tno features to add")
    if deletedOnes:
        caption(0, "\t{} features to delete".format(len(deletedOnes)))
        for f in sorted(deletedOnes):
            caption(0, "\t\t{}".format(f))
    else:
        caption(0, "\tno features to delete")

    caption(0, "\t{} features in common".format(len(commonOnes)))
    for f in sorted(commonOnes):
        diffFeature(f)
    caption(0, "Done")


def deliverDataset(thisSave, thisDeliver):
    caption(4, "Deliver data set to {}".format(thisDeliver))
    if os.path.exists(thisDeliver):
        rmtree(thisDeliver)
    copytree(thisSave, thisDeliver)


def deliverFeatures(thisSave, thisDeliver, newFeatures, deleteFeatures=None):
    caption(4, "Deliver features to {}".format(thisDeliver))
    if not os.path.exists(thisDeliver):
        os.makedirs(thisDeliver)
    for feature in newFeatures:
        tempLoc = "{}/{}.tf".format(thisSave, feature)
        deliverLoc = "{}/{}.tf".format(thisDeliver, feature)
        caption(0, "\t{}".format(feature))
        copy(tempLoc, deliverLoc)
    if deleteFeatures is not None:
        caption(4, "Delete features from {}".format(thisDeliver))
        for feature in deleteFeatures:
            caption(0, "\t{} ... ".format(feature), newLine=False)
            deliverLoc = "{}/{}.tf".format(thisDeliver, feature)
            if os.path.exists(deliverLoc):
                os.remove(deliverLoc)
                caption(0, "deleted", continuation=True)
            else:
                caption(0, "was not present", continuation=True)
