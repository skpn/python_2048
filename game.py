
import numpy as np
import random as rd

class Game2048:
	ONGOING = 0
	OVER = 1
	COMPLETED = 2
	def __init__(self, size = 4, unit = 2):
		if size < 2:
			raise ValueError('size must be at least 2')
		elif unit < 2:
			raise ValueError('unit must be at least 2')
		self.size = size
		self.unit = unit
		self.cell = [[0] * size for y in range(4)]
		self.limit = self.unit ** (self.size * self.size)
		self.score = 0
		self.highest = 0
		self.state = self.ONGOING
		self.new_cell()

	def print_cell(self):
		# print("highest : %d" % self.highest)
		print(self.score)
		for line in self.cell:
			print(' '.join(map(str, line)))

	def change_cell_value(self, y, x, value):
		self.score += value
		self.cell[y][x] += value
		if self.highest < self.cell[y][x]:
			self.highest = self.cell[y][x]
			if self.highest == self.limit:
				self.state = self.COMPLETED

	def new_cell(self):
		zeros = list(zip(*np.where(np.array(self.cell) == 0)))
		y, x = rd.choice(zeros)
		new_value = rd.choices((0, self.unit, self.unit * 2), [.1, .8, .1])[0]
		self.change_cell_value(y, x, new_value)
		if (len(zeros) == 1 
			and (y == 0 or self.cell[y - 1][x] != self.cell[y][x])
			and (y == self.size - 1 or self.cell[y + 1][x] != self.cell[y][x])
			and (x == 0 or self.cell[y][x - 1] != self.cell[y][x])
			and (x == self.size - 1 or self.cell[y][x + 1] != self.cell[y][x])):
			self.state = self.OVER

	def new_game(self):
		self.__init__(self.size)

	def merge_cells_left(self, y):
		x = 0
		while x < len(self.cell[y]) - 1:
			if self.cell[y][x] == self.cell[y][x + 1]:
				self.change_cell_value(y, x, self.cell[y][x])
				self.cell[y].pop(x + 1)
			x += 1

	def move_left(self):
		for y in range(self.size):
			if any(self.cell[y]):
				self.cell[y] = list(filter((0).__ne__, self.cell[y]))
				if len(self.cell[y]) > 1:
					self.merge_cells_left(y)
				self.cell[y] += [0] * (self.size - len(self.cell[y]))
		self.new_cell()

	def move_right(self):
		for line in self.cell: line.reverse()
		self.move_left()
		for line in self.cell: line.reverse()

	def move_up(self):
		self.cell = np.array(self.cell).T.tolist()
		self.move_left()
		self.cell = np.array(self.cell).T.tolist()

	def move_down(self):
		self.cell = np.array(self.cell).T.tolist()
		self.move_right()
		self.cell = np.array(self.cell).T.tolist()
