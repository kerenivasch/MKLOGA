import time
import numpy as np

from helpers import *
from classes.character import Character

class CharactersPlacement:
    def __init__(self, characters_set):
        self.fitness = -1
        self.characters_set = list()
        for character in characters_set:
            self.characters_set.append(Character(
                character=character['character'],
                button_id=character['button_id']
            ))
        self._order_fixed_characters()

    def randomize(self):
        np.random.shuffle(self.characters_set)
        self._order_fixed_characters()

    def calculate_fitness(self, keyboard_structure, searching_corpus_dict):
        fitness = 0

        smallest_distance = dict()
        for i, character in enumerate(self.characters_set):
            smallest_distance[character.character] = \
                keyboard_structure.smallest_distance_from_button_to_finger(i)

        for character in searching_corpus_dict:
            if character not in smallest_distance:
                warning_log('Found unrecognized character \'%s\'' % character)
                continue

            fitness += (smallest_distance[character] * searching_corpus_dict[character])

        self.fitness = round(fitness, 2)

        return self.fitness

    def mutate(self, maximum_number_of_mutation_operations):
        number_of_mutation_operations = np.random.randint(0, maximum_number_of_mutation_operations)
        for _ in range(number_of_mutation_operations):
            i = self._non_fixed_random_character()
            j = self._non_fixed_random_character()
            self.characters_set[i], self.characters_set[j] = self.characters_set[j], self.characters_set[i]

    def _order_fixed_characters(self):
        fixed_characters = list()

        for i in range(len(self.characters_set)):
            if self.characters_set[i].button_id != None:
                fixed_characters.append(self.characters_set[i])
        self.characters_set = [character for character in self.characters_set if character.button_id == None]

        fixed_characters = sorted(fixed_characters, key=lambda character: character.button_id)

        for character in fixed_characters:
            self.characters_set.insert(character.button_id - 1, character)

    def _non_fixed_random_character(self):
        rand = np.random.randint(0, len(self.characters_set) - 1)
        while self.characters_set[rand].button_id != None:
            rand = np.random.randint(0, len(self.characters_set) - 1)
        return rand

    def __getitem__(self, idx):
        return self.characters_set[idx].character
