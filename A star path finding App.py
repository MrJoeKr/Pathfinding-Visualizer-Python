import pygame

pygame.init()

w = 803
h = 605
display = pygame.display.set_mode((w,h))
pygame.display.set_caption('A star tracking app')
mainClock = pygame.time.Clock()

BLACK = (0,0,0)
WHITE = (255,255,255)

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


def main():
	running = True
	clicks = []
	plains = []
	sub_plains = []
	walls = []
	CLEAR = True
	while running:

		display.fill(BLACK)

		left_pressed, middle_pressed, right_pressed = pygame.mouse.get_pressed()
		mx, my = pygame.mouse.get_pos()
		clicks.append((mx,my))
		

		# draws board
		for i in range(44):
			for j in range(33):
				plain_rect = plain(5+i*18,5+j*18)
				sub_plains.append(plain_rect)
				if len(sub_plains) > 44*33: # prevent freezing
					del sub_plains[-1:]

		if CLEAR: # list of plain rectangles
			plains = list(sub_plains)
			sub_plains.clear()
			CLEAR = False

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				pygame.quit()
				quit()
			if left_pressed: # left click - drawing walls
				for pl in plains:
					if pl.collidepoint(mx,my):
						plains.remove(pl)
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

		pygame.display.update()
		mainClock.tick(60)


main()
