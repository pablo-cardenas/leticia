import random
import time

import numpy as np
from scipy.ndimage import convolve

from .clib import clib


def run(n_col, n_row, params, seed=42):
    taken_weight = float('inf')
    grid = np.zeros((n_row, n_col), dtype='bool')
    random.seed(seed)

    list_points = []
    list_probabilities = []
    list_variables = []
    i = 0
    while True:
        i += 1
        start_time = time.time()

        num_taken = np.count_nonzero(grid)

        # compute taken_distances, taken_distances_base
        taken_distances = np.zeros((n_row, n_col, num_taken))
        taken_distances_base = np.zeros(num_taken)
        clib.taken_distances(grid, n_row, n_col, taken_weight, taken_distances,
                             taken_distances_base)
        diff_taken_distances = taken_distances - taken_distances_base

        # compute neighbors distances
        distances = np.zeros((n_row, n_col))
        clib.distances(grid, n_row, n_col, taken_weight, distances)

        # compute neighbors distances
        neighbors_distances = np.zeros((n_row, n_col, num_taken, num_taken))
        neighbors_distances_base = np.zeros((num_taken, num_taken))
        clib.neighbors_distances(grid, n_row, n_col, taken_weight,
                                 neighbors_distances, neighbors_distances_base)
        diff_neighbors_distances = neighbors_distances - neighbors_distances_base

        # compute num_neighbors
        kernel = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
        num_neighbors = convolve(grid.astype(int), kernel, mode='constant')

        # compute probabilities
        variables = np.array([
            distances,
            num_neighbors,
            diff_taken_distances.sum(2) / (num_taken + 0.01),
            diff_neighbors_distances.max(3, initial=0).sum(2) / (num_taken + 0.01),
        ])
        linear_combination = np.einsum('i,ijk', params, variables)
        probabilities = np.exp(linear_combination)
        probabilities[0] = 0
        probabilities[grid] = 0
        probabilities[np.isinf(diff_taken_distances.sum(2))] = 0
        probabilities[np.isinf(distances)] = 0

        print('{:5d}{:5d}'.format(i, np.count_nonzero(probabilities)), end=' ')

        list_variables.append(variables.tolist())
        list_probabilities.append(probabilities.tolist())

        if probabilities.sum() == 0:
            break

        x = random.choices(range(n_row * n_col),
                           weights=probabilities.flatten())[0]

        list_points.append(x)

        grid.flat[x] = 1

        # use loggging
        print('{:5.2g}s'.format(time.time() - start_time), end='\r')

    return {
        'nrow': n_row,
        'ncol': n_col,
        'params': params,
        'seed': seed,
        'points': list_points,
        'probabilities': list_probabilities,
        'variables': list_variables,
    }
