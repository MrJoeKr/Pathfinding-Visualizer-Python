from collections import deque
import threading
import time
from typing import Optional
from config_constants import END_POINT_COLOR, SHOW_STEPS_DELAY, START_POINT_COLOR
from node_board_object import NodeBoard
from path_finding_algorithm import DrawDeque, SearchFunction, HeuristicFunction


class PathFinder:
    def __init__(
        self,
        search_func: SearchFunction,
        heuristic: Optional[HeuristicFunction] = None,
        show_steps: bool = True,
    ) -> None:

        self.search_func: SearchFunction = search_func
        self.heuristic: Optional[HeuristicFunction] = heuristic
        self.show_steps = show_steps

    # General function for finding path between two nodes in NodeBoard
    def start_search(self, board: NodeBoard) -> None:

        if not self.show_steps:
            # Threading not needed
            self.search_func(board, None, self.heuristic)

        else:
            draw_queue: DrawDeque = deque()

            thread = threading.Thread(
                target=self.search_func, args=(board, draw_queue, self.heuristic)
            )
            thread.start()

            # Draw nodes
            while draw_queue:
                color, node = draw_queue.popleft()

                # TODO -> make pop up animation better
                # node.draw_pop_up_animation(color)

                node.draw_node(color)

                if node is board.start_node:
                    node.draw_as_circle(START_POINT_COLOR)

                if node is board.end_node:
                    node.draw_as_circle(END_POINT_COLOR)

                # Speed of drawing
                time.sleep(SHOW_STEPS_DELAY)

        board.finding_path_finished = True
