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
    initial_characters_placement = CharactersPlacement(characters_set=genetic_config['characters_set'])

    info_log('Start genetic algorithm')
    genetic = Genetic(
        number_of_generations=genetic_config['number_of_generations'],
        number_of_characters_placements=genetic_config['number_of_characters_placements'],
        number_of_accepted_characters_placements=genetic_config['number_of_accepted_characters_placements'],
        number_of_randomly_injected_characters_placements=
                                        genetic_config['number_of_randomly_injected_characters_placements'],
        maximum_number_of_mutation_operations=genetic_config['maximum_number_of_mutation_operations'],
        corpus_path=genetic_config['corpus_path'],
        searching_corpus_size=genetic_config['searching_corpus_size'],
        testing_corpus_size=genetic_config['testing_corpus_size'],
        maximum_line_length=genetic_config['maximum_line_length'],
        random_seed=genetic_config['random_seed'],
        number_of_cores=genetic_config['number_of_cores'],
        keyboard_structure=keyboard_structure,
        initial_characters_placement=initial_characters_placement
    )
    genetic.start()
    #genetic.save_searching_and_testing_corpus(os.path.dirname(args.genetic_config))

    #genetic.best_characters_placement.calculate_fitness(
    #    genetic.keyboard_structure,
    #    genetic.testing_corpus_dict
    #)
    #info_log('Best characters placement fitness value on testing set: %s' % genetic.best_characters_placement.fitness)

    info_log('Visualize best characters placement found by genetic algorithm')
    genetic.keyboard_structure.visualize(
        dirpath=os.path.dirname(args.genetic_config),
        characters_placement=genetic.best_characters_placement,
        save=True
    )
