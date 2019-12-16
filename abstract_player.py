from abc import ABC, abstractmethod


class AbstractPlayer(ABC):

	@abstractmethod
	def choose_move(self, game):
		pass

	def __str__(self):
		pass
