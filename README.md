# Path-visualizer-in-python
- An application which [visualizes](#how-to-visualize-algorithm--maze-generation) various pathfinding algorithms, including [*A Star Search*](#a-star-search), [*Depth First Search*](#depth-first-search) and others
- Visualizes [maze generation](#maze-generation) as well
- Made in Python with the use of the module [pygame](https://www.pygame.org/).

# Table of contents
- [Setup](#setup)
- [Requirements](#requirements)
- [Controls](#controls)
- [How to visualize algorithm/maze](#how-to-visualize-algorithm--maze-generation)
- [Design the board](#design-the-board)
- [Algorithms](#algorithms)
- [Generate Mazes](#maze-generation)

# Setup
- Firstly, see [requirements](#requirements). The program cannot be run without them
- Start the **``run.pyw``** file to run the program.
- In the main menu, choose the algorithm and heuristic (heuristic is used only for *A Star Search*)
- Click **``Go To Board``** to start experimenting

# Requirements:
```console
pip install -r requirements.txt
```
  - [Python 3.X](https://www.python.org/downloads/)
  - modules:
    - [pygame](https://www.pygame.org/)

# Controls
- **``LEFT MOUSE CLICK``** for drawing a start/end/wall node
- **``RIGHT MOUSE CLICK``** for deleting a start/end/wall node
- **``SPACE``** to start the pathfinding
- **``R``** to clear the board
- **``BACKSPACE``** to go to the menu
- **``ESCAPE``** to exit the program
- **``M``** to generate a maze using [Recursive Division](#recursive-division)
- **``N``** to generate a maze using [Randomized Depth First Search](#randomized-depth-first-search)

  
# How to visualize algorithm/maze generation
Click on the **tick-box** in the *bottom-right corner* of the *board window* to have the algorithm or maze generation visualized.

# Design the board
The board can be styled with the ``config_constants.py`` file. See the file and change node properties according to your desires.

# Algorithms
- ### A Star Search
    - One of the fastest algorithms to find the shortest path between two points
    - Uses [heuristics](#heuristics) to find the path more effectively than [Dijkstra's algorithm](#dijkstras-algorithm)
    - **Always guarantees the shortest path** (if the path exists)
- ### Dijkstra's algorithm
    - Since the cost of travel between nodes (in current version) is only ``1``, the algorithm behaves in the same manner as [Breadth First Search](#breadth-first-search).
    - However, [A Star Search](#a-star-search) is just a variation of this algorithm
    - **Always guarantees the shortest path** (if the path exists)
- ### Depth First Search
    - As the name of the algorithm says, this algorithm first visits all nodes in depth and then comes back to visit the others
    - **Does not guarantee the shortest path!**
- ### Breadth-First Search
    - Analogical to [Depth First Search](#depth-first-search)
    - Firstly visits all nodes near by and then visits the others
    - **Guarantees the shortest path only if all nodes have the same cost of travel** (e.g. travelling from one node to the other costs only 1 point)
- ### Bogo Search
    - Inspiration from [Bogosort](https://en.wikipedia.org/wiki/Bogosort)
    - It's a variation of [Dijkstra's Algorithm](#dijkstras-algorithm), but randomly decides which node to visit first

# Maze Generation
See the [controls](#controls) to know how to generate a maze.

These are the algorithms for maze generation:

- ### Randomized Depth First Search
    - Starts with all nodes as walls
    - Uses [Depth First Search](#depth-first-search) but in randomized order
    - Randomly decides whether to visit a node or not
- ### Recursive division
    - Starts with a plain board
    - Divides the board with two perpendicular walls into four smaller boards and visits them [recursively](https://en.wikipedia.org/wiki/Recursion_(computer_science))
    - Looks objectively cooler than [Randomized Depth First Search](#randomized-depth-first-search)

# Heuristics
Heuristics only work for [A Star Search](#a-star-search) and are used to make [Dijsktra's algorithm](#dijkstras-algorithm) effective and faster on average. These are the implemented ones:

- ### Manhattan Distance
    - According to the [definition](https://xlinux.nist.gov/dads/HTML/manhattanDistance.html): 
        - *The distance between two points is measured along axes at right angles. In a plane with $p_1$ at $(x_1, y_1)$ and $p_2$ at $(x_2, y_2)$, it is $|x_1 - x_2| + |y_1 - y_2|$.*
    - Simply put, the formula above is used as a heuristic to find solution
    - Works nicely in a 2d board
    - **Guarantees shortest path**
- ### Euclidian Distance
    - According to the [definition](https://xlinux.nist.gov/dads/HTML/euclidndstnc.html): 
        - *The straight line distance between two points. In a plane with $p_1$ at $(x_1, y_1)$ and $p_2$ at $(x_2, y_2)$, it is $\sqrt{((x_1 - x_2)^2 + (y_1 - y_2)^2)}$.*
    - Simply put, it calculates the "air distance" between two points
    - **Guarantees shortest path**
- ### Hamming Distance
    - According to the [definition](https://xlinux.nist.gov/dads/HTML/HammingDistance.html): 
        - *The number of bits that differ between two binary strings. More formally, the distance between two strings of length $n$ A and B is $\sum_{i=1}^n{| A_i - B_i |}$.*
    - This heuristic is more effectively used in other problems (e.g. in [Sliding Tiles](https://visualstudiomagazine.com/articles/2015/10/30/sliding-tiles-c-sharp-ai.aspx))
    - In this case, it calculates the total number of different bits between ``x`` and ``y`` coordinates
    - Creates nice patterns ([visualize](#how-to-visualize-algorithm--maze-generation) by yourself)
    - **Guarantees shortest path**
    
### Enjoy.

- [MrJoeKr](https://github.com/MrJoeKr)
