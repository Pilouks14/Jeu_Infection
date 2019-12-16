from abstract_player import AbstractPlayer
from random import randrange as rng


class RandomPlayer(AbstractPlayer):
	NEXT_ID = 0

	def __init__(self):
		super().__init__()
		self._id = RandomPlayer.NEXT_ID
		RandomPlayer.NEXT_ID += 1

	def choose_move(self, game):
		valid_moves = game.valid_moves()
		if len(valid_moves) == 0:
			return

		return rng(0, len(valid_moves))

	def __str__(self):
		return "RandomPlayer #" + str(self._id)
