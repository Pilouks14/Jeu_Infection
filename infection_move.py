from abstract_move import AbstractMove
from enum import Enum
# from aenum import Enum  # for the aenum version

class InfectionMove(AbstractMove):
	DUPE, MOVE = range(1, 3)
	def __init__(self, token_pos, move):
		self.token_pos = token_pos
		self.move = move

		mx, my = abs(move[0]-token_pos[0]), abs(move[1]-token_pos[1])
		if (mx == 1 and my == 0) or (my == 1 and mx == 0):
			self.type = InfectionMove.DUPE
		elif (mx == 2 and my == 0) or (my == 2 and mx == 0):
			self.type = InfectionMove.MOVE
		else:
			self.type = None

	def __str__(self):
		x, y = self.token_pos
		ox, oy = self.move
		return "({};{} > {};{})".format(x, y, ox, oy)

	def __repr__(self):
		return self.__str__()