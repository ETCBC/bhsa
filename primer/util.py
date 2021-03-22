MQL_RESULTS = {
    1: {
        "file": "2017_q4439_text_Bas_Meeuse",
        "results": 8,
        "verses": 8,
        "words": 42,
    },
    2: {
        "file": "2017_q4440_text_Bas_Meeuse",
        "results": 156,
        "verses": 136,
        "words": 294,
    },
    "2a": {
        "file": "2017_q4467_text_Dirk_Roorda",
        "results": 160,
        "verses": 138,
        "words": 300,
    },
    3: {
        "file": "2017_q4441_text_Bas_Meeuse",
        "results": 308,
        "verses": 150,
        "words": 685,
    },
    4: {
        "file": "2017_q53_text_Wido_van Peursen",
        "results": 65,
        "verses": 51,
        "words": 315,
    },
    5: {
        "file": "2017_q494_text_Oliver_Glanz",
        "results": 23,
        "verses": 21,
        "words": 44,
    },
    6: {
        "file": "2017_q4442_text_Bas_Meeuse",
        "results": 10,
        "verses": 10,
        "words": 121,
    },
    7: {
        "file": "2017_q4334_text_Reinoud_Oosting",
        "results": 62,
        "verses": 61,
        "words": 348,
    },
    8: {
        "file": "2017_q523_text_Reinoud_Oosting",
        "results": 16,
        "verses": 16,
        "words": 32,
    },
    9: {
        "file": "2017_q491_text_Oliver_Glanz",
        "results": 344,
        "verses": 101,
        "words": 356,
    },
    "10a": {
        "file": "2017_q4416_text_Bas_Meeuse",
        "results": 232,
        "verses": 190,
        "words": 458,
    },
    "10b": {
        "file": "2017_q4437_text_Bas_Meeuse",
        "results": 2087,
        "verses": 675,
        "words": 5573,
    },
    "10b1": {
        "file": "2017_q4469_text_Dirk_Roorda",
        "results": 217,
        "verses": 103,
        "words": 677,
    },
    "10b2": {
        "file": "2017_q4470_text_Dirk_Roorda",
        "results": 63,
        "verses": 63,
        "words": 406,
    },
    "10bm": {
        "file": "2017_q4471_text_Dirk_Roorda",
        "results": 8,
        "verses": 4,
        "words": 8,
    },
}


def getTfVerses(A, results, focus):
    api = A.api
    L = api.L
    F = api.F
    T = api.T

    verses = set()
    words = set()

    for result in results:
        for pos in focus:
            focusNode = result[pos]
            if focusNode is None:
                continue
            if focusNode == -1:
                continue
            focusType = F.otype.v(focusNode)
            verse = T.sectionTuple(focusNode, fillup=True)[-1]
            verses.add(verse)
            verse = T.sectionTuple(focusNode, lastSlot=True, fillup=True)[-1]
            verses.add(verse)

            if focusType == "word":
                words.add(focusNode)
            else:
                for word in L.d(focusNode, otype="word"):
                    words.add(word)

    verses = sorted(verses)
    words = sorted(words)

    print(f"{len(verses):>3} verses")
    print(f"{len(words):>3} words")
    return (verses, words)


def getShebanqData(A, info, example):
    api = A.api
    T = api.T

    metadata = info[example]
    fileName = f"data/{metadata['file']}.csv"
    nResults = metadata["results"]
    nVerses = metadata["verses"]
    nWords = metadata["words"]

    verses = set()
    words = set()

    with open(fileName) as fh:
        next(fh)
        for line in fh:
            fields = line.rstrip("\n").split(",")
            verses.add(
                T.nodeFromSection(
                    (fields[0], int(fields[1]), int(fields[2])), lang="la"
                )
            )
            words.add(int(fields[3]))

    verses = sorted(verses)
    words = sorted(words)

    if len(words) != nWords:
        print(f"!!Words: found {len(words)}, expected {nWords}")
    if len(verses) != nVerses:
        print(f"!!Verses: found {len(verses)}, expected {nVerses}")

    print(f"{nResults} results in {nVerses} verses with {nWords} words")

    return (verses, words)


def compareResults(A, leftVerses, leftWords, rightVerses, rightWords):
    api = A.api
    T = api.T
    F = api.F

    equalVerses = True

    for (i, lv) in enumerate(leftVerses):
        leftVerse = T.sectionFromNode(lv)
        if i < len(rightVerses):
            rv = rightVerses[i]
            if lv == rv:
                continue
            rightVerse = T.sectionFromNode(rv)
            print(f"DIFFERENCE:\n{leftVerse}\n{rightVerse}")
            equalVerses = False
            break
        else:
            print(f"DIFFERENCE:\n{leftVerse}\nno verses left")
            equalVerses = False
            break
    if equalVerses and len(leftVerses) < len(rightVerses):
        rv = rightVerses[len(leftVerses)]
        rightVerse = T.sectionFromNode(rv)
        print(f"DIFFERENCE:\nno verses left\n{rightVerse}")
        equalVerses = False
    if equalVerses:
        print("VERSES EQUAL")

    equalWords = True

    for (i, lw) in enumerate(leftWords):
        leftWord = F.g_word.v(lw)
        if i < len(rightWords):
            rw = rightWords[i]
            if lw == rw:
                continue
            rightWord = F.g_word.v(rw)
            print(f"DIFFERENCE:\n{lw} = {leftWord}\n{rw} = {rightWord}")
            equalWords = False
            break
        else:
            print(f"DIFFERENCE:\n{lw} = {leftWord}\nno verses left")
            equalWords = False
            break
    if equalWords and len(leftWords) < len(rightWords):
        rw = rightWords[len(leftWords)]
        rightWord = F.g_word.v(rw)
        print(f"DIFFERENCE:\nno verses left\n{rightWord}")
        equalWords = False
    if equalWords:
        print("WORDS EQUAL")
    return None if equalVerses and equalWords else -1
