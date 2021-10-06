
import os
import copy
import json
import time
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


keyboard_file_name = "carpalx-0.12\keren\keren.conf"
def buildCarpalxInput(keyboard):
    with open(keyboard_file_name, 'w') as keyboard_file:
        keyboard_file.write(
            "<keyboard>\n<row 1>\nkeys    = `~ 1! 2@ 3\\# 4$ 5% 6^ 7& 8* 9( 0) -_ =+\nfingers =  0  1  1   2  3  3  3  6 7   7  8  9  9\n</row>\n<row 2>\nkeys    =")

        letters = 0
        for button, character in zip(keyboard_structure.buttons, keyboard):
            if character in my_letters:
                letters += 1
                keyboard_file.write(" " + character)

                if letters == 9:
                    keyboard_file.write(" ;: [{ ]} \\|\nfingers = 0 1 2 3 3 6 6 7 8 9  9  9  9\n</row>\n<row 3>\nkeys    =")

                if letters == 19:
                    keyboard_file.write(" '\"\nfingers = 0 1 2 3 3 6 6 7 8  9  9\n</row>\n<row 4>\nkeys    =")

                if letters == 26:
                    keyboard_file.write(" ,< .> /?\nfingers = 0 1 2 3 3 6 6  7  8  9\n</row>\n</keyboard>")
                    break

        keyboard_file.close()


start_all = time.clock()

est_time = 0
num_keyboards = 100
keyboards = list()
miki = 0
for i in range(num_keyboards):
    keyboards.append(copy.deepcopy(initial_characters_placement))
    keyboards[-1].randomize()

    buildCarpalxInput(keyboards[-1])

    start_est = time.clock()
#for i in range(num_keyboards):
    my_cmd = "perl carpalx-0.12/bin/carpalx -conf carpalx-0.12/etc/tutorial-00.conf"
    my_cmd_output = os.popen(my_cmd)
    for line in my_cmd_output:
        miki = float(line.rstrip())
    end_est = time.clock()

    est_time += end_est - start_est

    #
    #for line in my_cmd_output:
    #    labels[i] = float(line.rstrip())



print("time with generating files: ", time.clock() - start_all)
print("time only estimations: ", est_time)