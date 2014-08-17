import curses
def main():
	win = curses.initscr()
        dims = win.getmaxyx()
	win.addstr(dims[0]/2, dims[1]/2, 'this a cool player')
	win.refresh()
	win.getch()
	curses.endwin()
if __name__ == '__main__':
	main()
