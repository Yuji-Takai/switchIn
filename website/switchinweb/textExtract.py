from wand.image import Image
from PIL import Image as PI
import pyocr
import pyocr.builders
import io

company_list = ["GEICO", "AAA", "StateFarm", "AllState", "LibertyMutual"]

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


def pdf_to_text(filename):
    tool = pyocr.get_available_tools()[0]
    lang = tool.get_available_languages()[0]
    req_image = []
    final_text = []
    image_pdf = Image(filename=filename, resolution=500, format='pdf')
    image_jpeg = image_pdf.convert('jpeg')

    for img in image_jpeg.sequence:
        img_page = Image(image=img)
        req_image.append(img_page.make_blob('jpeg'))

    for img in req_image:
        txt = tool.image_to_string(
            PI.open(io.BytesIO(img)),
            lang=lang,
            builder=pyocr.builders.TextBuilder()
        )
        final_text.append(txt)
    return final_text[0]

def approximate_matching(text, info):
    words = recoverNumCorruption(text)

    # converting the text into a string of length of each word
    text_of_length = []
    for word in words:
        text_of_length.append(len(word))

    for key in info.keys():
        key_len_pattern = []
        key_split = key.split()
        total_len = len(key) - len(key_split) + 1
        for word in key_split:
            key_len_pattern.append(len(word))
        indList = kmp(key_len_pattern, text_of_length)
        if len(indList) > 0:
            diffList = []
            for n in range(len(indList)):
                diff = 0
                if (indList[n] + len(key_split) < len(words)):
                    for m in range(len(key_split)):
                        diff = diff + hammingDistance(words[indList[n] + m], key_split[m])
                else:
                    diff = total_len
                diffList.append(diff)
            if min(diffList) / total_len <= 0.35:
                info[key] = words[indList[diffList.index(min(diffList))] + len(key_split)]
    return info

def hammingDistance(str1, str2):
    if (len(str1) != len(str2)):
        return len(str1) if len(str1) < len(str2) else len(str2)
    else:
        i = 0
        count = 0
        for i in range(len(str1)):
            if str1[i] != str2[i]:
                count = count + 1
        return count

def recoverNumCorruption(text):
    # recover numbers that have spaces between them
    words = text.split()
    words2 = []

    i = 1
    while (i < len(words) - 1):
        if (words[i] == 'O' and (words[i - 1].isdigit() or words[i - 1] == '-') and (words[i + 1].isdigit() or words[i + 1] == '-')):
            words[i] = '0'
        i = i + 1

    i = 0
    while (i < len(words) - 1):
        j = 1
        while (i + j < len(words) and words[i].isdigit() and words[i + j].isdigit()):
            words[i] = words[i] + words[i + j]
            j = j + 1
        words2.append(words[i])
        i = i + j

    # recover locations where there should be a space after a colon
    words = words2
    words2 = []
    for word in words:
        ind = word.find(':')
        if (ind == len(word) - 1):
            words2.append(word[0:len(word) - 1])
        elif (ind != -1):
            words2.append(word[0:ind])
            words2.append(word[ind + 1: len(word)])
        else:
            words2.append(word)

    # recover dates that are separated
    words = words2
    words2 = []
    i = 0
    while (i < len(words) - 4):
        if (words[i].isdigit() and words[i + 1] == '-' and words[i + 2].isdigit() and words[i + 3] == '-' and words[i + 4].isdigit()):
            words2.append(words[i] + words[i + 1] + words[i + 2] + words[i + 3] + words[i + 4])
            i = i + 5
        else:
            words2.append(words[i])
            i = i + 1
    return words2

def discoverCompanyName(text, info):
    companyName = {'Company Name': ''}
    for company in company_list:
        indList = kmp(company, text)
        if len(indList) > 0:
            companyName['Company Name'] = company
            info.update(companyName)
            return info
    info.update(companyName)
    return info

def extractInfo(filename):
    text = pdf_to_text(filename)
    info = {"Policy Number": "", "Effective Date": "", "Expiration Date": "", "Registered State": "", "Vehicle Year": "", "Make": "", "Model": "", "VIN": "", "Property Damage Liability": "", "Bodily Injury Liability": "", "Comprehensive": "", "Collision": "", "Personal Injury Protection": "", "Uninsured &Underinsured Motorists": ""}
    info = approximate_matching(text, info)
    info = discoverCompanyName(text, info)
    if len(info["Effective Date"]) != 8:
        info["Effective Date"] = ""
    if len(info["Expiration Date"]) != 8:
        info["Expiration Date"] = ""
    return info





