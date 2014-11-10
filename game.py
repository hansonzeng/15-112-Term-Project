 # from player import*
import random,time
import pygame, sys
from pygame.locals import*
import math


pygame.init()


# Blue Monster http://icons.iconarchive.com/icons/spoon-graphics/monster
#/512/Blue-Monster-icon.png
class MonsterBlue(pygame.sprite.Sprite):
	def __init__(self,width,height):
		pygame.sprite.Sprite.__init__(self) # calls parent class
		# (Sprite) constructor
		self.width,self.height = width,height
		self.image = pygame.image.load('images/Blue-Monster.png').convert_alpha()
		self.image = pygame.transform.scale(self.image,(20,20)) 
		self.rect = self.image.get_rect()
		self.rect.x = random.randint(0,width)
		self.rect.y = random.randint(0,height)
		self.speed,self.direction = 2,random.random()*math.pi*2
		self.counter = 0

	def move(self): # Move and dx, dy obtained from NewGame.py in Hmk 9
		self.rect.x = (self.rect.x + self.dx()) % self.width
		self.rect.y = (self.rect.y + self.dy()) % self.height

	def dx(self):
		return math.cos(self.direction) * self.speed

	def dy(self):
		return math.sin(self.direction) * self.speed

	def delay(self):
		self.delay -= 1
		if self.delay == 5: return True
		if self.delay == 0: self.delay = 6

# Red Monster http://www.clker.com/cliparts/P/k/2/t/6/1/pink-and-
#blue-monster-md.png
class MonsterRed(pygame.sprite.Sprite):
	def __init__(self,width,height):
		pygame.sprite.Sprite.__init__(self)
		self.width,self.height = width,height
		self.image = pygame.image.load('images/redMonster.png').convert_alpha()
		self.image = pygame.transform.scale(self.image,(20,20))
		self.rect = self.image.get_rect()
		self.rect.x = random.randint(0,width)
		self.rect.y = random.randint(0,height)
		self.speed = 1
		self.count = 0
		self.timeDelay = 0
		self.justCollided = False

	def findPlayer(self,player,otherRed):
		if self.rect.x < player.rect.x and self.avoidOverlap(otherRed): 
			self.rect.x += self.speed
		elif self.rect.x > player.rect.x and self.avoidOverlap(otherRed): 
			self.rect.x -= self.speed
		if self.rect.y < player.rect.y and self.avoidOverlap(otherRed): 
			self.rect.y += self.speed
		elif self.rect.y > player.rect.y and self.avoidOverlap(otherRed):
			self.rect.y -= self.speed

	def avoidOverlap(self,otherRed):
		if otherRed == None: return True
		dSquared = (self.rect.x-otherRed.rect.x)**2 + \
		(self.rect.y-otherRed.rect.y)**2
		d = dSquared**(1/2.0)
		if d < 35: return False
		else: return True

	def updateMonster(self,player,otherMonster):
		self.findPlayer(player,otherMonster)
		self.rect.x = self.rect.x % self.width
		self.rect.y = self.rect.y % self.height

#Orange Monster http://www.clker.com/cliparts/f/G/d/N/J/q/monster-pac-md.png
class MonsterOrange(MonsterRed):
	def __init__(self,width,height):
		super(MonsterOrange,self).__init__(width,height)
		self.image = pygame.image.load('images/orangeMonster.png').convert_alpha()
		self.image = pygame.transform.scale(self.image,(20,20))

	def checkToExplode(self,player):
		dSquared = (player.rect.x-self.rect.x)**2 + (player.rect.y-self.rect.y)**2
		d = dSquared**(1/2.0)
		if d < 120: return True
		else:	return False

# Bullet Pink Monster http://blog.spoongraphics.co.uk/wp-content/uploads
#/2009/furry-monster/monster.jpg
class MonsterBullets(pygame.sprite.Sprite):
	def __init__(self,tempx,tempy):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('images/pinkMonster.png').convert_alpha()
		self.image = pygame.transform.scale(self.image,(10,10))
		self.rect = self.image.get_rect()
		self.rect.x = tempx
		self.rect.y = tempy
		self.speed = 5
		self.direction = [i*math.pi/2 for i in xrange(4)]

	def explosion(self,direction):# direction from 0 to 4
		self.number = direction % 4
		self.rect.x = self.rect.x + self.changex()
		self.rect.y = self.rect.y + self.changey()

	def changex(self):
		return math.cos(self.direction[self.number]) * self.speed

	def changey(self):
		return math.sin(self.direction[self.number]) * self.speed

