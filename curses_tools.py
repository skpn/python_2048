
import curses
import time
import textwrap

# functions and classes used with the ncurses library

def start_curses():
	stdscr = curses.initscr()
	curses.noecho()
	curses.cbreak()
	stdscr.keypad(True)
	return stdscr

def end_curses():
	curses.nocbreak()
	stdscr.keypad(False)
	curses.echo()
	curses.endwin()

def curses_aligned_write(stdscr, message, pos_y = "center", pos_x = "center",
	ulcorner = 0, line_len = 0, size_y = curses.LINES, size_x = curses.COLS):
	if line_len == 0:
		line_len = min(len(message), 70, (size_x) // 3)
	message = textwrap.wrap(message, line_len)
	if pos_y == "upper":
		y = ulcorner + 1
	elif pos_y == "center":
		y = ulcorner +  size_y // 2 - len(message) // 2
	else:
		y = ulcorner +  size_y - len(message)
	if pos_x == "left":
		x = ulcorner +  1
	elif pos_x == "center":
		x = ulcorner +  (size_x - line_len) // 2
	else:
		x = ulcorner +  size_x - line_len - 1
	for lines in message:
		stdscr.addstr(y, x, lines)
		y = y + 1

class Grid:
	'''A square grid with a minimum space grid cell on each side'''
	def __init__(self, stdscr, size, cell_size_y = 3, cell_size_x = 6):
		self.screen = stdscr
		self.cell_size_y = cell_size_y
		self.cell_size_x = cell_size_x
		self.size_y = cell_size_y * size + size - 1
		self.size_x = cell_size_x * size + size - 1
		self.start_y = (curses.LINES - self.size_y) // 2
		self.start_x = (curses.COLS - self.size_x) // 2
		if (self.size_y + (self.cell_size_y * 2) > curses.LINES
			or self.size_x + (self.cell_size_x * 2) > curses.COLS):
			raise ValueError ('Window too small for grid (lower square size or '
				'grid size')

	def print_grid_lines(self):
		''' prints the raw grid lines '''
		for y in range(self.start_y, self.start_y + self.size_y + 2):
			for x in range(self.start_x, self.start_x + self.size_x + 2):
				if (y - self.start_y) % (self.cell_size_y + 1) == 0:
					self.screen.addch(y, x, curses.ACS_HLINE, curses.A_BOLD)
				elif (x - self.start_x) % (self.cell_size_x + 1) == 0:
					self.screen.addch(y, x, curses.ACS_VLINE, curses.A_BOLD)

	def print_grid_border_line(self, y, left_char, middle_char, right_char):
		''' adds specific characters at the corners and intersections of the
			grid'''
		self.screen.addch(y, self.start_x, left_char, curses.A_BOLD)
		for x in range(self.start_x + self.cell_size_x + 1,
			self.start_x + self.size_x, self.cell_size_x + 1):
			self.screen.addch(y, x, middle_char, curses.A_BOLD)
		self.screen.addch(y, self.start_x + self.size_x + 1, right_char,
			curses.A_BOLD)

	def print_grid(self):
		self.print_grid_lines()
		self.print_grid_border_line(self.start_y, curses.ACS_ULCORNER,
			curses.ACS_TTEE, curses.ACS_URCORNER)
		for y in range(self.start_y + self.cell_size_y + 1,
			self.start_y + self.size_y, self.cell_size_y + 1):
			self.print_grid_border_line(y, curses.ACS_LTEE, curses.ACS_PLUS,
				curses.ACS_RTEE)
		self.print_grid_border_line(self.start_y + self.size_y + 1,
			curses.ACS_LLCORNER, curses.ACS_BTEE, curses.ACS_LRCORNER)
