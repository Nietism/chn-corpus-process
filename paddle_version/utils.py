# -*- coding: utf-8 -*-
import os
import random
import pygame
import cv2
import codecs
import time
try:
    import Image
except ImportError:
    from PIL import Image
from PIL import Image, ImageFilter


def getLocation(x):
    if x == 1:
        # mask the upper part
        left_x = 0
        left_y = 0
        right_x = 200
        right_y = 70
        return left_x, left_y, right_x, right_y
    elif x == 2:
        # mask the bottom part
        left_x = 0
        left_y = 120
        right_x = 200
        right_y = 265
        return left_x, left_y, right_x, right_y
    elif x == 3:
        # mask the left part
        left_x = 0
        left_y = 0
        right_x = 100
        right_y = 265
        return left_x, left_y, right_x, right_y
    elif x == 4:
        # mask the central part
        left_x = 0
        left_y = 80
        right_x = 200
        right_y = 140
        return left_x, left_y, right_x, right_y
    else:
        # mask the right part
        left_x = 100
        left_y = 0
        right_x = 200
        right_y = 265
        return left_x, left_y, right_x, right_y


def blur(imagename):
    image = Image.open("./data/" + imagename + ".png")
    num = random.randint(1, 5)
    left_x, left_y, right_x, right_y = getLocation(num)

    left_x += 0
    right_x += 0
    crop_image = image.crop((left_x, left_y, right_x, right_y))
    blured_image = crop_image.filter(ImageFilter.GaussianBlur(radius=10))
    image.paste(blured_image, (left_x, left_y, right_x, right_y))
    image.save("blurred.png")

