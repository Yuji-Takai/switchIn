from wand.image import Image
from PIL import Image as PI
import pyocr
import pyocr.builders
import io
import kmp

tool = pyocr.get_available_tools()[0]
lang = tool.get_available_languages()[0]
# langs = tool.get_available_languages()
# print("Available languages: %s" % ", ".join(langs))

req_image = []
final_text = []
image_pdf = Image(filename="GeicoDP.pdf", resolution=300)
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

# print(final_text)

coverages = {"Property Damage Liability": "", "Comprehensive": "", "Collision": "", "Personal Injury Protection": ""}

for key in coverages.keys():
    indList = kmp.kmp(key, final_text[0])
    num = "$"
    if len(indList) > 0:
        for ind in indList:
            i = ind + len(key) + 1
            if final_text[0][i] == "$":
                i = i + 1
                while final_text[0][i].isdigit() or final_text[0][i] == ',':
                    num = num + final_text[0][i]
                    i = i + 1
                coverages[key] = num
            
print(coverages)
    
