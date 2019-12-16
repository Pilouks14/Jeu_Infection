from abc import ABC, abstractmethod


class AbstractGame(ABC):
	def __init__(self, ply1, ply2):
		self._ply1 = ply1
		self._ply2 = ply2
		self._curPly = ply1

	@property
	def current_player(self):
		return self._curPly

	# abstract public AbstractGame getCopy();

	@abstractmethod
	def play(self, move: int):
		pass

	def play_and_swap(self, move: int):
		self.play(move)
		self._curPly = self._ply2 if self._curPly == self._ply1 else self._ply1

	@abstractmethod
	def valid_moves(self):
		pass

	@abstractmethod
	def move_to_string(self, move: int):
		pass

	@abstractmethod
	def is_over(self):
		pass

	@abstractmethod
	def get_winner(self):
		pass

	def __str__(self):
		pass
