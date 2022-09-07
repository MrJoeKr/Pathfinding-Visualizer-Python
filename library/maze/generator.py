import threading
from library.node.board import NodeBoard
from library.maze.algorithms import MazeFunction
from library.node.draw_queue import NodeQueue


class MazeGenerator:

    def __init__(self, maze_func: MazeFunction, show_steps: bool = False) -> None:
        self.maze_func = maze_func
        self.show_steps = show_steps

        # For threading purposes
        self._can_visualize = True

    def generate_maze(self, board: NodeBoard) -> None:

        if board.start_node is None or board.end_node is None:
            board.set_default_start_end()

        # print(self.show_steps)

        # print("Generating maze")

        if not self.show_steps:
            self.maze_func(board, None)
            board.update_screen()
        
        else:
            # Showing steps
            draw_queue: NodeQueue = NodeQueue()

            threading.Thread(target=self.maze_func, args=(board, draw_queue)).start()

            # maze_func is responsible for stopping drawing
            draw_queue.start_draw(do_while=self.can_visualize)

            # print("Drawing finished")

        # print("Generating ended")

        board.start_node.draw_start_node()
        board.end_node.draw_end_node()

    def can_visualize(self) -> bool:
        return self._can_visualize

    def stop_visualize(self) -> None:
        self._can_visualize = False
