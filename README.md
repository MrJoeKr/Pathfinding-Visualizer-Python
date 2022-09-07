# Path-visualizer-in-python
- Application which [visualizes](#how-to-visualize-algorithm--maze-generation) various pathfinding algorithms, including [*A Star Search*](#a-star-search), [*Depth First Search*](#depth-first-search) and others
- Visualizes [maze generation](#maze-generation) as well
- Made in Python with the use of module [pygame](https://www.pygame.org/).

# Table of contents
- [Setup](#setup)
- [Requirements](#requirements)
- [Controls](#controls)
- [How to visualize algorithm / maze](#how-to-visualize-algorithm--maze-generation)
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
Click on the **tick-box** in the *bottom-right corner* of the *board window* to have algorithm or maze generation visualized.

# Design the board
The board can be styled with the ``config_constants.py`` file. See the file and change node properties according to your desires.

# Algorithms
- ### A Star Search
    - One of the fastest algorithms to find the shortest path between two points
    - Uses [heuristics](#heuristics) to find the path more effectively then [Dijkstra's algorithm](#dijkstras-algorithm)
    - **Always gurantees the shortest path** (if path exists)
- ### Dijkstra's algorithm
    - Since the cost of travel between nodes (in current version) is only ``1``, the algorithm behaves in the same manner as [Breadth First Search](#breadth-first-search).
    - However, [A Star Search](#a-star-search) is just a variation of this algorithm
    - **Always gurantees the shortest path** (if path exists)
- ### Depth First Search
    - As the name of the algorithm says, this algorithm firstly visits all nodes into depth and then comes back to visit the others
    - **Does not gurantee the shortest path!**
- ### Breadth First Search
    - Analogical to [Depth First Search](#depth-first-search)
    - Firstly visits all nodes near by and then visits the others
    - **Gurantees the shortest path only if all nodes have the same cost of travel** (e.g. travelling from one node to the other costs only 1 point)
- ### Bogo Search
    - Inspiration from [Bogosort](https://en.wikipedia.org/wiki/Bogosort)
    - It's a variation of [Dijkstra's Algorithm](#dijkstras-algorithm), but randomly decides which node to visit first

# Maze Generation
See [controls](#controls) to know how to generate a maze.

These are the algorithms for maze generation:

- ### Randomized Depth First Search
    - Starts with all nodes as walls
    - Uses [Depth First Search](#depth-first-search), but in randomized order
    - Randomly decides whether to visit a node or not
- ### Recursive division
    - Starts with plain board
    - Divides board with two perpendicular walls into four smaller boards and visits them [recursively](https://en.wikipedia.org/wiki/Recursion_(computer_science))
    - Looks objectively cooler than [Randomized Depth First Search](#randomized-depth-first-search)

# Heuristics
Heuristics only work for [A Star Search](#a-star-search) and are used to make [Dijsktra's algorithm](#dijkstras-algorithm) effective and faster in average. These are the implemented ones:

- ### Manhattan Distance
    - According to [definition](https://xlinux.nist.gov/dads/HTML/manhattanDistance.html): 
        - *The distance between two points measured along axes at right angles. In a plane with p1 at (x1, y1) and p2 at (x2, y2), it is |x1 - x2| + |y1 - y2|.*
    - Simply put, the formula above is used as a heuristic to find solution
    - Works nicely in a 2d board
    - **Gurantees shortest path**
- ### Euclidian Distance
    - According to [definition](https://xlinux.nist.gov/dads/HTML/euclidndstnc.html): 
        - *The straight line distance between two points. In a plane with p1 at (x1, y1) and p2 at (x2, y2), it is √((x1 - x2)² + (y1 - y2)²).*
    - Simply put, it calculates the "air distance" between two points
    - **Gurantees shortest path**
- ### Hamming Distance
    - According to [definition](https://xlinux.nist.gov/dads/HTML/HammingDistance.html): 
        - *The number of bits which differ between two binary strings. More formally, the distance between two strings A and B is ∑ | Ai - Bi |.*
    - This heuristic is more effectively used in other problems (e.g. in [Sliding Tiles](https://visualstudiomagazine.com/articles/2015/10/30/sliding-tiles-c-sharp-ai.aspx))
    - In this case, it calculates the total number of different bits between ``x`` and ``y`` coordinates
    - Creates nice patterns ([visualize](#how-to-visualize-algorithm--maze-generation) by yourself)
    - **Gurantees shortest path**
    
### Enjoy.

- [MrJoeKr](https://github.com/MrJoeKr)
