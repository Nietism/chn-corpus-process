# -*- coding: utf-8 -*-

import os
import re
import codecs

from requests_html import HTMLSession

def get_single_char_info_from_hanzicraft(character):
    session = HTMLSession()
    url = "https://hanzicraft.com/character/" + character
    r = session.get(url)

    span_start = r.html.text.find("Decomposition:")
    span_end = r.html.text.find("Pinyin & Meaning:")
    text_span = r.html.text[span_start: span_end]

    flag_pos_1 = text_span.find("Once :")
    flag_pos_2 = text_span.find("Radical :")
    flag_pos_3 = text_span.find("Graphical :")

    once_decomposition = text_span[flag_pos_1: flag_pos_2].strip()
    radical_decomposition = text_span[flag_pos_2: flag_pos_3].strip()
    graphical_decomposition = text_span[flag_pos_3: ].strip()

    once_decomposition = once_decomposition[once_decomposition.find("=> ") + 3:]
    radical_decomposition = radical_decomposition[radical_decomposition.find("=> ") + 3:]
    graphical_decomposition = graphical_decomposition[graphical_decomposition.find("=> ") + 3:]

    # delete the semantic information in radical decomposition
    radical_list = list(radical_decomposition.split(","))
    processed_radical_list = []
    for item in radical_list:
        new_item = item[: item.find("(")].strip()
        processed_radical_list.append(new_item)

    radical_decomposition = ", ".join(processed_radical_list)

    return once_decomposition, radical_decomposition, graphical_decomposition

if __name__ == "__main__":

    data_lines = []
    with codecs.open("./3500-char-new.txt", "r", "utf-8") as file:
        data_lines = file.readlines()

    with codecs.open("./3500-char-decomposition.txt", "w", "utf-8") as file:
        for line in data_lines:
            char = line.strip()
            once, radical, graphical = get_single_char_info_from_hanzicraft(char)
            line_to_write = char + "\t" + once + "\t" + radical + "\t" + graphical
            file.write(line_to_write + "\n")

    print("decomposition information has been written to file!")