# Pink Monster http://blog.spoongraphics.co.uk/wp-content/uploads
#/2009/furry-monster/monster.jpg
class MonsterPink(MonsterRed):
	def __init__(self,width,height):
		super(MonsterPink,self).__init__(width,height)
		self.image = pygame.image.load('images/pinkMonster.png').convert_alpha()
		self.image = pygame.transform.scale(self.image,(20,20))

	def almostEqual(self,d1,d2):
		epsilon = 0.00001
		return (abs(d2-d1) < epsilon)

	def findPlayer(self,player,otherPink):
		if self.rect.x < player.rect.x and self.avoidOverlap(otherPink): 
			self.rect.x += self.speed
		elif self.rect.x > player.rect.x and self.avoidOverlap(otherPink): 
			self.rect.x -= self.speed
		if self.almostEqual(self.rect.x,player.rect.x) and \
		self.rect.y > player.rect.y and self.avoidOverlap(otherPink):
			self.rect.y -= self.speed
		elif self.almostEqual(self.rect.x,player.rect.x) and\
		 self.rect.y < player.rect.y and self.avoidOverlap(otherPink):
			self.rect.y += self.speed

# Green Monster http://4.bp.blogspot.com/-SlgUJTkjEHI/\
#TTff7_Aj1RI/AAAAAAAAAaY/YXy1gkE7rGY/s1600/green_climate_monster-263x300.png
class MonsterGreen(MonsterRed):
	def __init__(self,width,height):
		super(MonsterGreen,self).__init__(width,height)
		self.image = pygame.image.load('images/greenMonster.png').convert_alpha()
		self.image = pygame.transform.scale(self.image,(20,20))
		self.speed = 2


class Dot(pygame.sprite.Sprite):
	def __init__(self,pos):
		pygame.sprite.Sprite.__init__(self)
		self.radius = 5
		self.thickness = 5
		color = (200,100,155)
		self.image = pygame.Surface((10,10))
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.rect.x = pos[0]
		self.rect.y = pos[1]
		self.collideDirec = ''


	def collision(self,monsterList):
		for monster in monsterList:
			if pygame.sprite.collide_rect(self,monster):# if collision
				self.monster = monster
				if monster.dx() < 0 and monster.dy() < 0 and \
				self.rect.x < monster.rect.x: # collision on right
					self.collideDirec = 'right'
				elif monster.dx() < 0  and monster.dy() > 0 and \
				self.rect.x < monster.rect.x: # collision on right
					monster.direction = math.pi - monster.direction
					self.collideDirec = 'right'
				elif monster.dx() > 0 and monster.dy() > 0 and \
				self.rect.x > monster.rect.x: # collision on left
					self.collideDirec = 'left'
				elif monster.dx() > 0 and monster.dy() < 0 and \
				self.rect.x > monster.rect.y: # collision on left
					self.collideDirec = 'left'
				elif monster.dx() < 0 and monster.dy() < 0 and \
				self.rect.y > monster.rect.y: # collision on top
					self.collideDirec = 'top'
				elif monster.dx() > 0 and monster.dy() < 0 and \
				self.rect.y > monster.rect.y: # collision on top
					self.collideDirec = 'top'
				elif monster.dx() > 0 and monster.dy() > 0 and \
				self.rect.y < monster.rect.y: # collision on bottom
					self.collideDirec = 'bottom'
				else:
					self.collideDirec = 'bottom'
				if self.collideDirec != '':
					return True
				else:
					return False

	def collisionOtherMonsters(self,monsterList,data):
		for monster in monsterList:
			if pygame.sprite.collide_rect(self,monster):
				if monster.timeDelay == 0 and not monster.justCollided:
					monster.timeDelay = data.playtime
				monster.speed = 0
				if data.playtime > (monster.timeDelay + 5):
					if type(monster) == MonsterGreen:
						monster.speed = 2
					else:
						monster.speed = 1
					if data.playtime > (monster.timeDelay + 8):
						monster.justCollided = False
						monster.timeDelay = 0


	def playerCollision(self,player,data):
		if player.dx < 0 and self.rect.x < player.rect.x:
			player.dx = -player.dx
		if player.dx > 0 and self.rect.x > player.rect.x:
			player.dx =-player.dx

 			if player.dy < 0 and self.rect.bottom > player.rect.top:
 				player.dy =-player.dy

 			if player.dy > 0 and self.rect.top < player.rect.bottom:
 				player.dy = -player.dy


	def scrollDots(self): # scrolls dots
		self.rect.x -= 3

	def changeDirection(self):
		if self.collideDirec == 'right':
			self.monster.direction = math.pi - self.monster.direction
		if self.collideDirec == 'left':
			self.monster.direction = math.pi - self.monster.direction
		if self.collideDirec == 'top':
			self.monster.direction = self.monster.direction
		if self.collideDirec == 'bottom':
			self.monster.direction = 2*math.pi - self.monster.direction


