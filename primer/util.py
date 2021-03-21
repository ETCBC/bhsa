def getTfVerses(A, results, focus):
    api = A.api
    L = api.L
    F = api.F

    verses = set()
    words = set()

    for result in results:
        for pos in focus:
            focusNode = result[pos]
            if focusNode is None:
                continue
            verse = L.u(focusNode, otype="verse")[0]
            verses.add(verse)

            if F.otype.v(focusNode) == "word":
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
