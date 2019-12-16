#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from negamax_player import NegamaxPlayer
from infection_game import InfectionGame

if __name__ == "__main__":
	ply1, ply2 = NegamaxPlayer(), NegamaxPlayer()
	n, m = (9, 9)

	game = InfectionGame(ply1, ply2, n, m)
	print(game)
