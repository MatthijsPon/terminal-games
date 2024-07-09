import queue
import time
from terminal_games.common import draw_screen_layout
import terminal_games.config as conf
from terminal_games.entity import User, Enemy, Bullet


def num_bullets(object_list):
    count = 0
    for obj in object_list:
        if isinstance(obj, Bullet) and obj.entity.visible:
            count += 1
    return count


def process_move(move, state, config, screen):
    if move == 'left':
        screen.addstr(config.max_inner_y + 3, 0, ' ' * 20)
        screen.addstr(config.max_inner_y + 3, 0, 'left')
        state['objects']['user'][0].move_horizontal(-1, config.min_inner_x, config.max_inner_x)
    elif move == 'right':
        state['objects']['user'][0].move_horizontal(1, config.min_inner_x, config.max_inner_x)
        screen.addstr(config.max_inner_y + 3, 0, ' ' * 20)
        screen.addstr(config.max_inner_y + 3, 0, 'right')
    elif move == 'shoot':
        if num_bullets(state['objects']['objects']) < config.max_bullets:
            state['objects']['objects'].append(Bullet('|', state['objects']['user'][0].entity.x, state['objects']['user'][0].entity.y - 1, 10))
        screen.addstr(config.max_inner_y + 3, 0, ' ' * 20)
        screen.addstr(config.max_inner_y + 3, 0, 'shoot')
    else:
        screen.addstr(config.max_inner_y + 3, 0, ' ' * 20)
        screen.addstr(config.max_inner_y + 3, 0, f'pressed: {move}')

    return state


def visuals(screen, state, keyboard, config):
    try:
        move = keyboard.get(False)
        state = process_move(move, state, config, screen)
    except queue.Empty:
        screen.addstr(config.max_inner_y + 4, 0, 'empty')
        pass

    screen.addstr(config.max_inner_y + 2, 0, str(state['objects']['user'][0].entity.return_entity()))

    for sublist in ['user', 'enemies', 'objects']:
        new_list = []
        for obj in state['objects'][sublist]:
            if obj.entity.visible:
                screen.addstr(*obj.entity.return_entity())
                new_list.append(obj)
            elif sublist == 'enemies':
                state['score'] += obj.score
        state['objects'][sublist] = new_list

    write_score(screen, config, state)
    screen.refresh()

    for sublist in ['user', 'enemies', 'objects']:
        for obj in state['objects'][sublist]:
            screen.addstr(*obj.entity.return_empty())

    for sublist in ['enemies', 'objects']:
        for obj in state['objects'][sublist]:
            if sublist == 'enemies':
                obj.step(state['ticks'], config.min_inner_x, config.max_inner_x, config.min_inner_y, config.max_inner_y)
                if obj.check_game_over(config.max_inner_y):
                    msg = 'You Died!'
                    screen.addstr(config.max_inner_y // 2, config.max_x // 2 - len(msg) // 2, msg)
                    screen.refresh()
                    time.sleep(2)
                    return False, state
            else:
                obj.step(state['ticks'], config.min_inner_y, config.max_inner_y)
    # Check collisions
    for obj in state['objects']['objects']:
        for enemy in state['objects']['enemies']:
            if obj.check_collision(enemy):
                obj.visible = False
                enemy.visible = False
                screen.addstr(obj.y, obj.x, 'X')

    if len(state['objects']['enemies']) <= 0:
        msg = 'You Win!'
        screen.addstr(config.max_inner_y // 2, config.max_x // 2 - len(msg) // 2, msg)
        screen.refresh()
        time.sleep(2)
        return False, state

    # screen.addstr(0, 0, str(state['ticks']))
    state['ticks'] += 1
    return True, state


def write_score(screen, config, state):
    screen.addstr(config.min_y, config.min_x + 7, str(state['score']))


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
