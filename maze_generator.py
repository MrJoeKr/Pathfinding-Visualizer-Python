from node_board_object import NodeBoard
from maze_algorithms import MazeFunction


class MazeGenerator:

    def __init__(self, maze_func: MazeFunction) -> None:
        self.maze_func = maze_func

    def generate_maze(self, board: NodeBoard) -> None:
        print("Generating maze")
        self.maze_func(board)
        print("Generating ended")
