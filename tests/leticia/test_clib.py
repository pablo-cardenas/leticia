import numpy as np
from leticia.clib import clib


def test_taken_distances():
    n_row = 3
    n_col = 3
    taken_weight = 100

    grid = np.array([
        [0, 0, 0],
        [1, 0, 0],
        [0, 1, 0],
    ], dtype='bool')
    num_taken = np.count_nonzero(grid)

    taken_distances = np.zeros((n_row, n_col, num_taken))
    taken_distances_base = np.zeros(num_taken)
    clib.taken_distances(grid, n_row, n_col, taken_weight, taken_distances,
                         taken_distances_base)

    print(grid.astype(int))
    assert np.allclose(
        taken_distances.transpose((2, 0, 1)),
        [[
            [2, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ], [
            [2, 3, 2],
            [2, 3, 2],
            [2, 2, 2],
        ]],
    )

    assert np.allclose(taken_distances_base, [1, 2])


def test_neighbors_distances():
    n_row = 3
    n_col = 3
    taken_weight = 100

    grid = np.array([
        [0, 0, 0],
        [1, 0, 1],
        [0, 0, 0],
    ], dtype='bool')
    num_taken = np.count_nonzero(grid)

    neighbors_distances = np.zeros((n_row, n_col, num_taken, num_taken))
    neighbors_distances_base = np.zeros((num_taken, num_taken))
    clib.neighbors_distances(grid, n_row, n_col, taken_weight,
                             neighbors_distances, neighbors_distances_base)

    print(grid.astype(int))
    print(neighbors_distances_base)

    assert np.allclose(
        neighbors_distances.transpose((2, 3, 0, 1)),
        [[[
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ], [
            [2, 2, 2],
            [2, 4, 2],
            [2, 2, 2],
        ]],
         [[
             [2, 2, 2],
             [2, 4, 2],
             [2, 2, 2],
         ], [
             [0, 0, 0],
             [0, 0, 0],
             [0, 0, 0],
         ]]],
    )

    assert np.allclose(neighbors_distances_base, [
        [0, 2],
        [2, 0],
    ])
