import numpy as np
from numpy.random import uniform

def affinity(cell, antigen):
    return ((2-np.linalg.norm(cell - antigen))/2)

def inverse_affinity(cell, antigen):
    return (np.linalg.norm(cell - antigen)/2)

def create_random_cells(population_size, feature_num, feature_min, feature_max):
    population = [uniform(low=0, high=1, size=feature_num) for x in range(population_size)]
    return population


def clone(cell, clone_rate):
    clone_num = int(clone_rate / cell[1])
    clones = [(cell[0], cell[1]) for x in range(clone_num)]

    return clones

def hypermutate_variability(cell, mutation_rate, antigen):
    genes = cell[0]
    clone_cache = []
    for gen in genes:
        if uniform(0, 1) < mutation_rate:
            mutated_gen = gen + ((uniform(-1, 1) * (1 - cell[1])) * 0.1)
            
            if(mutated_gen < 0): mutated_gen = 0
            if(mutated_gen > 1): mutated_gen = 1
            clone_cache.append(mutated_gen)
        else:
            clone_cache.append(gen)

    mutated_cell = (np.array(clone_cache), affinity(clone_cache, antigen))
    return mutated_cell


def select(pop, pop_clones, pop_size):
    population = pop + pop_clones
    population = sorted(population, key=lambda x: abs(x[1]).any())[:pop_size]

    return population


def replace(population, population_rand, population_size):
    population = population + population_rand
    population = sorted(population, key=lambda x: abs(x[1]))[:population_size]

    return population

def remove_similar_clones(clone_population, sigma1):
    remaining_clones = []
    n_clones = len(clone_population)
    
    for i in range(n_clones):
        is_similar = False
        for j in range(i + 1, n_clones):
            similarity = affinity(clone_population[i][0], clone_population[j][0])
            if similarity > sigma1:
                is_similar = True
                break
        if not is_similar:
            remaining_clones.append(clone_population[i])
    return remaining_clones

def suppress_similar_cells(population, sigma1):
    suppressed_population = []

    for i, cell1 in enumerate(population):
        is_similar = False

        for j, cell2 in enumerate(population):
            if i != j:
                similarity = affinity(cell1, cell2)
                if similarity > sigma1:
                    is_similar = True
                    break

        if not is_similar:
            suppressed_population.append(cell1)

    return suppressed_population