class Player(Dot):

	def __init__(self,data,posx,posy,width,height):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.image.load('images/ufo.png').convert_alpha()
		self.image = pygame.transform.scale(self.image,(20,20))
		self.rect = self.image.get_rect()
		self.rect.x = posx
		self.rect.y = posy
		self.width,self.height = width, height
		self.direction = 0 # degrees in radions 
		self.dy,self.dx = 0,0# movements for horziontal and vertical
		self.maxSpeed = 5

	def changeNonAngleVert(self,add):
		self.dy += add
		if self.dy > self.maxSpeed: self.dy = self.maxSpeed
		if self.dy < -self.maxSpeed: self.dy = -self.maxSpeed

	def changeNonAngleHorz(self,add):
		self.dx += add
		if self.dx > self.maxSpeed: self.dx = self.maxSpeed
		if self.dx < -self.maxSpeed: self.dx = -self.maxSpeed
 
	def moveWithoutDir(self):
		self.rect.y = (self.rect.y + self.dy) % self.height
		self.rect.x = (self.rect.x + self.dx) % self.width


class Destination(pygame.sprite.Sprite): # make a destination
	def __init__(self,width,height):
		pygame.sprite.Sprite.__init__(self)
		self.time = pygame.time.get_ticks()
		self.image = pygame.image.load('images/activeDoor.png').convert_alpha()
		self.size = 50 # so as not to go off the screen
		self.rect = self.image.get_rect()
		self.rect.x = random.randint(self.size,width-self.size)
		self.rect.y = random.randint(self.size,height-self.size)
		self.activate = False

	def isActive(self):
		if random.random() < 0.2: # 20 percent chance
			self.activate = True
			return True
		else:
			self.activate = False
			return False

	def teleport(self,data):
		if int(data.drawDoorCounter) % (7*50) == 0:
			self.rect.x = random.randint(0,data.width)
			self.rect.y = random.randint(0,data.height)

	def isCollided(self,data):
		if pygame.sprite.collide_rect(self,data.player):
			data.scoreCounter += 1


class Fonts(object):
	def __init__(self,name,message):
		self.font = name
		self.message = message
		self.size = 30
		self.color = (0,0,0)
		self.newx = 320 # half of screenx
		self.newy = 180 # half of screeny

	def changeSize(self,size):
		self.size = size

	def changeColor(self,color):
		self.color = color

	def changeLocation(self,newx,newy):
		self.newx = newx
		self.newy = newy

	def setNumber(self,number): # only for score messages
		self.message = 'Score: %d' %(number)

	def getRendered(self):
		self.fontLoad = pygame.font.Font(self.font,self.size)
		self.fontRender = self.fontLoad.render(self.message,1,self.color)

	def drawMessage(self,screen):
		screen.blit(self.fontRender,(self.newx,self.newy))

