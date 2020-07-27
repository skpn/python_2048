
import curses
import time


def main(screen):
	colors = [0] + list(range(22, 52)) + list(reversed(range(124, 142)))
	for i in range(len(colors)):
		curses.init_pair(i + 1, colors[i], curses.COLOR_BLACK)
		screen.addstr(str(i).center(3), curses.color_pair(i + 1))
	# for i in range(len_colors):
	# 	curses.init_pair(i + 1, curses.COLOR_BLACK, colors[i])
	# 	screen.addstr(str(i).center(3), curses.color_pair(i + 1))
	screen.getch()

curses.wrapper(main)