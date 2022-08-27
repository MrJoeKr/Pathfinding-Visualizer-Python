import color_constants

DISPLAY_WIDTH = 800
DISPLAY_HEIGTH = 650

FPS = 60

# Nodes count
ROWS = 40
COLS = 53

# The delay needs to be bigger than the time of the path-finding algorithm
SHOW_STEPS_DELAY = 0.001
SHOW_PATH_DELAY = 0.01

# Node properties
NODE_SIZE = 15
FOREGROUND_PADDING = 0.5
WALL_COLOR = color_constants.BLACK
NODE_COLOR = color_constants.WHITE
NODE_BORDER_COLOR = color_constants.GRAY

# Visualizing path
OPEN_NODES_COLOR = color_constants.LIGHT_GREEN
CLOSED_NODES_COLOR = color_constants.LIGHT_BLUE
PATH_NODES_COLOR = color_constants.GOLDEN

START_POINT_COLOR = color_constants.GREEN
END_POINT_COLOR = color_constants.RED
