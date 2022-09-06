# Path-visualizer-in-python
Application which visualizes various pathfinding algorithms, including *A Star Search* or *Breadth First Search*. Made in Python with the use of module [pygame](https://www.pygame.org/).

# Table of contents
- [Setup](#setup)
- [Requirements](#requirements)
- [Controls](#controls)
- [How to visualize algorithm](#how-to-visualize-algorithm)
- [Design the board](#design-the-board)
- [Algorithms](#algorithms)
- [Generate Mazes](#maze-generation)

# Setup
- Firstly, see [requirements](#requirements). The program cannot be run without them
- Start **``run.pyw``** file to run the program.
- In the main menu, choose algorithm and heuristic (heurestic is used only for *A Star Search*)
- Click **``Go To Board``** to start experimenting

# Requirements:
  - [Python 3.x](https://www.python.org/downloads/)
  - modules:
    - [pygame](https://www.pygame.org/)

# Controls
- **``LEFT MOUSE CLICK``** for drawing start / end / wall node
- **``RIGHT MOUSE CLICK``** for deleting start / end / wall node
- **``SPACE``** to start the pathfinding
- **``R``** to clear board
- **``BACKSPACE``** to go to menu
- **``ESCAPE``** to exit program
- **``M``** to generate maze using [Recursive Division](#recursive-division)
- **``N``** to generate maze using [Randomized Depth First Search](#randomized-depth-first-search)

  
# How to visualize algorithm / maze generation
Click on the **tick-box** in the bottom-right corner of the board window to have algorithm or maze generation visualized.

# Design the board
The board can be styled with the ``config_constants.py`` file. See the file and change node properties according to your desires.

# Algorithms
- ### ``A Star Search``
    - One of the fastest algorithms to find the shortest path between two points
    - Uses [heuristics](#heuristics) to find the path more effectively then [Dijkstra's algorithm](#dijkstras-algorithm)
    - **Always gurantees the shortest path** (if path exists)
- ### ``Dijkstra's algorithm``
    - TO BE IMPLEMENTED
- ### ``Depth First Search``
    - As the name of the algorithm says, this algorithm firstly visits all nodes into depth and then comes back to visit the others
    - **Does not gurantee the shortest path!**
- ### ``Breadth First Search``
    - Analogical to [Depth First Search](#depth-first-search)
    - Firstly visits all nodes near by and then visits the others
    - **Gurantees the shortest path only if all nodes have the same cost of travel** (e.g. travelling from one node to the other costs only 1 point)
- ### ``Bogo Search``
    - TO BE IMPLEMENTED

# Maze Generation
- ### ``Randomized Depth First Search``
    - Starts with all nodes as walls
    - Uses [Depth First Search](#depth-first-search), but in randomized order
    - Randomly decides whether to visit a node or not
- ### ``Recursive division``
    - Starts with plain board
    - Divides board with two perpendicular walls into four smaller boards and visits them [recursively](https://en.wikipedia.org/wiki/Recursion_(computer_science))
    - Looks objectively cooler than [Randomized Depth First Search](#randomized-depth-first-search)

# Heuristics
- ### TODO
    
### Enjoy.

- [MrJoeKr](https://github.com/MrJoeKr)
