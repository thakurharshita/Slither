import pygame
import random
pygame.init()

width = 1000
height = 600

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Slither")

img = pygame.image.load("SNAKEHEAD.png")
img_2 = pygame.image.load("SNAKEBODY.png")
icon = pygame.image.load("icon1.png")
appleimg = pygame.image.load("APPLE.png")

pygame.display.set_icon(icon)

green = (0, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

bite = pygame.mixer.Sound('bite-small.wav')
crash = pygame.mixer.Sound('slime10.wav')

clock = pygame.time.Clock()

apple = 30
block = 20
FPS = 15

direction = "right"


extrasmallfont = pygame.font.SysFont("comicsansms", 25)
smallfont = pygame.font.SysFont("comicsansms", 30)
largefont = pygame.font.SysFont("comicsansms", 75)


def pause():

	paused = True

	message_to_screen("PAUSED", white, -280, size = "xsmall")
	message_to_screen("PRESS P TO CONTINUE OR Q TO QUIT", white, -240, size = "xsmall")

	pygame.display.update()		

	while paused:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
					paused = False
				if event.key == pygame.K_q:
					pygame.quit()

		clock.tick(10)

def score(score):
	text = extrasmallfont.render("SCORE: " + str(score), True, white)
	win.blit(text, [0, 0])
	

def randapplegen():
	randappleX = round(random.randrange(0, width - apple))
	randappleY = round(random.randrange(0, height - apple))

	return randappleX, randappleY


def game_intro():

	pygame.mixer.music.load("Around the Bend.WAV")
	pygame.mixer.music.play(-1)

	intro = True

	while intro:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					intro = False
				if event.key == pygame.K_q:
					pygame.quit()		


		win.fill(black)
		message_to_screen("WELCOME TO SLITHER", green, -150, size = "large")
		message_to_screen("YOU WILL HAVE TO EAT APPLES TO SURVIVE", white, -10, size = "small")
		message_to_screen("THE MORE APPLES YOU EAT THE LONGER YOU GROW", white, 40,size = "small")
		message_to_screen("IF YOU RUN INTO THE EDGES OR INTO YOURSELF, YOU DIE", white, 90, size = "small")
		message_to_screen("PRESS C TO PLAY, Q TO QUIT OR P TO PAUSE", white, 180, size = "small")
		pygame.display.update()

		clock.tick(10)


def snake(block, snakelist):

	if direction == "right":
		head = pygame.transform.rotate(img, 270)

	if direction == "left":
		head = pygame.transform.rotate(img, 90)
		
	if direction == "up":
		head = img
		
	if direction == "down":
		head = pygame.transform.rotate(img, 180)	

	win.blit(head, (snakelist[-1][0], snakelist[-1][1]))

	for XnY in snakelist[:-1]:
		win.blit(img_2, [XnY[0], XnY[1], block, block])

def text_objects(text, color, size):
	if size == "small":
		textsurface = smallfont.render(text, True, color)
	elif size == "large":
		textsurface = largefont.render(text, True, color)
	elif size == "xsmall":
		textsurface = extrasmallfont.render(text, True, color)		

	return textsurface, textsurface.get_rect()

def message_to_screen(msg, color, y_displace=0, size = "small"):
	textsurface, textrect = text_objects(msg, color, size)
	textrect.center = (width / 2), (height / 2)+y_displace
	win.blit(textsurface, textrect)

def gameloop():

	pygame.mixer.music.stop()
	pygame.mixer.music.load("Catch The Mystery.WAV")
	pygame.mixer.music.play(-1)


	global direction
	g_exit = False
	g_over = False

	x = width / 2
	y = height / 2

	xchange = 0
	ychange = 0

	snakelist = []
	snakelength = 1

	randappleX, randappleY = randapplegen()	

	while  not g_exit:

		if g_over == True:

			pygame.mixer.music.stop()

			message_to_screen("YOU LOSE", red, 240, size = "xsmall")
			message_to_screen("PRESS C TO PLAY AGAIN OR Q TO QUIT", green, 280, size = "xsmall")
			pygame.display.update()


		while g_over == True:
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					g_exit = True
					g_over = False
				if event.type == pygame.KEYDOWN:
					if event.key ==  pygame.K_q:
						g_exit = True
						g_over = False
					if event.key == pygame.K_c:
						g_over = False
						gameloop()


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				g_exit = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT or event.key == pygame.K_a:
					direction = "left"
					xchange = -block
					ychange = 0
				if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
					direction = "right"
					xchange = block
					ychange = 0
				if event.key == pygame.K_UP or event.key == pygame.K_w:
					direction = "up"
					xchange = 0
					ychange = -block
				if event.key == pygame.K_DOWN or event.key == pygame.K_s:
					direction = "down"
					xchange = 0
					ychange = block
				if event.key == pygame.K_p:
					pause()	


		if x >= width or x < 0 or y >= height or y < 0:
			g_over = True
			pygame.mixer.Sound.play(crash)


		y += ychange
		x += xchange

		win.fill(black)
		win.blit(appleimg, [randappleX, randappleY])

		snakehead = []
		snakehead.append(x)
		snakehead.append(y)
		snakelist.append(snakehead)

		if len(snakelist) > snakelength:
			del snakelist[0]

		for eachsegment in snakelist[:-1]:
			if eachsegment == snakehead:
				g_over = True
				pygame.mixer.Sound.play(crash)
	

		snake(block, snakelist)

		score(snakelength-1)

		pygame.display.update()

		if x > randappleX and x < randappleX + apple or x + block > randappleX and x + block < randappleX + apple:

			if y > randappleY and y < randappleY + apple:

				randappleX, randappleY = randapplegen()	
				pygame.mixer.Sound.play(bite)
				snakelength += 1

			elif y + block > randappleY and y + block < randappleY + apple:

				randappleX, randappleY = randapplegen()	
				pygame.mixer.Sound.play(bite)
				snakelength += 1


		clock.tick(FPS)	

	pygame.quit()

game_intro()
gameloop()