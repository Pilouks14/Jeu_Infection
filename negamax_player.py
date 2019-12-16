from abstract_player import AbstractPlayer


class NegamaxPlayer(AbstractPlayer):
	NEXT_ID = 0

	def __init__(self):
		super().__init__()
		self._id = NegamaxPlayer.NEXT_ID
		NegamaxPlayer.NEXT_ID += 1

	def _negamax(self, game):
		return 0

	def chooseMove(self, game):
		return self._negamax(game)

	def __str__(self):
		return "NegaMaxPlayer #" + self._id
