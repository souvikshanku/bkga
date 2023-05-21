from __future__ import annotations
import random

import numpy as np


class Population:
    def __init__(
            self,
            num_items: int,
            weights: list[float],
            values: list[float],
            max_weight: float
    ) -> None:
        self.num_items = num_items
        self.weights = np.array(weights)
        self.values = np.array(values)
        self.max_weight = max_weight

        self.pop_size = 3

        # Initialize population
        self.assortments = np.array(
            [np.random.randint(0, 2, num_items) for _ in range(self.pop_size)]
        )
        valid_assortments = []

        for assortment in self.assortments:
            if not self.exceed_max_weight(assortment):
                valid_assortments.append(np.array(assortment))
        self.assortments = valid_assortments

    def get_objective(self, assortment):
        return np.sum(assortment * self.values)

    def get_weight(self, assortment):
        return np.sum(assortment * self.weights)

    def evaluate_and_select(self):
        n = self.pop_size
        obj_values = np.array([self.get_objective(assortment) for assortment in self.assortments])
        sorted_assortments = list(np.array(self.assortments)[np.argsort(- obj_values)])

        new_generation = sorted_assortments[: int(n * 0.1)]  # 10% elitism

        self.while_count = 0
        while len(new_generation) < self.pop_size and self.while_count < 100:
            parent1 = random.choice(sorted_assortments[: n // 2])  # select parents from uppper 50%
            parent2 = random.choice(sorted_assortments[: n // 2])
            child1, child2 = self.crossover(list(parent1), list(parent2))

            if not self.exceed_max_weight(child1):
                new_generation.append(child1)
            if not self.exceed_max_weight(child2):
                new_generation.append(child2)

            self.while_count += 1

        self.assortments = np.array(new_generation)

    def crossover(self, parent1, parent2):
        locus = np.random.randint(self.num_items)
        child1 = parent1[:locus] + parent2[locus:]
        child2 = parent2[:locus] + parent1[locus:]
        return child1, child2

    def mutation(self):
        for i in range(2):
            assortment = self.assortments[i]
            flip_prob = 0.1
            flip_or_not = [random.random() < flip_prob for _ in range(self.num_items)]
            self.assortments[i] = np.array([
                assortment[i] == 0 if flip_or_not[i] else assortment[i] for i in range(len(assortment))  # noqa
            ]).astype(int)

    def exceed_max_weight(self, assortment):
        if self.get_weight(assortment) > self.max_weight:
            return True
        else:
            return False

    def evolve(self):
        max_iter = 100
        for _ in range(max_iter):
            self.evaluate_and_select()
            if self.while_count >= 100:
                break
            optim_sol = self.assortments[0]
            print(optim_sol, self.get_objective(optim_sol), self.get_weight(optim_sol))
            self.mutation()


num_items = 100
pop_size = 30
weights = np.random.randint(0, 20, num_items)
values = 10 + 2 * np.random.randint(0, 100, num_items)
max_weight = int(weights.sum() * 0.7)

bkga = Population(num_items, weights, values, max_weight)
print(bkga.assortments)
print("values: ", bkga.values)
print("weights: ", weights)
print("Max weight: ", max_weight)
print("---------------------")
bkga.evolve()

# TODO: Get rid of numpy
