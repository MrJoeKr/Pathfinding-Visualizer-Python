from collections import deque
import time
from typing import Any, Callable, Deque, Optional, Tuple

from color_constants import Color
from config_constants import CLOSED_NODES_COLOR, END_POINT_COLOR, OPEN_NODES_COLOR, SHOW_STEPS_DELAY, START_POINT_COLOR
from node_board_object import NodeBoard
from node_object import Node

DrawDeque = Deque[Tuple[Color, Node]]

class NodeQueue:

    def __init__(self):
        self._queue: DrawDeque = deque()
        # For threading purposes
        self._can_visualize: bool = True

    def push(self, node: Node, color: Color) -> None:
        self._queue.append((color, node))

    def popleft(self) -> Tuple[Color, Node]:
        return self._queue.popleft()

    def push_closed_node(self, node: Node) -> None:
        self._queue.append((CLOSED_NODES_COLOR, node))

    def push_open_node(self, node: Node) -> None:
        self._queue.append((OPEN_NODES_COLOR, node))

    def start_draw(self, draw_func: Optional[Callable[[Node, Color], None]] = None, do_while: Callable[[], bool] = lambda: True) -> None:
        while self.can_visualize() and do_while():

            if not self._queue:
                # Prevent lag
                time.sleep(0.2)
                continue

            color, node = self.popleft()

            # print(f"Drawing: {(color, node)}")

            # TODO -> make pop up animation better
            # node.draw_pop_up_animation(color)

            # Default
            if draw_func is None:
                node.draw_node(color)

            else:
                draw_func(node, color)

            # Speed of drawing
            time.sleep(SHOW_STEPS_DELAY)

    def stop_visualizing(self) -> None:
        self._can_visualize = False

    def can_visualize(self) -> bool:
        return self._can_visualize

    def clear(self) -> None:
        self._queue.clear()

    def empty(self) -> bool:
        return len(self._queue) == 0