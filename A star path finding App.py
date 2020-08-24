import pygame
import numpy as np
import time
import threading

pygame.init() # initializing

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

w = 800
h = 650
display = pygame.display.set_mode((w,h))
pygame.display.set_caption('A star tracking app')
mainClock = pygame.time.Clock()

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,242,0)
RED = (231,0,0)
LIGHT_GREEN = (126, 186, 0)
BLUE = (94, 182, 202)
LIGHTER_GREEN = (15, 216, 92)

children_rects = []
closed_rects = []

def draw_text()

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

	def get_rect(self):
		a = 15
		x = self.position[1] * 18 + 5 
		y = self.position[0] * 18 + 5
		rect = pygame.Rect(x,y,a,a)
		return rect

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
	start = [start[1],start[0]]
	end = [end[1],end[0]]
	start_node = Node(None, tuple(start))
	start_node.g = start_node.f = start_node.h = 0
	end_node = Node(None, tuple(end))
	end_node.g = end_node.f = end_node.h = 0

	open_list = [] # list with unvisited nodes 
	closed_list = [] # list with visited nodes

	open_list.append(start_node)

	num_rows, num_cols = np.shape(maze) # number of rows and columns of maze

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

	# loop to end node
	while len(open_list) > 0:
                
		current_node = open_list[0]
		current_index = 0
		for index,item in enumerate(open_list): # find 'the best' node
			if item.f < current_node.f:
				current_node = item
				current_index = index

		open_list.pop(current_index)
		closed_list.append(current_node)

		if current_node == end_node: # found end node
			return return_path(current_node, maze)

		# create children from all adjacent squares
		children = []

		for move in moves:
			
			node_position = (current_node.position[0] + move[0], current_node.position[1] + move[1])

			# check if possible (boundaries)
			if (node_position[0] > (num_rows - 1)) or node_position[0] < 0 \
			or node_position[1] > ((num_cols - 1) or node_position[1] < 0):
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
			child.h = (((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2))
			child.f = child.g + child.h

			# check if child is already in open_list and g is already lower
			if len([i for i in open_list if child == i and child.g > i.g]) > 0:
				continue

			# add children to open list and loop again
			open_list.append(child)

	if len(open_list) == 0:
		print('Impossible')

def search_with_steps(maze,start,end):

	global children_rects
	global closed_rects

	start = [start[1],start[0]]
	end = [end[1],end[0]]
	start_node = Node(None, tuple(start))
	start_node.g = start_node.f = start_node.h = 0
	end_node = Node(None, tuple(end))
	end_node.g = end_node.f = end_node.h = 0

	open_list = [] # list with unvisited nodes 
	closed_list = [] # list with visited nodes

	open_list.append(start_node)

	num_rows, num_cols = np.shape(maze) # number of rows and columns of maze

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

	children_rects = [] # for drawing possible children
	closed_rects = []

	# loop to end node
	while len(open_list) > 0:
                
		current_node = open_list[0]
		current_index = 0
		for index,item in enumerate(open_list): # find 'the best' node
			if item.f < current_node.f:
				current_node = item
				current_index = index

		open_list.pop(current_index)
		closed_list.append(current_node)

		if current_node == end_node: # found end node
			return return_path(current_node, maze)


		# create children from all adjacent squares
		children = []


		for move in moves:
			
			node_position = (current_node.position[0] + move[0], current_node.position[1] + move[1])

			# check if possible (boundaries)
			if (node_position[0] > (num_rows - 1)) or node_position[0] < 0 \
			or node_position[1] > ((num_cols - 1) or node_position[1] < 0):
				continue

			# walls -> 1-s
			if maze[node_position[0]][node_position[1]] != 0:
				continue

			# create new children node
			new_node = Node(current_node, node_position)
			children.append(new_node)

			# draw possible children and closed rectangles
			for child in open_list:
				rect = child.get_rect()
				if rect not in children_rects:
					children_rects.append(rect)

			for done in closed_list:
				done_rect = done.get_rect()
				if done_rect not in closed_rects:
					closed_rects.append(done_rect)

			time.sleep(0.03)
			
			

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
			child.h = (((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2))
			child.f = child.g + child.h

			# check if child is already in open_list and g is already lower
			if len([i for i in open_list if child == i and child.g > i.g]) > 0:
				continue

			# add children to open list and loop again
			open_list.append(child)

	if len(open_list) == 0:
		print('Impossible')


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
	x = (point_rect.x-5) // 18
	y = (point_rect.y-5) // 18
	return (x,y)


def main():
	global children_rects
	global closed_rects
	running = True
	plains = []
	sub_plains = []
	walls = []
	points = []
	path_list = []
	CLEAR = True
	choose_start = True
	choose_end = False
	choose_walls = False
	start_choosed = False
	end_choosed = False
	once = True
	done = False
	while running:

		display.fill(BLACK)

		left_pressed, middle_pressed, right_pressed = pygame.mouse.get_pressed()
		mx, my = pygame.mouse.get_pos()
		

		# draws plain
		for i in range(33):
			for j in range(44):
				plain_rect = plain(5+j*18,5+i*18)
				sub_plains.append(plain_rect)
				if len(sub_plains) > 44*33: # prevent freezing
					del sub_plains[-1:]

		if CLEAR: # list of plain rectangles
			plains = list(sub_plains)
			maze_1d = [0 for i in range(44*33)]
			CLEAR = False

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				pygame.quit()
				quit()
			if left_pressed: 
				# firstly = choose start and end point
				for pl in plains:
					if pl.collidepoint(mx,my):
						if choose_start: # renders text 'Choose starting point', gives ability to choose it
							choose_start = False
							start_choosed = True
							start_rect = draw_point(pl.x,pl.y,GREEN)
							start_rect_pos = plains.index(pl)
							plains[start_rect_pos] = start_rect

						if choose_end:
							end_rect_pos = plains.index(pl)
							if end_rect_pos != start_rect_pos:
								choose_end = False
								end_choosed = True
								choose_walls = True
								end_rect = draw_point(pl.x,pl.y,RED)
								plains[end_rect_pos] = end_rect

			# left click - drawing walls
				if choose_walls:
					for pl in plains:
						if pl.collidepoint(mx,my):
							wall_pos = plains.index(pl)
							if wall_pos != end_rect_pos and wall_pos != start_rect_pos:
								maze_1d[wall_pos] = 1
								wall_rect = wall(pl.x,pl.y)
								walls.append(wall_rect)
								left_pressed = False


			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_BACKSPACE: # clear walls and remake plains - list
					walls.clear()
					plains.clear()
					path_list.clear()
					children_rects.clear()
					closed_rects.clear()
					CLEAR = True

					choose_start = True
					choose_end = False
					once = True
					start_choosed = False
					end_choosed = False
					done = False
					path = None

				if start_choosed and end_choosed:
					if event.key == pygame.K_SPACE: # Start A* algorithm
						start = get_point_pos(start_rect)
						end = get_point_pos(end_rect)
						maze_2d = np.reshape(maze_1d,(33,44))
						#path = search(maze_2d, start, end)
						path = threading.Thread(target=search_with_steps,args=(maze_2d, start, end))
						path.start()
						#path = search_with_steps(maze_2d, start, end)
						done = True
						choose_walls = False

						#print('\n'.join([''.join(["{:" ">3d}".format(item) for item in row]) for row in maze_2d]))

						#print()

						#print('\n'.join([''.join(["{:" ">3d}".format(item) for item in row]) for row in path]))


		# draws walls
		for wl in walls:
			pygame.draw.rect(display,BLACK,wl)

		
		if start_choosed:
			if once:
				choose_end = True
				once = False
			pygame.draw.rect(display,GREEN,start_rect)
		if end_choosed: 
			pygame.draw.rect(display,RED,end_rect)

		'''
		if done: 
			for row in path:
				for num in row:
					if num > 0:
						y = path.index(row) * 18 + 5
						x = row.index(num) * 18 + 5
						path_rect = draw_point(x,y,LIGHT_GREEN)
						path_list.append(path_rect)
				done = False
		'''
		if path_list:
			for rect in path_list:
				if rect != path_list[-1]:
					pygame.draw.rect(display,LIGHT_GREEN,rect)
		
		for child in children_rects:
				pygame.draw.rect(display,BLUE,child)

		for done in closed_rects:
			pygame.draw.rect(display,LIGHTER_GREEN,done)


		pygame.display.update()
		mainClock.tick(60)


main()


# tick box if you want to see how the algorithm works
# ENTER - start finding
