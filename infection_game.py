import numpy as np
from abstract_game import AbstractGame
from infection_move import InfectionMove
import struct


class InfectionGame(AbstractGame):
	DUPES = ((-1, 0), (1, 0), (0, -1), (0, 1))
	MOVE = np.array(((0, -2), (0, 2), (-2, 0), (2, 0)))
	MOVES = np.array(((-2, 0), (-1, 0), (1, 0), (2, 0),
                   (0, -2), (0, -1), (0, 1), (0, 2)))

	def __init__(self, ply1, ply2, N: int, M: int):
		super().__init__(ply1, ply2)
		self._size = (N, M)
		self._board = np.full((N, M), 0)
		self._indices = np.indices((N, M), dtype='uint')

		self._board[0, 0] = 1
		self._board[-1, -1] = 2

		self._value2player = {0: None, 1: ply1, 2: ply2}
		self._player2value = {None: 0, ply1: 1, ply2: 2}

		self._nb_tokens = {
			ply1: self.get_nb_pawns(ply1),
			ply2: self.get_nb_pawns(ply1)}

	def get_nb_pawns(self, ply):
		value = self._player2value[ply]
		if value is None:
			return -1
		return np.count_nonzero(self._board == value)

	def replace_neighbour(self, move: InfectionMove, token_value):
		for neighbour in InfectionGame.DUPES:
			pos = np.array(move.move) + neighbour
			if pos[0] >= 0 and pos[0] < self._size[0]:
				if pos[1] >= 0 and pos[1] < self._size[1]:
					if self._board[pos[0], pos[1]] != 0:
						self._board[pos[0], pos[1]] = token_value

	def play(self, move: InfectionMove):
		if move is None:
			return ValueError('Invalid move index: ' + str(move))
		if isinstance(move, int):
			move = self.valid_moves()[move]
		if move.type is None:
			raise ValueError('Invalid move: ' + str(move))

		token_value = self._player2value[self._curPly]
		self._board[move.move[0], move.move[1]] = token_value

		if move.type == InfectionMove.DUPE:
			self.replace_neighbour(move, token_value)
		elif move.type == InfectionMove.MOVE:
			self._board[move.token_pos[0], move.token_pos[1]] = 0

	def valid_moves(self, ply=None):
		ply = ply if ply is not None else self._curPly
		tokens = self._board == self._player2value[ply]
		tokens_posi = self._indices[:, tokens]
		nb_token = tokens_posi.shape[1]

		nb_moves = InfectionGame.MOVES.shape[0]
		tokens_pos = np.repeat(tokens_posi, nb_moves, axis=1)
		moves = np.tile(InfectionGame.MOVES, (nb_token, 1)).T

		cases = tokens_pos + moves

		N, M = self._size
		mask = [(cases[0] >= 0) & (cases[0] < N), (cases[1] >= 0) & (cases[1] < M)]
		mask = np.sum(mask, axis=0)
		cases = cases[:, mask == 2]
		tokens_pos = tokens_pos[:, mask == 2]

		moves = []
		for pos, final in zip(tokens_pos.T, cases.T):
			if self._board[final[0], final[1]] == 0:
				moves.append(InfectionMove(pos, final))

		return moves

	def move_to_string(self, move: InfectionMove):
		return str(move)

	def is_over(self):
		nb_tokens_ply1 = self.get_nb_pawns(self._ply1)
		nb_tokens_ply2 = self.get_nb_pawns(self._ply2)
		if nb_tokens_ply1 == 0 or nb_tokens_ply1 == 0:
			return True

		nb_moves_1 = len(self.valid_moves(self._ply1)) == 0
		nb_moves_2 = len(self.valid_moves(self._ply2)) == 0
		if nb_moves_1 and nb_moves_2:
			return True

		return False

	def get_winner(self):
		nb_tokens_ply1 = self.get_nb_pawns(self._ply1)
		nb_tokens_ply2 = self.get_nb_pawns(self._ply2)
		if nb_tokens_ply1 > nb_tokens_ply2:
			return self._ply1
		elif nb_tokens_ply1 < nb_tokens_ply2:
			return self._ply2

		return None

	def situation_to_string(self, show_moves=False):
		draw_text = ""

		draw_board = self._board.astype('O', copy=True)
		if show_moves:
			for move in self.valid_moves():
				pos = move.move
				if draw_board[pos[0], pos[1]] != 0:
					continue
				elif draw_board[pos[0], pos[1]] in ('+', '*'):
					draw_board[pos[0], pos[1]] = '@'
				else:
					draw_board[pos[0], pos[1]
                ] = '+' if move.type == InfectionMove.DUPE else '*'

		for row in draw_board:
			for case in row:
				draw_text += str(case) + " "
			draw_text += "\n"
		return draw_text