def init(data):
	data.screen = pygame.display.set_mode((640,360),0,32)
	# BELOW ARE FOR IMAGES
	bif = "images/stars.jpg"
	mif = "images/paintBrush.png"
	menuPic = "images/realSpace.jpg"
	gameOverPic = "images/gameOver.jpg"
	instruction1 = 'images/GeneralInstructionScreen.jpg'
	instruction2 = 'images/GeneralInstructionScreen2.jpg'
	instruction3 = 'images/GeneralInstructionScreen3.jpg'

	background = pygame.image.load(bif).convert()
	cursorPic = pygame.image.load(mif).convert_alpha()

	menuScreen = pygame.image.load(menuPic).convert_alpha()
	gameOverScreen = pygame.image.load(gameOverPic).convert_alpha()

	instruction1Screen = pygame.image.load(instruction1).convert_alpha()
	instruction2Screen = pygame.image.load(instruction2).convert_alpha()
	instruction3Screen = pygame.image.load(instruction3).convert_alpha()

	data.menuMessage = []
	menuFont = 'font/Capsmall_clean.ttf'
	menuMessage = ['Play','Instructions','Quit']
	for i in xrange(len(menuMessage)):
		data.menuMessage.append(Fonts(menuFont,menuMessage[i]))

	data.gameTitle = Fonts('font/Prototype.ttf','UFO Painter')
	data.gameOverTitle = Fonts('font/Prototype.ttf','Game Over')
	data.restartMessage = Fonts('font/Prototype.ttf','Click r to restart Game')
	data.scoreBoard = Fonts('font/Prototype.ttf','Score: ')
	data.nextPage = Fonts('font/Prototype.ttf','Press "O" for Next')
	data.nextPage2 = Fonts('font/Prototype.ttf','Press "P" for Next')
	data.playGame = Fonts('font/Prototype.ttf','"Press Enter to Play!"')
	data.timeOut = Fonts('font/Prototype.ttf','Time Out')
	data.win = Fonts('font/Prototype.ttf',"Congratulations! Click 'r' to replay!")

	data.playerSpeed = 5
	data.changeSpeed = 0.1
	data.delay = 20 # used to check delay collision for monsters
	data.width, data.height = 640,360
	data.background = pygame.transform.scale(background,(data.width,data.height))
	data.cursorPic = pygame.transform.scale(cursorPic,(20,20))
	data.menuScreen = pygame.transform.scale(menuScreen,(data.width,data.height))
	data.gameOverScreen = pygame.transform.scale(gameOverScreen,(data.width,data.height))
	data.instruction1Screen = pygame.transform.scale(instruction1Screen,(data.width,data.height))
	data.instruction2Screen = pygame.transform.scale(instruction2Screen,(data.width,data.height))
	data.instruction3Screen = pygame.transform.scale(instruction3Screen,(data.width,data.height))

	#this is a list of only the monsters #http://www.youtube.com/watch?v=4W2AqUetBi4
	data.all_sprites_list = pygame.sprite.Group()

	data.greenMonster_list = pygame.sprite.Group()
	data.pinkMonster_list = pygame.sprite.Group()
	data.orangeMonster_list = pygame.sprite.Group()
	data.monsterBullets_list = pygame.sprite.Group()
	data.redMonster_list = pygame.sprite.Group()
	data.blueMonster_list = pygame.sprite.Group()
	data.path_list = pygame.sprite.Group()

	data.player = Player(data,10,10,data.width,data.height)
	data.all_sprites_list.add(data.player)

	data.destination = Destination(data.width,data.height)
	data.all_sprites_list.add(data.destination)

	for x in xrange(3): # Creates all the blue monsters!
		monster = MonsterBlue(data.width,data.height)
		data.blueMonster_list.add(monster)
		data.all_sprites_list.add(monster)

	createRedMonster(5,data)
	createOrangeMonster(5,data)
	createPinkMonster(5,data)
	createGreenMonster(2,data)


	data.explodex = 0
	data.explodey = 0
	# limit to 60 frames per second
	data.clock = pygame.time.Clock()
	data.FPS = 60
	data.playtime = 0
	data.secondTemp = 0

	data.pause = False
	data.check = False
	data.mouseButtonUp = True
	data.gameOver = False
	data.gameStart = False
	data.instruction1 = False
	data.instruction2 = False
	data.instruction3 = False

	data.drawDoorCounter = 0
	data.scoreCounter = 0
	data.levelCounter = 0


	data.level2 = False
	data.level3 = False
	data.level4 = False
	data.level5 = False
	data.isWin = False


	data.cheat1 = False
	data.cheat2 = False
	data.cheat3 = False
	data.cheat4 = False
	data.cheat5 = False


def createRedMonster(number,data): 
	for x in xrange(number):
		redMonster = MonsterRed(data.width,data.height)
		data.redMonster_list.add(redMonster)

def createOrangeMonster(number,data):
	for x in xrange(number):
		orangeMonster = MonsterOrange(data.width,data.height)
		data.orangeMonster_list.add(orangeMonster)

def createPinkMonster(number,data):
	for x in xrange(number):
		pinkMonster = MonsterPink(data.width,data.height)
		data.pinkMonster_list.add(pinkMonster)

