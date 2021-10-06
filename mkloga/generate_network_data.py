
import os
import re
import copy
import json
import tensorflow as tf
import numpy as np
import time
from classes.keyboard_structure import KeyboardStructure
from classes.characters_placement import CharactersPlacement

start_time = time.time()

random_seed=961
np.random.seed(random_seed)
tf.random.set_seed(random_seed)

punct = True
number_of_characters_placements = 10000

def _preprocess_line(line):
    _regex = re.compile('[^%s]' % ''.join(sorted(set(initial_characters_placement))))
    return _regex.sub('', line)

def build_corpus():
    corpus_path = "./data_dir/TED2013 v1.1.txt"
    maximum_line_length = 500
    searching_corpus_size = 10000

    corpus = open(corpus_path, 'r', encoding='utf-8').read().split('\n')
    corpus = [line for line in corpus if len(line) <= maximum_line_length]

    rng = np.random.RandomState(random_seed)
    rng.shuffle(corpus)

    searching_corpus = [_preprocess_line(line) for line in corpus[:searching_corpus_size]]

    if len(searching_corpus) < searching_corpus_size:
        print('Searching corpus size didn\'t reach %s, its current size is %s' %
                    (searching_corpus_size, len(searching_corpus)))

    searching_corpus_dict = dict()
    for line in searching_corpus:
        for char in line.strip():
            try:
                searching_corpus_dict[char] += 1
            except:
                searching_corpus_dict[char] = 1

    return searching_corpus_dict

def buildCarpalxInput(keyboard):
    carpalx_file_name = "carpalx-0.12\keren\keren.conf"
    with open(carpalx_file_name, 'w') as carpalx_file:
        carpalx_file.write(
            "<keyboard>\n<row 1>\nkeys    = `~ 1! 2@ 3\\# 4$ 5% 6^ 7& 8* 9( 0) -_ =+\nfingers =  0  1  1   2  3  3  3  6 7   7  8  9  9\n</row>\n<row 2>\nkeys    =")

        letters = 0
        for button, character in zip(keyboard_structure.buttons, keyboard):
            if character in my_letters:
                letters += 1
                carpalx_file.write(" " + character)

                if letters == 9:
                    carpalx_file.write(" ;: [{ ]} \\|\nfingers = 0 1 2 3 3 6 6 7 8 9  9  9  9\n</row>\n<row 3>\nkeys    =")

                if letters == 19:
                    carpalx_file.write(" '\"\nfingers = 0 1 2 3 3 6 6 7 8  9  9\n</row>\n<row 4>\nkeys    =")

                if letters == 26:
                    carpalx_file.write(" ,< .> /?\nfingers = 0 1 2 3 3 6 6  7  8  9\n</row>\n</keyboard>")
                    break

        carpalx_file.close()

def buildCarpalxInput_punct(keyboard):
    punct_map = {"-":"-_", "+":"=+", "{":"[{", "}":"]}", ";":";:", "'":"'\"", ",":",<", ".":".>", "?":"/?"}

    carpalx_file_name = "carpalx-0.12\keren\keren.conf"
    with open(carpalx_file_name, 'w') as carpalx_file:
        carpalx_file.write("<keyboard>\n<row 1>\nkeys    = `~ 1! 2@ 3\\# 4$ 5% 6^ 7& 8* 9( 0)")

        letters = 0
        for button, character in zip(keyboard_structure.buttons, keyboard):
            if character in my_letters:
                letters += 1

                if character in punct_map.keys():
                    carpalx_file.write(" " + punct_map[character])
                elif character>='a' and character<='z':
                    carpalx_file.write(" " + character)
                else:
                    print("wrong character: ", character)
                    exit(1)

                if letters == 2:
                    carpalx_file.write("\nfingers =  0  1  1   2  3  3  3  6 7   7  8  9  9\n</row>\n<row 2>\nkeys    =")

                if letters == 14:
                    carpalx_file.write(" \\|\nfingers = 0 1 2 3 3 6 6 7 8 9  9  9  9\n</row>\n<row 3>\nkeys    =")

                if letters == 25:
                    carpalx_file.write(" \nfingers = 0 1 2 3 3 6 6 7 8  9  9\n</row>\n<row 4>\nkeys    =")

                if letters == 35:
                    carpalx_file.write(" \nfingers = 0 1 2 3 3 6 6  7  8  9\n</row>\n</keyboard>")
                    break

        carpalx_file.close()


