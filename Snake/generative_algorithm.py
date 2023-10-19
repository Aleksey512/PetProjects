import random


def crossover(parent1, parent2):
    if not parent1:
        return parent2

    if not parent2:
        return parent1

    crossover_point = random.randint(0, len(parent1) - 1)
    child_genome = parent1[:crossover_point] + parent2[crossover_point:]
    return child_genome


def mutate(genome, mutation_rate: float):
    mutated_genome = genome[:]
    for i in range(len(mutated_genome)):
        if random.random() < mutation_rate:
            mutated_genome[i] = random.choice(["LEFT", "RIGHT", "UP", "DOWN"])
    return mutated_genome
