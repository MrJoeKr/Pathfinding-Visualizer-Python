import pygame
import numpy as np

pygame.init() # initializing

w = 800
h = 600
display = pygame.display.set_mode((w,h))
pygame.display.set_caption('A star tracking app')
mainClock = pygame.time.Clock()

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,242,0)
RED = (231,0,0)

# A* algorithm	
class Node(): 
	# class for nodes - white rectangles
	# 3 variables - g,h,f
	# f = g + h
	def __init__(self, parent=None, position=None):
		self.parent = parent
		self.position = position
		self.g = 0
		self.h = 0
		self.f = 0

	def __eq__(self,other):
		# check equality with another node
		return self.position == other.position

def return_path(current_node, maze):
	# returns the path of the search function
	path = []
	num_rows, num_cols = np.shape(maze) # the shape of maze
	result = [[-1 for i in range(num_cols)] for j in range(num_rows)]
	current = current_node
	while current is not None: # loops until the end node
		path.append(current.position)
		current = current.parent

	path = path[::-1] # reverse path - we went from end to start so we have to reverse it
	start_value = 0
	
	for i in range(len(path)):
		result[path[i][0]][path[i][1]] = start_value
		start_value += 1
	return result

def search(maze, start, end): # cost -> value of one transition

	start_node = Node(None, tuple(start))
	start_node.g = start_node.f = start_node.h = 0
	end_node = Node(None, tuple(end))
	end_node.g = end_node.f = end_node.h = 0

	open_list = [] # list with unvisited nodes 
	closed_list = [] # list with visited nodes

	open_list.append(start_node)

	iterations = 0
	max_iterations = (len(maze)//2)**10

	num_rows, num_cols = np.shape(maze) # number of rows and columns of maze

	# loop to end node
	while len(open_list) > 0:
                
		iterations += 1

		current_node = open_list[0]
		current_index = 0
		for index,item in enumerate(open_list): # find 'the best' node
			if item.f < current_node.f:
				current_node = item
				current_index = index

		if iterations > max_iterations: # if too many iterations
			print('Too many iterations.')
			return return_path(current_node,maze)

		open_list.pop(current_index)
		closed_list.append(current_node)

		if current_node == end_node: # found end node
			return return_path(current_node, maze)

		# all possible moves from one square to another
		moves = [
		[0,-1], # up
		[1,0], # right
		[0,1], # down
		[-1,0], # left
		[1,-1], # up right
		[1,1], # down right
		[-1,1], # down left
		[-1,-1] # up left
		]

		# create children from all adjacent squares
		children = []

		for move in moves:
			
			node_position = (current_node.position[0] + move[0], current_node.position[1] + move[1])

			# check if possible (boundaries)
			if node_position[0] > (num_rows - 1) or node_position[0] < 0 \
			or node_position[1] > (num_cols - 1) or node_position[1] < 0:
				continue

			# walls -> 1-s
			if maze[node_position[0]][node_position[1]] != 0:
				continue

			# create new children node
			new_node = Node(current_node, node_position)
			children.append(new_node)

		for child in children:
			# check if in closed list
			if child in closed_list:
				continue

			#change the value of cost when diagonal child
			cost = 1
			if current_node.position[0] - child.position[0] != 0 and current_node.position[1] - child.position[1] != 0:
				cost = 2

			# otherwise create initialize values
			child.g = current_node.g + cost
			child.h = (child.position[0] ** 2 - end_node.position[0] ** 2) + (child.position[1] ** 2 - end_node.position[1] ** 2)
			child.f = child.g + child.h

			# check if child is already in open_list and g is already lower
			if len([i for i in open_list if child == i and child.g > i.g]) > 0:
				continue

			# add children to open list and loop again
			open_list.append(child)


# environment

def plain(x,y):
	a = 15
	plain_rect = pygame.Rect(x,y,a,a)
	pygame.draw.rect(display,WHITE,plain_rect)
	return plain_rect

def wall(x,y):
	a = 15
	wall_rect = pygame.Rect(x,y,a,a)
	pygame.draw.rect(display,BLACK,wall_rect)
	return wall_rect

def draw_point(x,y, color):
	a = 15
	point_rect = pygame.Rect(x,y,a,a)
	pygame.draw.rect(display,color,point_rect)
	return point_rect

def get_point_pos(point_rect):
	return (point_rect.x, point_rect.y)


def main():
	running = True
	plains = []
	sub_plains = []
	walls = []
	points = []
	CLEAR = True
	choose_start = True
	choose_end = False
	while running:

		display.fill(BLACK)

		left_pressed, middle_pressed, right_pressed = pygame.mouse.get_pressed()
		mx, my = pygame.mouse.get_pos()
		

		# draws plain
		for i in range(44):
			for j in range(33):
				plain_rect = plain(5+i*18,5+j*18)
				sub_plains.append(plain_rect)
				if len(sub_plains) > 44*33: # prevent freezing
					del sub_plains[-1:]

		if CLEAR: # list of plain rectangles
			plains = list(sub_plains)
			maze = [0 for i in range(44*33)]
			CLEAR = False

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				pygame.quit()
				quit()
			if left_pressed: 
				# firstly = choose start and end point
				if choose_start: # renders text 'Choose starting point', gives ability to choose it
					choose_start = False
					for pl in plains:
						if pl.collidepoint(mx,my):
							point_rect = draw_point(pl.x,pl.y,GREEN)
							points.append(point_rect)
							plains.remove(pl)


			# left click - drawing walls
				for pl in plains:
					if pl.collidepoint(mx,my):
						pos = plains.index(pl)
						maze[pos] = 1
						wall_rect = wall(pl.x,pl.y)
						walls.append(wall_rect)


			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_BACKSPACE: # clear walls and remake plains - list
					walls.clear()
					plains.clear()
					CLEAR = True

		# draws walls
		for wl in walls:
			pygame.draw.rect(display,BLACK,wl)

		for point in points:
			pygame.draw.rect(display,point)

		pygame.display.update()
		mainClock.tick(60)


main()


# learn A* algorithm
# starting, ending point (A,B)
# tick box if you want to see how the algorithm works
# ENTER - start finding
