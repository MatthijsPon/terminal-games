import curses
from terminal_games.main import main


if __name__ == '__main__':
    curses.wrapper(main)
