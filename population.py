from __future__ import annotations

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

    def get_objective(self, assortment):
        return np.sum(assortment * self.values)

    def get_weight(self, assortment):
        return np.sum(assortment * self.weights)

    def evaluate(self):
        """
        It also sorts the assortment based on their objective values.
        """
        obj_values = [self.get_objective(assortment) for assortment in self.assortments]
        sorted_assortments = [
            assortment for _, assortment in sorted(zip(obj_values, self.assortments), reverse=True)
        ]
        self.assortments = np.array(sorted_assortments)

    def crossover(self):
        locus = np.random.randint(1, self.num_items - 1)
        print("locus: ", locus)
        parent1 = list(self.assortments[0])
        parent2 = list(self.assortments[1])

        child1 = parent1[:locus] + parent2[locus:]
        child2 = parent2[:locus] + parent1[locus:]

        self.assortments[0] = np.array(child1)
        self.assortments[1] = np.array(child2)

    def check_constraints(self):
        pass


# items = [
#     [0, 1, 0, 1, 1, 0],
#     [1, 0, 1, 0, 1, 1],
#     [0, 1, 0, 0, 1, 0],
# ]

weights = [12, 22, 10, 34, 56, 15]
values = [3, 4, 1, 6, 8, 5]
max_weight = 40

bkga = Population(6, weights, values, max_weight)
print(bkga.assortments)
print("values: ", bkga.values)
print("---------------------")

bkga.evaluate()

print(bkga.assortments)
print("---------------------")

bkga.crossover()
print(bkga.assortments)
