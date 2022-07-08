# -*- coding: utf-8 -*-

import codecs
import pygame

pygame.init()
def characterToimage(word, imagename):
    font = pygame.font.Font("msyh.ttc", 200)
    rtext = font.render(word, True, (0, 0, 0), (255, 255, 255))
    pygame.image.save(rtext, "./data/" + imagename + ".png")



if __name__ == "__main__":

    file_path = "./3500-char-new.txt"
    with codecs.open(file_path, "r", "utf-8") as file:
        for line in file.readlines():
            character = line.strip()
            print(character, "has been convertd to image!")
            characterToimage(word=character, imagename=character)

    print("all the characters has been processed!")
    