#open genetic_config
if(punct):
    path_str = "and_punctuations"
else:
    path_str = "only"

genetic_config_path = "searched_characters_placements\letters_" + path_str + "_dir\genetic_config.json"
with open(genetic_config_path, 'r') as file:
    genetic_config = json.load(file)
initial_characters_placement = CharactersPlacement(characters_set=genetic_config['characters_set'])
keyboard_structure = KeyboardStructure(
    name=genetic_config['keyboard_structure']['name'],
    width=genetic_config['keyboard_structure']['width'],
    height=genetic_config['keyboard_structure']['height'],
    buttons=genetic_config['keyboard_structure']['buttons'],
    hands=genetic_config['hands']
)

#my buttons ids
my_letters = []
my_buttons = [keyboard_structure.buttons[i].id for i in range(len(keyboard_structure.buttons))]
for c in initial_characters_placement.characters_set:
    if(c.button_id is not None):
        my_buttons.remove(c.button_id)
    else:
        my_letters.append(c.character)
number_of_characters = len(my_letters)

print("generating labeled keyboards...")
searching_corpus_dict = build_corpus()
characters_placements = list()
labels = np.zeros([number_of_characters_placements], dtype=float)
for i in range(number_of_characters_placements):
    characters_placements.append(copy.deepcopy(initial_characters_placement))
    characters_placements[-1].randomize()

    if(punct):
        buildCarpalxInput_punct(characters_placements[-1])
    else:
        buildCarpalxInput(characters_placements[-1])
    my_cmd = "perl carpalx-0.12/keren/carpalx_keren -conf carpalx-0.12/etc/tutorial-00.conf"
    my_cmd_output = os.popen(my_cmd)
    for line in my_cmd_output:
        labels[i] = float(line.rstrip())

#one-hot from bzq
features = np.zeros([number_of_characters_placements,number_of_characters,number_of_characters], dtype=int)
for cp in range(len(characters_placements)):
    for l in range(len(my_letters)):
        for button, character in zip(keyboard_structure.buttons, characters_placements[cp]):
            if character == my_letters[l]:
                #if (button.id==22):
                #    print(cp)
                #    for button, character in zip(keyboard_structure.buttons, characters_placements[cp]):
                #        print(button.id, character)
                #    exit()
                position = my_buttons.index(button.id)
                features[cp][l][position] = 1
                break

#qwerty
#qpath = "predefined_characters_placements\qwerty_dir\genetic_config.json"
#with open(qpath, 'r') as file:
#    qgenetic_config = json.load(file)
#qwerty_placement = CharactersPlacement(characters_set=qgenetic_config['characters_set'])
#qwerty_onehot = np.zeros([1,number_of_characters,number_of_characters], dtype=int)
#for l in range(len(my_letters)):
#    for button, character in zip(keyboard_structure.buttons, qwerty_placement):
#        if character == my_letters[l]:
#            position = my_buttons.index(button.id)
#            qwerty_onehot[0][l][position] = 1
#            break

#qwerty_placement.calculate_fitness(keyboard_structure, searching_corpus_dict)
#qwerty_label = qwerty_placement.fitness

#save generated data
path_str = ""
if(punct):
    path_str = "_punct"

data_file_path = "carpalx-0.12\keren\data" + path_str + ".txt"
with open(data_file_path, 'w') as data_file:
    for f in range(len(features)):
        for i in range(len(my_letters)):
            for j in range(len(my_letters)):
                data_file.write(str(features[f][i][j]) + " ")
        data_file.write(str(labels[f]) + "\n")

data_file.close()

print("time: ", time.time() - start_time)


