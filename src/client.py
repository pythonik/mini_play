import curses
def main():
	win = curses.initscr()
	win.addstr(0, 0, 'this a cool player')
	win.refresh()
	win.getch()
	curses.endwin()
if __name__ == '__main__':
	main()