def createGreenMonster(number,data):
	for x in xrange(number):
		greenMonster = MonsterGreen(data.width,data.height)
		data.greenMonster_list.add(greenMonster)


def keyPressed(data): 
	if data.gameStart and not data.gameOver:
		if data.event.type == pygame.KEYDOWN:
			if data.event.key == K_DOWN: # for horz or vert movements
				data.player.changeNonAngleVert(5)
			if data.event.key == K_UP:
				data.player.changeNonAngleVert(-5)
			if data.event.key == K_RIGHT:
				data.player.changeNonAngleHorz(5)
			if data.event.key == K_LEFT:
				data.player.changeNonAngleHorz(-5)
			if data.event.key == K_1:
				data.cheat1 = not data.cheat1
			if data.event.key == K_2:
				data.cheat2 = not data.cheat2
			if data.event.key == K_3:
				data.cheat3 = not data.cheat3
			if data.event.key == K_4:
				data.cheat4 = not data.cheat4
			if data.event.key == K_5:
				data.cheat5 = not data.cheat5
			if data.event.key == K_r:
				init(data)
			if data.event.key == K_x:
				data.level2 = True
			if data.event.key == K_c:
				data.level3 = True
				data.level2 = False
			if data.event.key == K_v:
				data.level4 = True
				data.level3 = False
			if data.event.key == K_b:
				data.level5 = True
				data.level4 = False
			if data.event.key == K_t:
				data.pause = not data.pause


	if data.gameOver:
		if data.event.type == pygame.KEYDOWN:
			if data.event.key == K_r:
				init(data)

	if data.instruction1 == True:
		if data.event.type == pygame.KEYDOWN:
			if data.event.key == K_o:
				data.instruction1 = False
				data.instruction2 = True

	if data.instruction2 == True:
		if data.event.type == pygame.KEYDOWN:
			if data.event.key == K_p:
				data.instruction2 = False
				data.instruction3 = True

	if data.instruction3 == True:
		if data.event.type == pygame.KEYDOWN:
			if data.event.key == K_RETURN:
				data.instruction2 = False
				data.gameStart = True


def mousePressed(data):
	if data.gameStart and not data.gameOver:
		if data.event.type == pygame.MOUSEBUTTONDOWN:
			data.mouseButtonUp = False
		if data.event.type == pygame.MOUSEMOTION:
			if data.mouseButtonUp == False:
				data.path_list.add(Dot(data.event.pos))
				data.all_sprites_list.add(Dot(data.event.pos))
		if data.event.type == pygame.MOUSEBUTTONUP:
			data.mouseButtonUp = True

	elif not data.gameStart and not data.gameOver and not data.instruction1 and not\
	data.instruction2 and not data.instruction3:
		if data.event.type == pygame.MOUSEBUTTONDOWN:
			x,y = pygame.mouse.get_pos()
			if 350<x<420 and data.menuy<y<data.menuy+data.menuAdd:
				data.gameStart = True
			if 350<x<530 and data.menuy+data.menuAdd<y<data.menuy+data.menuAdd*2: 
				data.instruction1 = True
			if 350<x<410 and data.menuy+data.menuAdd*2<y<data.menuy+data.menuAdd*3:
				pygame.quit()
				sys.exit()


	if data.instruction3 == True:
		if data.event.type == pygame.MOUSEBUTTONDOWN:
			x,y = pygame.mouse.get_pos()
			if data.width-200<x<data.width and data.height-50<y<data.height-25:
				data.instruction3 = False
				data.gameStart = True
			

def redrawAll(data):
	menu = data.menuMessage
	data.menux,data.menuy,data.menuAdd =350,115,50
	titlex,titley = 100,20

	x,y = pygame.mouse.get_pos()

