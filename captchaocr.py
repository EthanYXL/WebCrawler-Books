import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def remove_bg(img):
    new_image = []
    for i in img.getdata():
        if i[:3][0] in range(80, 131) and i[:3][1] in range(80, 131) and i[:3][2] in range(80, 131):
            new_image.append(i)
        else:
            new_image.append((255, 255, 255))
    img.putdata(new_image)
    return img


def captchocr(crop):
    image = Image.open("captcha/test.png")
    image = image.crop(crop)
    image = remove_bg(image)
    image.save("captcha/captcha.png")
    custom_config = r'-c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    return pytesseract.image_to_string(image, lang="eng", config=custom_config)







