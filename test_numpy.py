#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np

# CONSTANTS
N, M = 5, 5
SIZE = (N, M)
PLY1 = 1
PLY2 = 2
MOVES = np.array(((-2, 0), (-1, 0), (1, 0), (2, 0),
                  (0, -2), (0, -1), (0, 1), (0, 2)))

# BOARD VARS
board = np.zeros(SIZE, dtype='uint')
board[0, 0] = PLY1
board[-1, -1] = PLY2
index = np.indices(SIZE)

print("Board:", board.shape)
print("Index:", index.shape)

# GET POSSIBLES MOVEMENTS
tokens_pos = index[:, board == 1]
nb_token = tokens_pos.shape[1]
print("Tokens_pos:\n", tokens_pos)

tokens_pos = np.tile(tokens_pos, MOVES.shape[0])
moves = np.tile(MOVES, (nb_token, 1)).T
print("Tokens_pos:\n", tokens_pos)
print("Moves:\n", moves)

print("Tokens_pos:", tokens_pos.shape)
print("Moves:", moves.shape)

cases = tokens_pos + moves
print("Tokens_pos:\n", cases)

mask = np.sum(
    [(cases[0] >= 0) & (cases[0] < N), (cases[1] >= 0) & (cases[1] < M)], axis=0)
cases = cases[:, mask == 2]

for mv in cases.T:
	print(mv, board[mv[0], mv[1]])
