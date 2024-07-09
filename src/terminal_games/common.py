def draw_screen_layout(screen, config):
    screen.addstr(config.min_y, config.min_x, 'Score:')
    for i in range(config.min_inner_x, config.max_inner_x + 1):  # Hor lines
        screen.addstr(config.min_inner_y - 1, i, '-')
        screen.addstr(config.max_inner_y + 1, i, '-')

    for i in range(config.min_inner_y, config.max_inner_y + 1):  # Vert lines
        screen.addstr(i, config.min_inner_x - 1, '|')
        screen.addstr(i, config.max_inner_x + 1, '|')
    screen.refresh()
