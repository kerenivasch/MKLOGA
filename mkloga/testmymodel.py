
import re
import json
import numpy as np
import tensorflow as tf

from classes.keyboard_structure import KeyboardStructure
from classes.characters_placement import CharactersPlacement

random_seed=961
np.random.seed(random_seed)
tf.random.set_seed(random_seed)

#path = "predefined_characters_placements\dvorak_simplified_dir\genetic_config.json"
#path = "carpalx-0.12\keren\\carpalx_config.json"
#path = "predefined_characters_placements\qwerty_dir\genetic_config.json"
#path = "searched_characters_placements\letters_only_dir\genetic_config.json" #abc
#path = "carpalx-0.12\keren\\bzq_config.json"
path = "carpalx-0.12\keren\\my_model_config.json"

with open(path, 'r') as file:
    genetic_config = json.load(file)
initial_characters_placement = CharactersPlacement(characters_set=genetic_config['characters_set'])

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


keyboard_structure = KeyboardStructure(
        name=genetic_config['keyboard_structure']['name'],
        width=genetic_config['keyboard_structure']['width'],
        height=genetic_config['keyboard_structure']['height'],
        buttons=genetic_config['keyboard_structure']['buttons'],
        hands=genetic_config['hands']
    )

bzq = initial_characters_placement.calculate_fitness(
        keyboard_structure,
        build_corpus()
    )

print("bzq: ", bzq)


my_letters = []
my_buttons = [keyboard_structure.buttons[i].id for i in range(len(keyboard_structure.buttons))]
for c in initial_characters_placement.characters_set:
    if(c.button_id is not None):
        my_buttons.remove(c.button_id)
    else:
        my_letters.append(c.character)

my_letters.sort()
number_of_characters = len(my_letters)

model = tf.keras.models.load_model('saved_model/my_model')

keyboard_onehot = np.zeros([1, 26, 26], dtype=int)
for l in range(26):
    for button, character in zip(keyboard_structure.buttons, initial_characters_placement):
        if character == my_letters[l]:
            position = my_buttons.index(button.id)
            keyboard_onehot[0][l][position] = 1
            break

print(my_letters)
print(my_buttons)

prediction = model.predict(keyboard_onehot)
print("my: ", prediction)