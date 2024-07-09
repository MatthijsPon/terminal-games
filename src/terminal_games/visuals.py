import logging
import queue
import curses
import time
import terminal_games.config as conf
import terminal_games.space_invaders as si


def center_message(screen, config, message, y, *args):
    x = config.max_x // 2 - len(message) // 2
    screen.addstr(y, x, message, *args)


def show_options(screen, config, options, highlight_key, y_offset):
    for key, value in options.items():
        if key == highlight_key:
            center_message(screen, config, ' ' + value + ' ', y_offset + key, curses.color_pair(1))
        else:
            center_message(screen, config, ' ' + value + ' ', y_offset + key)
    screen.refresh()


def clear_screen(screen, config):
    for i in range(config.max_y):
        screen.addstr(i, 0, " " * (config.max_x - 1))
    screen.refresh()


def fit_message(screen, message, max_x, max_y):
    logging.info('test ' + str(max_y) + ' ' + str(max_x))
    for y in range(max_y):
        screen.addstr(y, 0, message[max_x * y: max_x * (y + 1)])
        if max_x * (y + 1) > len(message):
            break


def startup_error(screen, config, message):
    """Try to fit an error on screen, log it and raise it."""
    logging.error(message)
    if config.max_x * config.max_y < len(message):
        message = message.split('.')[0]
    fit_message(screen, message, config.max_x, config.max_y)
    screen.refresh()
    time.sleep(5)
    raise EnvironmentError(message)


def homescreen(screen, keyboard, status):
    """Shows home screen, containing selection of games."""
    config = conf.Config()
    check = config.startup_check()
    if check is not None:
        startup_error(screen, config, check)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    center_message(screen, config, 'Select Game', 0)
    center_message(screen, config, 'Press space to continue', 2)
    # center_message(screen, config, 'Press Ctrl+D to exit', 3)
    options = {
        0: 'Space Invaders',
        1: 'Exit',
    }
    cur_option = 0
    show_options(screen, config, options, cur_option, 5)
    while True:
        try:
            move = keyboard.get(False)
            if move == 'shoot':
                break
            elif move == 'up':
                if cur_option > 0:
                    cur_option -= 1
                    show_options(screen, config, options, cur_option, 5)
            elif move == 'down':
                if cur_option < len(options) - 1:
                    cur_option += 1
                    show_options(screen, config, options, cur_option, 5)

        except queue.Empty:
            pass
        try:  # Check if fork has quit
            cur_status = status.get(False)
            if cur_status:
                exit(0)
        except queue.Empty:
            pass
    clear_screen(screen, config)
    if cur_option == 0:
        si.run(screen, keyboard, status, config)
    else:
        exit(0)

