import copy

def restartButton(init_gs):
    print('hii')
    mouse_clicked = 0
    mouse_x = 'a'
    mouse_y = 'a'
    possible_dropped_square = 'a'
    gs = copy.deepcopy(init_gs)

    return mouse_clicked, mouse_x, mouse_y, possible_dropped_square, gs