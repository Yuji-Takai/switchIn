def kmp(pattern, text):
    if (pattern == None or len(pattern) == 0):
        raise ValueError("Cannot match an empty pattern with a text")
    if (text == None or len(text) == 0):
        raise ValueError("Cannot match a pattern with an empty text")
    indList = []
    if (len(pattern) > len(text)):
        return indList
    failureTable = buildFailureTable(pattern)
    i = 0
    j = 0
    while (i <= len(text) - len(pattern)):
        while (j < len(pattern) and text[i + j] == pattern[j]):
            j = j + 1
        if j == 0:
            i = i + 1
        else:
            if j == len(pattern):
                indList.append(i)
            nextAlignment = failureTable[j - 1]
            i = i + j - nextAlignment
            j = nextAlignment
    return indList

def buildFailureTable(pattern):
    failureTable = [0]
    i = 0
    j = 1
    while (j < len(pattern)):
        if pattern[i] == pattern[j]:
            i = i + 1
            failureTable.append(i)
            j = j + 1
        else :
            if i == 0:
                failureTable.append(0)
                j = j + 1
            else :
                i = failureTable[i - 1]

    return failureTable