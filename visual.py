
from game import Game2048
import curses
import time

class Cell2048:
	def __init__(self, y_pos, x_pos, y_size, x_size):
		self.y_pos = y_pos
		self.x_pos = x_pos
		self.y_size = y_size
		self.x_size = x_size
		self.value = 0
		self.y_pos_write = self.y_pos + self.y_size // 2
	
	def write(self, screen, value):
		for y in range(self.y_pos, self.y_pos + self.y_size):
			screen.addstr(y, self.x_pos, " ".center(self.x_size),
				curses.color_pair())
		screen.addstr(self.y_pos_write, self.x_pos,
			str(value).center(self.x_size))

class Visual2048:
	def __init__(self, game):
		if not isinstance(game, Game2048):
			raise TypeError("game must be an instance of Game class")
		self.game = game
		self.x_cell = len(str(game.limit)) + 3 
		self.y_cell = self.x_cell * 2 // 3 + (self.x_cell * 2 % 3 > 0)
		self.y_game = self.y_cell * game.size
		self.x_game = self.x_cell * game.size
		self.y_start = None
		self.x_start = None
		self.colors = [0, *range(22, 52), *reversed(range(124, 142))]

	def print_cell(self, screen, y, x, cell, color):
		screen.addstr(y, x, str(cell).center(self.x_cell), color)

	def print_game(self, screen, game, score):
		screen.addstr(self.y_start - 2, self.x_start, score.rjust(self.x_game))
		y = self.y_start
		for line in game.cell:
			x = self.x_start
			for cell in line:
				self.print_cell(screen, y + self.y_cell // 2 , x, cell)
				x += self.x_cell
			y += self.y_cell

	def get_next_move(self, screen, game):
		input = screen.getch()
		if input == curses.KEY_RIGHT:
			self.game.move_right()
		elif input == curses.KEY_LEFT:
			self.game.move_left()
		elif input == curses.KEY_UP:
			self.game.move_up()
		elif input == curses.KEY_DOWN:
			self.game.move_down()

	def end_game(self):
		screen.clear()
		state = ("game %s, press any key to exit "
			% ["over", "completed"][self.game.state - 1])
		screen.addstr(curses.LINES // 2, 0, state.center(curses.COLS))
		screen.refresh()
		time.sleep(2)
		screen.getch()

	def set_curses(self):
		curses.curs_set(0)
		curses.noecho()

	def set_colors(self, colors = None):
		if colors == None:
			colors = self.colors
		for i in range(len(colors)):
			curses.init_pair(i + 1, colors[i], curses.COLOR_BLACK)

	def set_variables(self):
		self.y_start = (curses.LINES - self.y_game) // 2
		self.x_start = (curses.COLS - self.x_game) // 2
		if self.y_start < 3 or self.x_start < 3:
			raise ValueError("screen too small for game size")

	def set_game(self):
		self.set_curses()
		self.set_colors()
		self.set_variables()

	def game_loop(self, screen):
		self.set_game()
		while self.game.state == self.game.ONGOING:
			self.print_game(screen, self.game, str(self.game.score))
			self.get_next_move(screen, self.game)
		end_game()

	def start_game(self):
		print('game start')
		curses.wrapper(self.game_loop)
		print('game end')
