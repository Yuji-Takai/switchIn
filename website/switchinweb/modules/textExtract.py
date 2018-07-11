from wand.image import Image
from PIL import Image as PI
import pyocr
import pyocr.builders
import io
import os
import cv2
import numpy as np
from .patternMatch import kmp, approximate_matching, recoverCorruption
from .companyKeys import *
from .geico import geicoFormat

company_list = ["GEICO", "AAA", "StateFarm", "AllState", "LibertyMutual"]

""" Converts the pdf file into strings
:param filename:    name of the pdf file
:returns:           list of strings
"""
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


""" Converts the img file into strings
:param img_path:    path to the image file
:returns:           string representation of the content of the image
"""
def img_to_text(img_path):
    tool = pyocr.get_available_tools()[0]
    lang = tool.get_available_languages()[0]
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    cv2.imwrite("thres.png", img)
    result = tool.image_to_string(PI.open("thres.png"), lang=lang, builder=pyocr.builders.TextBuilder())
    os.remove("thres.png")
    return result

""" Searches the insurance company name
:param text:        text from which the company name is searched
:returns: company name found or None
"""
def searchCompanyName(text):
    for company in company_list:
        indList = kmp(company, text)
        if len(indList) > 0:
            return company
    return None

""" runs the appropriate text search for the specified company name
:param filename:    path to the file to be converted to text
:returns:           dictionary containing the
"""
def extractInfo(filename):
    extention = filename.split(".")
    extention = extention[len(extention) - 1].lower()
    text = pdf_to_text(filename) if extention == "pdf" else img_to_text(filename)
    company = searchCompanyName(text)
    words = recoverCorruption(text)
    if (company == "GEICO"):
        for key in GEICO:
            GEICO[key] = approximate_matching(words, key)
        GEICO.update({"Company Name": company})
        return geicoFormat(GEICO)
    elif (company == "AAA"):
        for key in AAA:
            AAA[key] = approximate_matching(words, key)
        return AAA.update({"Company Name": company})
    elif (company == "StateFarm"):
        for key in STATE_FARM:
            STATE_FARM[key] = approximate_matching(words, key)
        return STATE_FARM.update({"Company Name": company})
    elif (company == "AllState"):
        for key in ALL_STATE:
            ALL_STATE[key] = approximate_matching(words, key)
        return ALL_STATE.update({"Company Name": company})
    elif (company == "LibertyMutual"):
        for key in LIBERTY_MUTUAL:
            LIBERTY_MUTUAL[key] = approximate_matching(words, key)
        return LIBERTY_MUTUAL.update({"Company Name": company})
    else:
        for key in GENERAL:
            GENERAL[key] = approximate_matching(words, key)
        return GENERAL.update({"Company Name": company})

