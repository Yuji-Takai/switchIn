import Image
import pytesseract
#print image_to_string(Image.open('.png'))
print (pytesseract.image_to_string(Image.open('AllstateDeclarationPage2.jpg'), lang='eng'))
