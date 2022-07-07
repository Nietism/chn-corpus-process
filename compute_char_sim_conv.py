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
import torch.nn.functional as F
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
            Y[i, j] = (X[i: i + h, j: j + w] * K).sum()
    return Y

laplacian_kernel = torch.tensor([[0, 1, 0], [1, -4, 1], [0, 1, 0]]).to(device)

def conv_feature_extract(input_tensor):
    # input_tensor of shape [c, h, w]
    conv1_res = cross_correlation(input_tensor[0, :, :], laplacian_kernel).to(device)
    conv1_res = F.max_pool2d(conv1_res.unsqueeze(0), 2).squeeze(0)
    conv2_res = cross_correlation(torch.tanh(conv1_res), laplacian_kernel).to(device)
    conv2_res = F.max_pool2d(conv2_res.unsqueeze(0), 2).squeeze(0)
    return conv2_res

def my_min_max_scaler(input_tensor):
    min_in = torch.min(input_tensor)
    max_in = torch.max(input_tensor)
    return (input_tensor - min_in) / max_in



if __name__ == "__main__":

    char2id, id2char = get_dict_from_lib(filepath="./3500-char-new.txt")

    assert len(char2id) == len(id2char)
    query_char = "泰"
    query_char_data = get_tensor_by_char(query_char).permute(2, 1, 0).to(device) # of shape [3, 200, 264]

    query_res = torch.zeros(len(char2id))
    query_conv_res = conv_feature_extract(query_char_data)
    query_conv_res = query_conv_res.flatten()
    # local_left_res = torch.zeros(len(char2id))
    # local_right_res = torch.zeros(len(char2id))
    # local_upper_res = torch.zeros(len(char2id))
    # local_bottom_res = torch.zeros(len(char2id))
    # local_central_res = torch.zeros(len(char2id))

    for char, id in char2id.items():
        if char != query_char:
            key_char_data = get_tensor_by_char(char).permute(2, 1, 0).to(device) # of shape [3, 200, 264]
            key_conv_res = conv_feature_extract(key_char_data)
            key_conv_res = key_conv_res.flatten()
            query_res[id] = F.pairwise_distance(query_conv_res, key_conv_res)
            # local_left_res[id] = cross_correlation(query_char_data[2, :100, :], key_char_data[2, :100, :])
            # local_right_res[id] = cross_correlation(query_char_data[2, 100:, :], key_char_data[2, 100:, :])
            # local_upper_res[id] = cross_correlation(query_char_data[2, :, :150], key_char_data[2, :, :150])
            # local_bottom_res[id] = cross_correlation(query_char_data[2, :, 120:], key_char_data[2, :, 120:])
            # local_central_res[id] = cross_correlation(query_char_data[2, :, 80:140], key_char_data[2, :, 80:140])
            # query_res[id] = cross_correlation(query_char_data, key_char_data)
        else:
            continue

    # local_left_res = my_min_max_scaler(local_left_res)
    # local_right_res = my_min_max_scaler(local_right_res)
    # local_upper_res = my_min_max_scaler(local_upper_res)
    # local_bottom_res = my_min_max_scaler(local_bottom_res)
    # local_central_res = my_min_max_scaler(local_central_res)
    # query_res = local_left_res + local_right_res + local_upper_res + local_bottom_res + local_central_res
    # query_res = local_upper_res
    sim_char_ids = query_res.topk(5)[-1].tolist()
    for id in sim_char_ids:
        print(id2char[id])
