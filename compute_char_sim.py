# -*- coding: utf-8 -*-
import os
import random
import codecs
import time

import cv2
from PIL import Image
import pytesseract
from PIL import Image, ImageFilter

import torch
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt

device = "cuda:0"

# import pygame
# pygame.init()
# def characterToimage(word, imagename):
#     font = pygame.font.Font("msyh.ttc", 200)
#     rtext = font.render(word, True, (0, 0, 0), (255, 255, 255))
#     pygame.image.save(rtext, "./chn-char-lib/" + imagename + ".png")

def get_tensor_by_char(character):
    img_path = "./chn-char-lib/" + character + ".png"
    img = np.array(Image.open(img_path))
    img_data = torch.Tensor(img).to(device) # [w, h, channel]
    return img_data

def get_dict_from_lib(filepath):
    char2id = {}
    id2char = {}
    char_ids = 0
    with codecs.open(filepath, "r", "utf-8") as file:
        char_ids = 0
        for line in file.readlines():
            char = line.strip()
            char2id.update({char: char_ids})
            id2char.update({char_ids: char})
            char_ids += 1
    return char2id, id2char


def cross_correlation(X, K): 
    h, w = K.shape
    Y = torch.zeros((X.shape[0] - h + 1, X.shape[1] - w + 1))
    for i in range(Y.shape[0]):
        for j in range(Y.shape[1]):
            Y[i, j] = (X[i:i + h, j:j + w] * K).sum()
    return Y

def my_min_max_scaler(input_tensor):
    min_in = torch.min(input_tensor)
    max_in = torch.max(input_tensor)
    return (input_tensor - min_in) / max_in



if __name__ == "__main__":

    char2id, id2char = get_dict_from_lib(filepath="./3500-char-new.txt")

    assert len(char2id) == len(id2char)
    query_char = "卓"
    query_char_data = get_tensor_by_char(query_char).permute(2, 1, 0)[0, :, :] # [h, w] of the 1st channel
    query_res = torch.zeros(len(char2id))

    for char, id in char2id.items():
        if char != query_char:
            key_char_data = get_tensor_by_char(char).permute(2, 1, 0)[0, :, :].to(device)
            # TODO(lium, 27/06)
            query_res[id] = cross_correlation(query_char_data, key_char_data)
        else:
            continue

    query_res = my_min_max_scaler(query_res)
    sim_char_ids = query_res.topk(5)[-1].tolist()
    for id in sim_char_ids:
        print(id2char[id])
