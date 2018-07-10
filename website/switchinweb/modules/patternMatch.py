""" Knuth–Morris–Pratt (KMP) algorithm
:param pattern:     pattern to be searched in the text
:param text:        text to search the pattern in
:returns:           list containing all of the index where match was found
"""
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

""" builds the failure table for KMP algorithm
:param pattern:     pattern to build the failure table on
:returns:           failure table
"""
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

""" algorithm for approximate pattern matching
:param text:    text from which the value for the key is found
:param key:     string searched in the text
:returns:       value for the key searched
"""
def approximate_matching(words, key):
    # converting the text into a string of length of each word
    text_of_length = []
    for word in words:
        text_of_length.append(len(word))
    # converting the key into a string of length of each word
    key_len_pattern = []
    key_split = key.split()
    for word in key_split:
        key_len_pattern.append(len(word))
    # approximate pattern match
    total_len = len(key) - len(key_split) + 1
    indList = kmp(key_len_pattern, text_of_length)
    if len(indList) > 0:
        diffList = []
        for n in range(len(indList)):
            diff = 0
            for m in range(len(key_split)):
                diff = diff + hammingDistance(words[indList[n] + m], key_split[m])
            diffList.append(diff)
        if min(diffList) / total_len <= 0.35:
            return words[indList[diffList.index(min(diffList))] + len(key_split)]
    return ""

""" calculates the hamming distance between two strings
:param str1:    string 1
:param str2:    string 2
: returns:      number of mismatch between the two strings
"""
def hammingDistance(str1, str2):
    if (len(str1) != len(str2)):
        return len(str1) if len(str1) < len(str2) else len(str2)
    else:
        i = 0
        count = 0
        for i in range(len(str1)):
            if str1[i].lower() != str2[i].lower():
                count = count + 1
        return count

""" recovers some of the recognition errors of the OCR
:param text:    string of the text
:returns:       the original text split into list of words
"""
def recoverCorruption(text):
    words = text.split()
    i = 0
    while (i < len(words) - 1):
        # recover something that should be 0 but was recognized as O
        if (i > 0 and words[i] == 'O' and (words[i - 1][len(words[i - 1]) - 1].isdigit() or words[i][len(words[i]) - 1] == '-') and (words[i + 1][0].isdigit() or words[i + 1][0] == '-')):
            i = i - 1
            words[i] = words[i] + '0'
            temp = words[0:i + 1]
            temp2 = words[i + 2:len(words)]
            words = temp + temp2

        # remove colons
        ind = words[i].find(":")
        if (ind != -1):
            temp = words[0:i + 1]
            temp2 = words[i + 1:len(words)]
            temp[i] = words[i][0:ind]
            if (words[i][ind + 1: len(words[i])]):
                temp.append(words[i][ind + 1: len(words[i])])
            words = temp + temp2

        # recover numbers that have spaces between them
        j = 1
        while (i + j < len(words) and words[i].isdigit()
            and words[i + j].isdigit()):
            words[i] = words[i] + words[i + j]
            j = j + 1
        temp = words[0:i + 1]
        temp2 = words[i + j: len(words)]
        words = temp + temp2

        # recover numbers with comma and date
        while (i < len(words) - 1 and (words[i][len(words[i]) - 1].isdigit()
            and words[i + 1][0] == ',')
            or (words[i][len(words[i]) - 1] == ','
                and words[i + 1][0].isdigit())
            or (words[i][len(words[i]) - 1].isdigit()
                and words[i + 1][0] == '-')
            or (words[i][len(words[i]) - 1] == '-'
                and words[i + 1][0].isdigit())):
            words[i] = words[i] + words[i + 1]
            temp = words[0:i + 1]
            temp2 = words[i + 2:len(words)]
            words = temp + temp2

        # recover date in the format "XX-X" "X-XX" -> "XX-XX-XX"
        if (i > 0 and (not words[i].isdigit() and words[i][0].isdigit()) and (not words[i - 1].isdigit() and words[i - 1][len(words[i - 1]) - 1].isdigit())):
            i = i - 1
            words[i] = words[i] + words[i + 1]
            temp = words[0:i + 1]
            temp2 = words[i + 2:len(words)]
            words = temp + temp2

        i = i + 1
    return words