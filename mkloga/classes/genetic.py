import re
import os
import copy
import time
import math
import numpy as np
import tensorflow as tf

from multiprocessing import Process, Manager
from threading import Thread
from helpers import *

punct = True

class Genetic:
    def __init__(
        self,
        number_of_generations,
        number_of_characters_placements,
        number_of_parent_placements,
        number_of_accepted_characters_placements,
        number_of_randomly_injected_characters_placements,
        maximum_number_of_mutation_operations,
        corpus_path,
        searching_corpus_size,
        testing_corpus_size,
        maximum_line_length,
        random_seed,
        number_of_cores,
        keyboard_structure,
        initial_characters_placement
    ):

        path_str = ""
        if (punct):
            path_str = "_punct"
        self.model = tf.keras.models.load_model('saved_model/my_model' + path_str)

        self.my_letters = []
        self.my_buttons = [keyboard_structure.buttons[i].id for i in range(len(keyboard_structure.buttons))]
        for c in initial_characters_placement.characters_set:
            if (c.button_id is not None):
                self.my_buttons.remove(c.button_id)
            else:
                self.my_letters.append(c.character)

        self.number_of_generations = number_of_generations
        self.number_of_characters_placements = number_of_characters_placements
        self.number_of_parent_placements = number_of_parent_placements
        self.number_of_accepted_characters_placements = number_of_accepted_characters_placements
        self.number_of_randomly_injected_characters_placements = number_of_randomly_injected_characters_placements
        self.maximum_number_of_mutation_operations = maximum_number_of_mutation_operations
        self.number_of_cores = number_of_cores
        self.keyboard_structure = keyboard_structure
        self.initial_characters_placement = initial_characters_placement
        self._regex = re.compile('[^%s]' % ''.join(sorted(set(self.initial_characters_placement))))

        self.corpus = open(corpus_path, 'r', encoding='utf-8').read().split('\n')
        self.corpus = [line for line in self.corpus if len(line) <= maximum_line_length]

        rng = np.random.RandomState(random_seed)
        rng.shuffle(self.corpus)

        self.searching_corpus = [self._preprocess_line(line) for line in self.corpus[:searching_corpus_size]]

        if len(self.searching_corpus) < searching_corpus_size:
            warning_log('Searching corpus size didn\'t reach %s, its current size is %s' %
                (searching_corpus_size, len(self.searching_corpus)))

        self.searching_corpus_dict = dict()
        for line in self.searching_corpus:
            for char in line.strip():
                try: self.searching_corpus_dict[char] += 1
                except: self.searching_corpus_dict[char] = 1

        self.testing_corpus = [self._preprocess_line(line) for line in
                            self.corpus[searching_corpus_size:searching_corpus_size + testing_corpus_size]]

        if len(self.testing_corpus) < testing_corpus_size:
            warning_log('Testing corpus size didn\'t reach %s, its current size is %s' %
                (testing_corpus_size, len(self.testing_corpus)))

        self.testing_corpus_dict = dict()
        for line in self.testing_corpus:
            for char in line.strip():
                try: self.testing_corpus_dict[char] += 1
                except: self.testing_corpus_dict[char] = 1

        self.characters_placements = list()
        for _ in range(self.number_of_characters_placements):
            self.characters_placements.append(copy.deepcopy(self.initial_characters_placement))
            self.characters_placements[-1].randomize()

        self.time = -1
        self.best_characters_placement = None

    def buildCarpalxInput(self, keyboard):
        carpalx_file_name = "carpalx-0.12\keren\keren.conf"
        with open(carpalx_file_name, 'w') as keyboard_file:
            keyboard_file.write(
                "<keyboard>\n<row 1>\nkeys    = `~ 1! 2@ 3\\# 4$ 5% 6^ 7& 8* 9( 0) -_ =+\nfingers =  0  1  1   2  3  3  3  6 7   7  8  9  9\n</row>\n<row 2>\nkeys    =")

            letters = 0
            for button, character in zip(self.keyboard_structure.buttons, keyboard):
                if character in self.my_letters:
                    letters += 1
                    keyboard_file.write(" " + character)

                    if letters == 9: #10
                        keyboard_file.write(
                            " ;: [{ ]} \\|\nfingers = 0 1 2 3 3 6 6 7 8 9  9  9  9\n</row>\n<row 3>\nkeys    =")
                            #" [{ ]} \\|\nfingers = 0 1 2 3 3 6 6 7 8 9  9  9  9\n</row>\n<row 3>\nkeys    =")

                    if letters == 19:
                        keyboard_file.write(" '\"\nfingers = 0 1 2 3 3 6 6 7 8  9  9\n</row>\n<row 4>\nkeys    =")
                        #keyboard_file.write(" ;: '\"\nfingers = 0 1 2 3 3 6 6 7 8  9  9\n</row>\n<row 4>\nkeys    =")

                    if letters == 26:
                        keyboard_file.write(" ,< .> /?\nfingers = 0 1 2 3 3 6 6  7  8  9\n</row>\n</keyboard>")
                        break

            keyboard_file.close()

    def buildCarpalxInput_punct(self, keyboard):
        punct_map = {"-": "-_", "+": "=+", "{": "[{", "}": "]}", ";": ";:", "'": "'\"", ",": ",<", ".": ".>", "?": "/?"}

        carpalx_file_name = "carpalx-0.12\keren\keren.conf"
        with open(carpalx_file_name, 'w') as carpalx_file:
            carpalx_file.write("<keyboard>\n<row 1>\nkeys    = `~ 1! 2@ 3\\# 4$ 5% 6^ 7& 8* 9( 0)")

            letters = 0
            for button, character in zip(self.keyboard_structure.buttons, keyboard):
                if character in self.my_letters:
                    letters += 1

                    if character in punct_map.keys():
                        carpalx_file.write(" " + punct_map[character])
                    elif character >= 'a' and character <= 'z':
                        carpalx_file.write(" " + character)
                    else:
                        print("wrong character: ", character)
                        exit(1)

                    if letters == 2:
                        carpalx_file.write(
                            "\nfingers =  0  1  1   2  3  3  3  6 7   7  8  9  9\n</row>\n<row 2>\nkeys    =")

                    if letters == 14:
                        carpalx_file.write(" \\|\nfingers = 0 1 2 3 3 6 6 7 8 9  9  9  9\n</row>\n<row 3>\nkeys    =")

                    if letters == 25:
                        carpalx_file.write(" \nfingers = 0 1 2 3 3 6 6 7 8  9  9\n</row>\n<row 4>\nkeys    =")

                    if letters == 35:
                        carpalx_file.write(" \nfingers = 0 1 2 3 3 6 6  7  8  9\n</row>\n</keyboard>")
                        break

            carpalx_file.close()

    def start(self):
        start_time = time.time()

        for generation in range(self.number_of_generations):
            info_log('Start generation number %s' % (generation + 1))

            info_log('Calculate fitness function for each characters placement')
            self.model_best = self.calculate_fitness_for_characters_placements()
            info_log('model fitness value: %s' % self.model_best[0][2])

            same_kb = True
            num_same = 0
            while same_kb:
                for i in range(len(self.my_letters)):
                    for j in range(len(self.my_letters)):
                        if self.model_best[num_same][1][i][j]!=self.model_best[num_same+1][1][i][j]:
                            same_kb=False
                num_same += 1
            #print("Number of same keyboards: ", num_same)

            print("model fitness: ", [self.model_best[i][2] for i in range(10)])

            true_fitness = []
            for b in self.model_best:
                if(punct):
                    self.buildCarpalxInput_punct(b[0])
                else:
                    self.buildCarpalxInput(b[0])
                my_cmd = "perl carpalx-0.12/keren/carpalx_keren -conf carpalx-0.12/etc/tutorial-00.conf"
                my_cmd_output = os.popen(my_cmd)

                for line in my_cmd_output:
                    true_fitness.append(float(line.rstrip()))

            print("true fitness: ", [true_fitness[i] for i in range(10)])
            info_log('true value: %s' % true_fitness[0])

            self.model.fit(
                np.array([self.model_best[i][1] for i in range(len(self.model_best))]), np.array(true_fitness), epochs=10)

            new_predictions = self.model.predict(np.array([self.model_best[i][1] for i in range(10)]))
            print("new model fitness: ", [new_predictions[i][0] for i in range(10)])

            trueJoint = [[self.model_best[i][0], true_fitness[i]] for i in range(len(self.model_best))]
            sorted_trueJoint = sorted(trueJoint, key=lambda x:x[1])
            self.parents = [sorted_trueJoint[i][0] for i in range(self.number_of_parent_placements)]

            best_fitness_value = sorted_trueJoint[0][1]
            best_characters_placement = sorted_trueJoint[0][0]
            if self.best_characters_placement is None or best_fitness_value < self.best_fitness_value:
                self.best_characters_placement = best_characters_placement
                self.best_fitness_value = best_fitness_value
            info_log('Best characters placement fitness value: %s' % self.best_fitness_value)

            info_log('Start natural selection and crossover')
            self.natural_selection_and_crossover()

            info_log('Start mutating characters placements')
            self.mutate_characters_placements()

            info_log('Start random injection')
            self.random_injection()

        self.time = round((time.time() - start_time) / 60, 2)
        info_log('Time taken for genetic algorithm is %s minutes' % (self.time))

    def calculate_fitness_for_characters_placements(self):
        def calculate_bucket_fitness(characters_placements, keyboard_structure, searching_corpus_dict, index, fitness_dict):
            for i, characters_placement in enumerate(characters_placements):
                characters_placement.calculate_fitness(keyboard_structure, searching_corpus_dict)
                fitness_dict[index + i] = characters_placement.fitness

        #manager = Manager()
        fitness_dict = [0 for _ in self.characters_placements]#manager.dict()

        '''
        bucket_size = math.ceil(len(self.characters_placements) / self.number_of_cores)
        processes = list()
        for i in range(self.number_of_cores):
            start = i * bucket_size
            end = start + bucket_size
            process = Process(
                target=calculate_bucket_fitness,
                args=(
                    self.characters_placements[start:end],
                    self.keyboard_structure,
                    self.searching_corpus_dict,
                    start,
                    fitness_dict
                )
            )
            process.start()
            processes.append(process)

        for process in processes:
            process.join()
        '''

        num_of_characters = len(self.my_letters)
        #calculate_bucket_fitness(self.characters_placements, self.keyboard_structure, self.searching_corpus_dict, 0, fitness_dict)
        keyboard_onehots = np.zeros([len(self.characters_placements), num_of_characters, num_of_characters], dtype=int)
        for cp in range(len(self.characters_placements)):
            for l in range(num_of_characters):
                for button, character in zip(self.keyboard_structure.buttons, self.characters_placements[cp]):
                    if character == self.my_letters[l]:
                        position = self.my_buttons.index(button.id)
                        keyboard_onehots[cp][l][position] = 1
                        break
        fitness_dict = self.model.predict(keyboard_onehots)

        #best_fitness_value = float('inf')
        #best_characters_placement = None
        #for i, characters_placement in enumerate(self.characters_placements):
        #    characters_placement.fitness = fitness_dict[i][0]
        #    if characters_placement.fitness < best_fitness_value:
        #        best_fitness_value = characters_placement.fitness
        #        best_characters_placement = characters_placement


        joint = [[self.characters_placements[i], keyboard_onehots[i], fitness_dict[i][0]] for i in range(len(self.characters_placements))]
        sorted_joint = sorted(joint, key=lambda x:x[2])

        #return best_characters_placement,
        return sorted_joint[:self.number_of_accepted_characters_placements]

    def old_natural_selection_and_crossover(self):
        self.characters_placements = sorted(self.characters_placements,
                                                key=lambda characters_placement: characters_placement.fitness)

        temp_characters_placements = list()
        for i in range(self.number_of_accepted_characters_placements):
            temp_characters_placements.append(copy.deepcopy(self.characters_placements[i]))

        while len(temp_characters_placements) < self.number_of_characters_placements - \
                                                            self.number_of_randomly_injected_characters_placements:
            a, b = np.random.beta(a=0.5, b=2, size=2)

            a = math.floor(a * self.number_of_characters_placements)
            b = math.floor(b * self.number_of_characters_placements)

            assert(a != self.number_of_characters_placements)
            assert(b != self.number_of_characters_placements)

            temp_characters_placements.append(self._crossover(
                self.characters_placements[a],
                self.characters_placements[b]
            ))

            if len(temp_characters_placements) >= self.number_of_characters_placements - \
                                                            self.number_of_randomly_injected_characters_placements:
                break

            temp_characters_placements.append(self._crossover(
                self.characters_placements[b],
                self.characters_placements[a]
            ))

        self.characters_placements = temp_characters_placements

    def natural_selection_and_crossover(self):
        temp_characters_placements = list()
        for i in range(self.number_of_accepted_characters_placements):
            temp_characters_placements.append(copy.deepcopy(self.model_best[i][0]))

        while len(temp_characters_placements) < self.number_of_characters_placements - \
                                                            self.number_of_randomly_injected_characters_placements:
            a, b = np.random.randint(low=0, high=self.number_of_parent_placements, size=2)

            temp_characters_placements.append(self._crossover(
                self.parents[a],
                self.parents[b]
            ))

        self.characters_placements = temp_characters_placements

    def random_injection(self):
        for _ in range(self.number_of_randomly_injected_characters_placements):
            random_characters_placement = copy.deepcopy(self.characters_placements[0])
            random_characters_placement.randomize()
            self.characters_placements.append(random_characters_placement)

    def mutate_characters_placements(self):
        for characters_placement in self.characters_placements:
            characters_placement.mutate(self.maximum_number_of_mutation_operations)

    def save_searching_and_testing_corpus(self, dirpath):
        with open(os.path.join(dirpath, 'searching_corpus'), 'w') as file:
            file.write('\n'.join(self.searching_corpus))

        with open(os.path.join(dirpath, 'testing_corpus'), 'w') as file:
            file.write('\n'.join(self.testing_corpus))

    def _preprocess_line(self, line):
        return self._regex.sub('', line)

    def _oldcrossover(self, a, b):
        new_characters_placement = copy.deepcopy(a)

        chosen_characters = list()
        for character in new_characters_placement.characters_set:
            if character.button_id != None or np.random.rand() >= 0.5:
                chosen_characters.append(character)

        needed_characters = list()
        for character in b.characters_set:
            if character not in chosen_characters:
                needed_characters.append(character)

        j = 0
        for i in range(len(new_characters_placement.characters_set)):
            if new_characters_placement.characters_set[i] in chosen_characters:
                continue

            new_characters_placement.characters_set[i] = copy.deepcopy(needed_characters[j])
            j += 1

        return new_characters_placement

    def _crossover(self, a, b):
        new_characters_placement = copy.deepcopy(a)

        placements = list(range(len(new_characters_placement.characters_set)))
        while len(placements)>0:
            parent = random.choice([a, b])
            original_place = random.choice(placements)
            place = original_place
            new_place = -1
            while new_place != original_place:
                new_characters_placement.characters_set[place] = parent.characters_set[place]

                new_place = a.characters_set.index(b.characters_set[place])

                placements.remove(place)
                place = new_place

        return new_characters_placement