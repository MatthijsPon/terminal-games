from terminal_games.common import draw_screen_layout
from terminal_games.entity import Ticked


class Snake(Ticked):
    movement = 'up'

    def step(self, ticks, min_y, max_y):
        if self.movement == 'down':
            self.move_vertical(1, min_y, max_y)
        elif self.movement == 'right':
            self.move_horizontal(1, min_x, max_x)
        elif self.movement == 'left':
            self.move_horizontal(-1, min_x, max_x)
        else:
            self.move_vertical(-1, min_y, max_y)

    def change_movement(self, move):
        self.movement = move


def run(screen, keyboard, status, config):
    started = True
    draw_screen_layout(screen, config)
    state = {
        'ticks': 0,
        'score': 0,
        'objects': {
            'user': [User('^', config.max_inner_x // 2, config.max_inner_y)],
            'enemies': [Enemy('#', config.min_inner_x + i, config.min_inner_y, 30, 100) for i in range(10)],
            'objects': [],
        },
    }
    while started:
        # This is one tick
        start_seconds = time.time()
        started, state = visuals(screen, state, keyboard, config)
        try:  # Check if fork has quit
            cur_status = status.get(False)
            if cur_status:
                break
        except queue.Empty:
            pass
        end_seconds = time.time()
        diff = end_seconds - start_seconds
        if diff < 1 / config.max_tps:
            time.sleep(1 / config.max_tps - diff)
