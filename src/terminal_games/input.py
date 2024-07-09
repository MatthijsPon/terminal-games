import queue
import sys
import termios
import tty
import signal
import terminal_games.config as conf
EOT = '\x04'  # CTRL+D
ESC = '\x1b'
CSI = '['
CTC = '^C'


def getchar():
    fd = sys.stdin.fileno()
    attr = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)  # read 1 byte
    finally:
        termios.tcsetattr(fd, termios.TCSANOW, attr)


def process_input(q, status, timeout):
    c = getchar()
    if c == EOT:
        status.put('exit')
        return False
    elif c == '^C':  # This doesn't work
        raise KeyboardInterrupt
    elif c in ['C', 'd']:
        q.put('right', timeout=timeout)
    elif c in ['D', 'a']:
        q.put('left', timeout=timeout)
    elif c in ['A', 'w']:
        q.put('up', timeout=timeout)
    elif c in ['B', 's']:
        q.put('down', timeout=timeout)
    elif c == ' ':
        q.put('shoot')
    else:
        q.put(c)
    return True


def run_with_timeout(func, timeout):
    signal.signal(signal.SIGALRM)


def input_tick(q, status_poll, status_visual):
    config = conf.Config()
    timeout = config.timeout
    run = True
    while run:
        try:
            stop = status_visual.get(False)
            if stop:
                raise ConnectionError('Visuals quit.')
        except queue.Empty:
            pass

        # TODO this is blocking, so only exists upon keypress
        #  maybe a keypress needed?
        run = process_input(q, status_poll, timeout)