# Stuff to draw when game is running
	if data.gameStart and not data.gameOver and not data.pause:
		data.screen.blit(data.background,(0,0))
		data.scoreBoard.changeColor((255,255,255))
		data.scoreBoard.changeLocation(10,0)
		data.scoreBoard.setNumber(data.scoreCounter)
		if data.scoreCounter == 0 or data.scoreCounter > 0:
			data.scoreBoard.changeColor((204,255,255))
		if data.scoreCounter > 100:
			data.scoreBoard.changeColor((102,255,102))
		if data.scoreCounter > 200: 
			data.scoreBoard.changeColor((255,255,0))
		if data.scoreCounter > 300:
			data.scoreBoard.changeColor((255,128,0))
		if data.scoreCounter > 400:
			data.scoreBoard.changeColor((255,51,51))
		data.scoreBoard.getRendered()
		data.scoreBoard.drawMessage(data.screen)

		for item in data.all_sprites_list:
			if data.level3 == True and type(item) == MonsterRed:
				item.kill()
			if data.level4 == True and type(item) == MonsterOrange:
				item.kill()
			if data.level5 == True and type(item) == MonsterPink:
				item.kill()

		if data.isWin:
			data.win.changeLocation(data.width/2-200,data.height/2)
			data.win.changeColor((0,0,255))
			data.win.getRendered()
			data.win.drawMessage(data.screen)

		data.all_sprites_list.draw(data.screen) # draw the monster sprites!

#Stuff to draw when game has ended
	elif not data.gameStart and not data.gameOver:
		if not data.instruction1 and not data.instruction2 and not data.instruction3:
			data.screen.blit(data.menuScreen,(0,0))
			data.gameTitle.changeColor((255,255,255))
			data.gameTitle.changeSize((50))
			data.gameTitle.changeLocation(titlex,titley)
			data.gameTitle.getRendered()
			data.gameTitle.drawMessage(data.screen)
			for i in xrange(len(menu)):
				menu[i].changeLocation(data.menux,data.menuy+data.menuAdd*i)
				if 350<x<420 and data.menuy<y<data.menuy+data.menuAdd: 
					menu[0].changeSize(50)
				else: menu[0].changeSize(30)
				if 350<x<530 and data.menuy+data.menuAdd<y<data.menuy+data.menuAdd*2: menu[1].changeSize(50)
				else: menu[1].changeSize(30)
				if 350<x<410 and data.menuy+data.menuAdd*2<y<data.menuy+data.menuAdd*3: menu[2].changeSize(50)
				else: menu[2].changeSize(30)
				menu[i].getRendered()
				menu[i].drawMessage(data.screen)
		if data.instruction1 == True:
			data.screen.blit(data.instruction1Screen,(0,0))
			data.nextPage.changeLocation(data.width-300,data.height-50)
			data.nextPage.changeSize(15)
			data.nextPage.getRendered()
			data.nextPage.drawMessage(data.screen)
		if data.instruction2 == True:
			data.screen.blit(data.instruction2Screen,(0,0))
			data.nextPage2.changeLocation(data.width-300,data.height-25)
			data.nextPage2.changeSize(15)
			data.nextPage2.getRendered()
			data.nextPage2.drawMessage(data.screen)
		if data.instruction3 == True:
			data.screen.blit(data.instruction3Screen,(0,0))
			data.playGame.changeLocation(data.width-180,data.height-80)
			data.playGame.changeSize(15)
			data.playGame.getRendered()
			data.playGame.drawMessage(data.screen)


	elif data.gameStart and data.gameOver:
		data.screen.blit(data.gameOverScreen,(0,0))
		data.gameOverTitle.getRendered()
		data.gameOverTitle.drawMessage(data.screen)
		data.restartMessage.changeLocation(320,230)
		data.restartMessage.getRendered()
		data.restartMessage.drawMessage(data.screen)

	if data.gameStart and not data.gameOver and data.pause == True:
		data.timeOut.changeLocation(data.width/2-50,data.height/2-20)
		data.timeOut.changeColor((0,0,255))
		data.timeOut.getRendered()
		data.timeOut.drawMessage(data.screen)

	if not data.pause:
		x -= data.cursorPic.get_width()/2
		y -= data.cursorPic.get_height()/2
		data.screen.blit(data.cursorPic,(x,y)) # mouse movement



def update(data):
	if data.gameStart and not data.gameOver and not data.pause:
		data.drawDoorCounter += 1
		data.player.moveWithoutDir()
		data.destination.teleport(data)
		levelToggler(data)
