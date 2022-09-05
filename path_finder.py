from collections import deque
import threading
import time
from typing import Optional
from color_constants import Color
from config_constants import END_POINT_COLOR, SHOW_STEPS_DELAY, START_POINT_COLOR
from node_board_object import NodeBoard
from node_draw_queue import NodeQueue
from node_object import Node
from path_finding_algorithm import SearchFunction, HeuristicFunction, search_a_star, manhattan_distance


class PathFinder:
    def __init__(
        self,
        search_func: SearchFunction = search_a_star,
        heuristic: Optional[HeuristicFunction] = manhattan_distance,
        show_steps: bool = False,
    ) -> None:

        self.search_func: SearchFunction = search_func
        self.heuristic: Optional[HeuristicFunction] = heuristic
        self.show_steps = show_steps

        self.finding_path_finished = False

        # For drawing path
        self._draw_queue: Optional[NodeQueue] = NodeQueue()

    def start_search(self, board: NodeBoard) -> bool:
        """
        General function for finding path between two nodes in NodeBoard

        Starts new thread when board.show_steps is True

        Parameters
        ---
        board : NodeBoard

        Returns
        ---
        True if path was found else False

        """

        if not self.show_steps:
            # Threading not needed
            self.search_func(board, None, self.heuristic)

        else:
            self._draw_queue = NodeQueue()

            thread = threading.Thread(
                target=self.search_func,
                args=(board, self._draw_queue, self.heuristic))
            thread.start()

            def _draw_func(node: Node, color: Color) -> None:
                node.draw_node(color)

                if node is board.start_node:
                    node.draw_as_circle(START_POINT_COLOR)

                elif node is board.end_node:
                    node.draw_as_circle(END_POINT_COLOR)

            # Draw nodes
            self._draw_queue.start_draw(draw_func=_draw_func, do_while=lambda: not self._draw_queue.empty())

        self.finding_path_finished = True
        board.finding_path_finished = True

        return board.solution_found()

    def stop_visualizing(self) -> None:
        if self._draw_queue is not None:
            self._draw_queue.stop_visualizing()
