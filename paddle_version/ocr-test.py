# -*- coding: utf-8 -*-

import codecs
from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
from utils import getLocation, blur

ocr = PaddleOCR(use_angle_cls=True, lang="ch")


def check_if_blurred_res_right(query_char):

    blur(query_char)
    blur_result = ocr.ocr("./blurred.png", cls=True)
    blur_txts = [line[1][0] for line in blur_result]
    # print("The recognized result by ocr is:", blur_txts)

    if query_char not in blur_txts:
        print(query_char, blur_txts)



if __name__ == "__main__":

    mismatch_list = []
    file_path = "./3500-char-new.txt"

    with codecs.open(file_path, "r", "utf-8") as file:
        for line in file.readlines():
            character = line.strip()
            check_if_blurred_res_right(character)

    print("all the characters has been processed!")



    