# Iterations between the levels and checks for distance between monsters
		if data.level2 == True:
			for red in data.redMonster_list:
				data.all_sprites_list.add(red)
			temp = None # used for testing monster's proximity to each other
			for redMonster in data.redMonster_list:
				redMonster.updateMonster(data.player,temp)
				temp = redMonster

		if data.level3 == True:
			explosionCount = 0 # for Orange Monsters explosions
			for orange in data.orangeMonster_list:
				data.all_sprites_list.add(orange)
			temp = None
			for orangeMonster in data.orangeMonster_list:
				orangeMonster.updateMonster(data.player,temp)
				temp = orangeMonster
				if orangeMonster.checkToExplode(data.player) == True:
					data.explodex,data.explodey = orangeMonster.rect.x,orangeMonster.rect.y
					orangeMonster.kill()

					for i in xrange(4):
						bullets = MonsterBullets(data.explodex,data.explodey)
						data.monsterBullets_list.add(bullets)
						data.all_sprites_list.add(bullets)

			for bullets in data.monsterBullets_list:
				bullets.explosion(explosionCount)
				explosionCount += 1

			for bullets in data.monsterBullets_list:
					if pygame.sprite.collide_rect(data.player,bullets):
						if data.cheat3 == False:
							data.gameOver = True
					for monster in data.blueMonster_list:
						if pygame.sprite.collide_rect(bullets,monster):
							monster.kill()

		if data.level4 == True:
			for pink in data.pinkMonster_list:
				data.all_sprites_list.add(pink)
			temp = None
			for pinkMonster in data.pinkMonster_list:
				pinkMonster.updateMonster(data.player,temp)
				temp = pinkMonster

		if data.level5 == True:
			for green in data.greenMonster_list:
				data.all_sprites_list.add(green)
			temp = None
			for greenMonster in data.greenMonster_list:
				greenMonster.updateMonster(data.player,temp)
				temp = greenMonster

# Collisions with the player!
		for monster in data.blueMonster_list:
			if pygame.sprite.collide_rect(monster,data.player):
				if data.cheat1 == False:
					data.gameOver = True
			monster.move()

		if data.level2 == True:
			for monster in data.redMonster_list:
				if pygame.sprite.collide_rect(monster,data.player):
					if data.cheat2 == False:
						data.gameOver = True

		if data.level4 == True:
			for monster in data.pinkMonster_list:
				if pygame.sprite.collide_rect(monster,data.player):
					if data.cheat4 == False:
						data.gameOver = True

		if data.level5 == True:
			for monster in data.greenMonster_list:
				if pygame.sprite.collide_rect(monster,data.player):
					if data.cheat5 == False:
						data.gameOver = True


# Collisions with the path
		for path in data.path_list: # monster bouncing 
			if path.collision(data.blueMonster_list):
				check(path.monster) # 
				if path.monster.counter == 0:
					path.monster.counter = 20
					path.changeDirection()
			if data.level2 == True:
				path.collisionOtherMonsters(data.redMonster_list,data)
			if data.level3 == True:
				path.collisionOtherMonsters(data.orangeMonster_list,data)
				for bullets in data.monsterBullets_list:
						if pygame.sprite.collide_rect(path,bullets):
							bullets.speed = -bullets.speed

			if pygame.sprite.collide_rect(path,data.player):
				path.playerCollision(data.player,data)
				data.playerSpeed -= data.changeSpeed

			if data.level4 == True:
				path.collisionOtherMonsters(data.pinkMonster_list,data)

			if data.level5 == True:
				path.collisionOtherMonsters(data.greenMonster_list,data)

# Collision with the destination
		data.destination.isCollided(data)
		

# Helpers for update
def check(monster):# helps delay collision to only react to
# one out of 20 collisions; customize with counter.
	if monster.counter > 0: monster.counter -= 1

def levelToggler(data):
	if data.scoreCounter == 500:
		data.scoreCounter = 0
		data.levelCounter += 1
	if data.levelCounter == 2:
		data.level2 = True
	if data.levelCounter == 3:
		data.level3 = True
		data.level2 = False
	if data.levelCounter == 4:
		data.level4 = True
		data.level3 = False
	if data.levelCounter == 5:
		data.level5 = True
		data.level4 = False
	if data.levelCounter == 6:
		data.level5 = False
		data.cheat2 = True
		data.isWin = True


def run():
	class Struc:pass
	data = Struc()
	init(data)
	while True:
		milliseconds = data.clock.tick(data.FPS)
		data.timeInit = milliseconds/1000.0 # seconds passed since last frame
		data.playtime += data.timeInit 
		pygame.mouse.set_visible(0) # removes the cursor from screen
		for data.event in pygame.event.get():
			if data.event.type == QUIT:
				pygame.quit()
				sys.exit()
			mousePressed(data)
			keyPressed(data)
		update(data)
		redrawAll(data)
		# updates screen with what was drawn
		pygame.display.flip()

run()
