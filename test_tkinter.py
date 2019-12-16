#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
assert sys.version_info[0] == 3, "Please use python 3."
import tkinter as tk
from tkinter import ttk
from infection_game import InfectionGame
from infection_move import InfectionMove
from random_player import RandomPlayer
from human_player import HumanPlayer
from negamax_player import NegamaxPlayer
import numpy as np

CELL_SIZE = 64
DELAY = 50
N = 9
M = 9


class Cell(tk.Button):
	def __init__(self, parent, pos, color=(30, 30, 30), *args, **kwargs):
		tk.Button.__init__(self, parent, *args, **kwargs)
		self.pos = pos
		self._rgb = None
		self._color = None
		self._hover_color = None
		self.color = color
		self.configure(bg=self._color)

		self.bind("<Leave>", self.on_leave)
		self.bind("<Enter>", self.on_enter)

	@property
	def state(self):
		return self['state']

	@state.setter
	def state(self, value):
		self.config(state=value)

	def enable(self):
		self.config(state="normal")

	def disable(self):
		self.config(state="disabled")

	def toggle_state(self):
		self.state = "normal" if self.state == "disabled" else "disabled"

	def on_enter(self, event):
		if self.state == "normal":
			self.configure(bg=self._hover_color)

	def on_leave(self, event):
		self.configure(bg=self._color)

	@property
	def color(self):
		return self._rgb

	@color.setter
	def color(self, rgb):
		self._rgb = rgb
		gray = self._rgb[0] + self._rgb[1] + self._rgb[2] / 3
		hov = rgb
		if gray <= 127:
			hov = (self._rgb[0] + 16, self._rgb[1] + 16, self._rgb[2] + 16)
		else:
			hov = (self._rgb[0] - 16, self._rgb[1] - 16, self._rgb[2] - 16)
		self._hover_color = "#%02x%02x%02x" % hov
		self._color = "#%02x%02x%02x" % rgb
		self.configure(bg=self._color)


class Application(tk.Frame):
	def __init__(self, master=None, N=9, M=9):
		super().__init__(master)
		self.master = master
		self.N, self.M = N, M
		self.master.geometry("{:.0f}x{:.0f}".format(N * CELL_SIZE, M * CELL_SIZE))
		self.cells = np.full((N, M), None, dtype='O')
		self.create_widgets()

	def create_widgets(self):
		self.grid_propagate(False)
		tk.Grid.rowconfigure(self.master, 0, weight=1)

		tk.Grid.columnconfigure(self.master, 0, weight=1)

		# Create & Configure frame
		self.grid(row=0, column=0, sticky='nsew')

		# Create a 5x10 (rows x columns) grid of buttons inside the frame
		for x in range(self.N):
			tk.Grid.rowconfigure(self, x, weight=1)
			for y in range(self.M):
				tk.Grid.columnconfigure(self, y, weight=1)
				# create a button inside frame
				self.cells[x, y] = Cell(self, pos=(
					x, y), height=CELL_SIZE, width=CELL_SIZE)
				# self.cells[x, y].disable()
				self.cells[x, y].grid(row=x, column=y, sticky='nsew')


class Controller:
	def __init__(self, model, view, delay=100):
		self.model = model
		self.view = view
		self.delay = delay

		self.ply2color = {model._ply1: (
			244, 65, 145), model._ply2: (65, 244, 214), None: (30, 30, 30)}
		self.color2ply = {v: k for k, v in self.ply2color.items()}

		self.old_board = np.zeros_like(self.model._board)
		self.selected = None
		self.moves = None

		board = model._board
		N, M = board.shape
		for x in range(N):
			for y in range(M):
				self.setup_command(view.cells[x, y])
		self.update_cells()

	def update_cells(self):
		board = self.model._board
		N, M = board.shape
		# TODO: Only edit modify cells & Disable/Enable player's cells
		difference = np.where(board != self.old_board)
		for x in range(N):
			for y in range(M):
				cell = view.cells[x, y]
				cell.color = self.ply2color[self.model._value2player[board[x, y]]]
				if board[x, y] == self.model._player2value[model._curPly]:
					cell.enable()
				else:
					cell.disable()

	def setup_command(self, cell):
		cell['text'] = str(cell.pos)
		cell['command'] = lambda: self.cell_pressed(cell)

	def play_move(self, move):
		self.old_board = self.model._board.copy()
		self.model.play_and_swap(move)
		self.selected = None
		self.moves = None
		self.update_cells()
		if not self.model.is_over():
			view.master.after(self.delay, self.play)
		else:
			nb_tokens1 = self.model.get_nb_pawns(self.model._ply1)
			nb_tokens2 = self.model.get_nb_pawns(self.model._ply2)
			print(self.model.get_winner(), nb_tokens1, nb_tokens2)
		print(self.model.situation_to_string())

	def play(self):
		if not isinstance(self.model.current_player, HumanPlayer):
			self.play_move(self.model.current_player.choose_move(self.model))
			#view.master.after(100, self.play)

	def cell_pressed(self, cell):
		if self.selected is not None and cell.color not in self.color2ply:
			self.play_move(InfectionMove(self.selected, cell.pos))
		elif self.color2ply[cell.color] == self.model.current_player:
			if self.moves is not None:
				for move in self.moves:
					pos = move.move
					cell2 = self.view.cells[pos[0], pos[1]]
					cell2.disable()
					cell2.color = self.ply2color[None]
				self.moves = None

			self.selected = cell.pos
			validMoves = self.get_cell_moves(self.selected)
			for move in validMoves:
				pos = move.move
				cell = self.view.cells[pos[0], pos[1]]
				cell.enable()
				if move.type == InfectionMove.DUPE:
					cell.color = (100, 100, 100)
				elif move.type == InfectionMove.MOVE:
					cell.color = (75, 75, 75)
			self.moves = validMoves

	def get_cell_moves(self, cell):
		validmoves = self.model.valid_moves()
		moves = []
		current = self.selected
		for move in validmoves:
			if move.token_pos[0] == current[0] and move.token_pos[1] == current[1]:
				moves.append(move)
		return moves


if __name__ == "__main__":
	root = tk.Tk()
	model = InfectionGame(RandomPlayer(), RandomPlayer(), N, M)
	view = Application(master=root, N=N, M=M)
	controller = Controller(model, view, DELAY)
	root.after(DELAY, controller.play)
	view.mainloop()
