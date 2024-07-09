import threading as th
import queue as q
import curses
import logging
import datetime
from terminal_games.input import input_tick
from terminal_games.visuals import homescreen


def main(screen):
    """Starts Visual (main) and Keyboard thread (daemon)"""
    # logging.basicConfig(filename=f'/tmp/terminal_games_{datetime.datetime.now().strftime("%Y_%m_%d_%H.%M.%S")}.log')
    logging.basicConfig(filename=f'./terminal_games.log', level=logging.INFO, filemode='w+')
    curses.curs_set(0)
    keyboard = q.Queue(1)
    status_visual = q.Queue(1)
    status_poll = q.Queue(1)
    t = th.Thread(target=input_tick, args=(keyboard, status_visual, status_poll), daemon=True)
    t.start()
    homescreen(screen, keyboard, status_visual)


if __name__ == '__main__':
    curses.wrapper(main)
