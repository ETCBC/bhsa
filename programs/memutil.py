import psutil

process = psutil.Process()
previousUsage = 0


def showMemBytes(label, n):
    print(f"{label} {n / 1024 / 1024 / 1024:>5.2f} GB")


def memUsage():
    global previousUsage
    usageBytes = process.memory_info().rss
    showMemBytes("Current:", usageBytes)
    deltaBytes = usageBytes - previousUsage
    showMemBytes("Delta:  ", deltaBytes)
    previousUsage = usageBytes
