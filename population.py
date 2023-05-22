from __future__ import annotations
import random


class Population:
    def __init__(
            self,
            num_items: int,
            weights: list[float],
            values: list[float],
            max_weight: float
    ):
        self.num_items = num_items
        self.weights = weights
        self.values = values
        self.max_weight = max_weight
        self.pop_size = 10
        self.mutate_prob = 0.3
        self.init_pop()  # Initialize population

    def init_pop(self):
        done = False
        while not done:
            self.assortments = [
                [random.randint(0, 1) for _ in range(self.num_items)] for _ in range(self.pop_size)
            ]
            valid_assortments = []
            for assortment in self.assortments:
                if not self.get_weight(assortment) > self.max_weight:
                    valid_assortments.append(assortment)
            self.assortments = valid_assortments
            if len(self.assortments) >= 1:
                done = True

    def get_objective(self, assortment):
        return sum([assortment[i] * self.values[i] for i in range(self.num_items)])

    def get_weight(self, assortment):
        return sum([assortment[i] * self.weights[i] for i in range(self.num_items)])

    def evaluate_and_select(self):
        n = self.pop_size
        obj_values = [self.get_objective(assortment) for assortment in self.assortments]
        sorted_assortments = [
            assortment for _, assortment in sorted(zip(obj_values, self.assortments), reverse=True)
        ]
        new_generation = sorted_assortments[: int(n * 0.1)]  # 10% elitism
        self.max_iter = 500
        iter_count = 0
        while len(new_generation) < self.pop_size and iter_count < self.max_iter:
            parent1 = random.choice(sorted_assortments[: n // 2])  # select parents from uppper 50%
            parent2 = random.choice(sorted_assortments[: n // 2])
            child1, child2 = self.crossover(list(parent1), list(parent2))
            child1 = self.mutation(child1)
            child2 = self.mutation(child2)
            if not self.get_weight(child1) > self.max_weight:
                new_generation.append(child1)
            if not self.get_weight(child2) > self.max_weight:
                new_generation.append(child2)
            iter_count += 1
        self.assortments = new_generation

    def crossover(self, parent1, parent2):
        locus = random.randint(0, self.num_items - 1)
        child1 = parent1[:locus] + parent2[locus:]
        child2 = parent2[:locus] + parent1[locus:]
        return child1, child2

    def mutation(self, child):
        flip_or_not = [random.random() < self.mutate_prob for _ in range(self.num_items)]
        return [
            int(child[i] == 0) if flip_or_not[i] else child[i] for i in range(self.num_items)
        ]

    def evolve(self):
        num_gens = 50
        for _ in range(num_gens):
            self.evaluate_and_select()
            obj_values = [self.get_objective(assortment) for assortment in self.assortments]
            sorted_assortments = [
                assortment for _, assortment in sorted(zip(obj_values, self.assortments), reverse=True)  # noqa
            ]
            optim_sol = sorted_assortments[0]
            print(optim_sol, self.get_objective(optim_sol), self.get_weight(optim_sol))


if __name__ == '__main__':
    num_items = 20
    pop_size = 50
    weights = [random.randint(0, 20) for _ in range(num_items)]
    values = [10 + 2 * random.randint(0, 100) for _ in range(num_items)]
    max_weight = int(sum(weights) * 0.7)

    bkga = Population(num_items, weights, values, max_weight)
    print("values:", bkga.values)
    print("weights:", weights)
    print("Max weight:", max_weight)
    print("---------------------")
    bkga.evolve()
