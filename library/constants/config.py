import library.constants.color as color

DISPLAY_WIDTH = 800
DISPLAY_HEIGTH = 650

FPS = 120

# Nodes count ROWS * COLS
ROWS = 40
COLS = 53

# all possible moves from one square to another
MOVES = [
    (0, -1),  # up
    (1, 0),  # right
    (0, 1),  # down
    (-1, 0),  # left
    # (1, -1),  # up right
    # (1, 1),  # down right
    # (-1, 1),  # down left
    # (-1, -1)  # up left
]

# The delay needs to be bigger than the time of the path-finding algorithm
SHOW_STEPS_DELAY = 0.001
# Debugging purposes - very slow
# SHOW_STEPS_DELAY = 0.07
SHOW_PATH_DELAY = 0.005

# Node properties
NODE_SIZE = 15
FOREGROUND_PADDING = 0.5
WALL_COLOR = color.BLACK
NODE_COLOR = color.WHITE
NODE_BORDER_COLOR = color.GRAY

# Visualizing path
OPEN_NODES_COLOR = color.LIGHT_BLUE
# CLOSED_NODES_COLOR = color_constants.LIGHT_GREEN
CLOSED_NODES_COLOR = (64, 117, 21)
PATH_NODES_COLOR = color.GOLDEN

START_POINT_COLOR = color.GREEN
# START_POINT_COLOR = (24, 38, 249)
END_POINT_COLOR = color.RED
