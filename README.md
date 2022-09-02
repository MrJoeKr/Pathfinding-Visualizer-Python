# Path-visualizer-in-python
Application which visualizes various pathfinding algorithms, including *A Star Search* or *Breadth First Search*. Made in Python with the use of module [pygame](https://www.pygame.org/).

# Table of contents
- [Setup](#setup)
- [Requirements](#requirements)
- [Controls](#controls)
- [How to visualize algorithm](#how-to-visualize-algorithm)
- [Design the board](#design-the-board)

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
  - **LEFT MOUSE CLICK** for drawing start / end / wall node
  - **RIGHT MOUSE CLICK** for deleting start / end / wall node
  - **SPACE** to start the path finding
  - **"R"** to clear board
  - **BACKSPACE** to go to menu
  - **ESCAPE** to exit program

  
# How to visualize algorithm
Click on the **tick-box** in the bottom-right corner of board window to have algorithm visualized.
    

# Design the board
The board can be styled with the ``config_constants.py`` file. See the file and change node properties according to your desires.
    
### Enjoy.

- [MrJoeKr](https://github.com/MrJoeKr)
