import os
import json
import argparse

from helpers import *
from classes.keyboard_structure import KeyboardStructure
from classes.characters_placement import CharactersPlacement

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--genetic-config', required=True)
    args = parser.parse_args()

    info_log('Load genetic config file: %s' % args.genetic_config)
    with open(args.genetic_config, 'r') as file:
        genetic_config = json.load(file)

    info_log('Construct keyboard structure')
    keyboard_structure = KeyboardStructure(
        name=genetic_config['keyboard_structure']['name'],
        width=genetic_config['keyboard_structure']['width'],
        height=genetic_config['keyboard_structure']['height'],
        buttons=genetic_config['keyboard_structure']['buttons'],
        hands=genetic_config['hands']
    )

    info_log('Construct initial characters placement')
    characters_placement = CharactersPlacement(characters_set=genetic_config['characters_set'])

    info_log('Visualize the characters placement')
    keyboard_structure.visualize(
        dirpath=os.path.dirname(args.genetic_config),
        characters_placement=characters_placement,
        save=True
    )
