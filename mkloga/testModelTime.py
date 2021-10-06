
import copy
import json
import time
import numpy as np
import tensorflow as tf
from classes.keyboard_structure import KeyboardStructure
from classes.characters_placement import CharactersPlacement

path = "searched_characters_placements\letters_only_dir\genetic_config.json"
with open(path, 'r') as file:
    genetic_config = json.load(file)
initial_characters_placement = CharactersPlacement(characters_set=genetic_config['characters_set'])
keyboard_structure = KeyboardStructure(
        name=genetic_config['keyboard_structure']['name'],
        width=genetic_config['keyboard_structure']['width'],
        height=genetic_config['keyboard_structure']['height'],
        buttons=genetic_config['keyboard_structure']['buttons'],
        hands=genetic_config['hands']
    )
my_letters = []
my_buttons = [keyboard_structure.buttons[i].id for i in range(len(keyboard_structure.buttons))]
for c in initial_characters_placement.characters_set:
    if(c.button_id is not None):
        my_buttons.remove(c.button_id)
    else:
        my_letters.append(c.character)
num_letters = len(my_letters)

model = tf.keras.models.load_model('saved_model/my_model')


start_all = time.clock()

est_time = 0
num_keyboards = 100
keyboards = list()
keyboards_onehot = np.zeros([num_keyboards, num_letters, num_letters], dtype=int)
for i in range(num_keyboards):
    keyboards.append(copy.deepcopy(initial_characters_placement))
    keyboards[-1].randomize()

    for l in range(len(my_letters)):
        for button, character in zip(keyboard_structure.buttons, keyboards[-1]):
            if character == my_letters[l]:
                position = my_buttons.index(button.id)
                keyboards_onehot[i][l][position] = 1
                break

start_est = time.clock()
model.predict(keyboards_onehot)
end_est = time.clock()
est_time += end_est - start_est

print("time with generating one hot: ", time.clock() - start_all)
print("time only estimation: ", est_time)