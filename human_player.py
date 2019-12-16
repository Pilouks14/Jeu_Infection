from abstract_player import AbstractPlayer


class HumanPlayer(AbstractPlayer):
	NEXT_ID = 0

	def __init__(self, name):
		super().__init__()
		self._name = name

	def _negamax(self, game):
		return 0

	def choose_move(self, game):
		choice = None
		valid_moves = game.valid_moves()
		while len(valid_moves) != 0 and choice is None:
			for i, move in enumerate(valid_moves):
				print("{} - {}".format(i + 1, game.move_to_string(move)))

			try:
				choice = int(input('')) - 1
			except:
				choice = None
			if choice < 0 or choice >= len(valid_moves):
				choice = None

		return choice

	def __str__(self):
		return self._name
