import os
import json
import argparse

from helpers import *
from classes.keyboard_structure import KeyboardStructure
from classes.characters_placement import CharactersPlacement
from classes.genetic import Genetic

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--genetic-config', required=True)
    parser.add_argument('--testing-corpus', required=True)
    args = parser.parse_args()

    info_log('Load genetic config file: %s' % args.genetic_config)
    with open(args.genetic_config, 'r') as file:
        genetic_config = json.load(file)

    info_log('Load testing corpus file: %s' % args.testing_corpus)
    with open(args.testing_corpus, 'r', encoding='utf-8') as file:
        testing_corpus = file.readlines()

    testing_corpus_dict = dict()
    for line in testing_corpus:
        for char in line.strip():
            try: testing_corpus_dict[char] += 1
            except: testing_corpus_dict[char] = 1

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

    characters_placement.calculate_fitness(keyboard_structure, testing_corpus_dict)
    info_log('Fitness value: %s' % characters_placement.fitness)
