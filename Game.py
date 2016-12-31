from Board import Board
from Piece import Piece
import time
import sys
import pygame
from pygame.locals import *
class GameWork(Board, Piece, object):
	def __init__(self):
		super(GameWork, self).__init__()
		self.setGameVariables()
		self.setShapes()
		self.setColors()
		pass
	def start(self):
		pygame.init()
    		self.FPSCLOCK = pygame.time.Clock()
    		self.Display = pygame.display.set_mode((self.WindowW, self.WindowH))
    		self.SmallFont = pygame.font.Font('ComicSansMs.ttf', 20)
    		self.MediumFont = pygame.font.Font('ComicSansMs.ttf', 40)
    		self.BigFont = pygame.font.Font('ComicSansMs.ttf', 100)
    		pygame.display.set_caption('TETRIS')

    		self.showTextScreen('TETRIS')
    		while True: # game loop
        		self.runGame()
        		self.showTextScreen('Game Over')
		pass
	def runGame(self):
		self.board=self.BlankBoard()
		self.updateScore()
		self.fallingPiece = self.getNewPiece()
		self.nextPiece = self.getNewPiece()
		while True: # game loop
			if self.fallingPiece == None:
				# No falling piece in play, so start a new piece at the top
				self.fallingPiece = self.nextPiece
				self.fallingPiece=self.fallingPiece
				self.nextPiece = self.getNewPiece()
				self.lastFallTime = time.time() # reset lastFallTime

				if not self.isValidPosition(self.board, self.fallingPiece):
					return # can't fit a new piece on the board, so game over

			self.checkForQuit()
			for event in pygame.event.get(): # event handling loop
				if event.type == KEYUP:
					if (event.key == K_p):
						# Pausing the game
						self.Display.fill(self.BgColor)
						self.showTextScreen('Paused') # pause until a key press
						self.lastFallTime = time.time()
						self.lastMoveDownTime = time.time()
						self.lastMoveSidewaysTime = time.time()

					elif (event.key == K_LEFT or event.key == K_a):
						self.movingLeft = False
					elif (event.key == K_RIGHT or event.key == K_d):
						self.movingRight = False
					elif (event.key == K_DOWN or event.key == K_s):
						self.movingDown = False

				elif event.type == KEYDOWN:
					# moving the piece sideways
					if (event.key == K_LEFT or event.key == K_a) and self.isValidPosition(self.board, self.fallingPiece, adjX=-1):
						self.moveleft()

					elif (event.key == K_RIGHT or event.key == K_d) and self.isValidPosition(self.board, self.fallingPiece, adjX=1):
						self.moveright()

					# rotating the piece (if there is room to rotate)

					elif (event.key == K_s):
						self.rotate()
					elif (event.key == K_q): # rotate the other direction
						self.antirotate()

					# making the piece fall faster with the down key
					elif (event.key == K_DOWN) :
						self.down()

					# move the current piece all the way down
					elif event.key == K_SPACE:
						self.space()

			# handle moving the piece because of user input
			if (self.movingLeft or self.movingRight) and time.time() - self.lastMoveSidewaysTime > self.SideFreq:
				if self.movingLeft and self.isValidPosition(self.board, self.fallingPiece, adjX=-1):
					self.fallingPiece['x'] -= 1
				elif self.movingRight and self.isValidPosition(self.board, self.fallingPiece, adjX=1):
					self.fallingPiece['x'] += 1
				self.lastMoveSidewaysTime = time.time()

			if self.movingDown and time.time() - self.lastMoveDownTime > self.DownFreq and self.isValidPosition(self.board, self.fallingPiece, adjY=1):
				self.fallingPiece['y'] += 1
				self.lastMoveDownTime = time.time()


			freq=self.getFreq()
			if time.time() - self.lastFallTime > freq:

				if not self.isValidPosition(self.board, self.fallingPiece, adjY=1):
					# falling piece has landed, set it on the board
					super(GameWork,self).updateScore(10) #since GameWork also has an update score we use the keyword super
					self.addToBoard(self.board, self.fallingPiece,self.PIECES)
					if(self.fallingPiece['shape'] == 'D'):
						super(GameWork,self).updateScore(self.removeSpecialLines()*100)
					elif self.fallingPiece['shape'] == 'E':
						self.removeVerticalLine()
					elif self.fallingPiece['shape'] == 'F':
						self.removeVerticalLine()
						super(GameWork,self).updateScore(self.removeSpecialLines()*100)
					super(GameWork,self).updateScore(self.removeCompleteLines()*100)
					self.updateScore()
					self.fallingPiece = None
				else:
					# if piece did not land, just move the piece down
					self.fallingPiece['y'] += 1
					self.lastFallTime = time.time()

			# drawing all components
			self.Display.fill(self.BgColor)
			self.drawBoard(self.board)
			self.drawStatus()
			self.drawIns()
			self.drawNextPiece(self.nextPiece,self.PIECES)
			if self.fallingPiece != None:
				self.drawPiece(self.fallingPiece)

			pygame.display.update()
			self.FPSCLOCK.tick(self.FPS)

	def terminate(self):
		pygame.quit()
		sys.exit()

	def checkForKeyPress(self):
		# Go through event queue looking for a KEYUP event.
		# Grab KEYDOWN events to remove them from the event queue.
		self.checkForQuit()

		for event in pygame.event.get([KEYDOWN, KEYUP]):
			if event.type == KEYDOWN:
				continue
			return event.key
		return None

	def showTextScreen(self,text):

		titleSurf, titleRect = self.makeTextObjs(text, self.BigFont, self.TextShadowColor)
		titleRect.center = (int(self.WindowW / 2), int(self.WindowH / 2))
		self.Display.blit(titleSurf, titleRect)

		# Draw the text
		titleSurf, titleRect = self.makeTextObjs(text, self.BigFont, self.TextColor)
		titleRect.center = (int(self.WindowW / 2) - 3, int(self.WindowH / 2) - 3)
		self.Display.blit(titleSurf, titleRect)

		# Display score if game is over
		if(text=="Game Over"):
			sc=self.getScore()
			scoretext="Your score is "+str(sc)
			scoreSurf, scoreRect = self.makeTextObjs(scoretext, self.MediumFont, self.TextColor)
			scoreRect.center = (int(self.WindowW / 2), int(self.WindowH / 2) + 70)
			self.Display.blit(scoreSurf, scoreRect)

		# Draw the additional "Press any key to play." text.
		pressKeySurf, pressKeyRect = self.makeTextObjs('Press any key to play.', self.SmallFont, self.TextColor)
		pressKeyRect.center = (int(self.WindowW / 2), int(self.WindowH / 2) + 120)
		self.Display.blit(pressKeySurf, pressKeyRect)

		while self.checkForKeyPress() == None:
			pygame.display.update()
			self.FPSCLOCK.tick()

	def checkForQuit(self):
		for event in pygame.event.get(QUIT): # get all the QUIT events
			self.terminate() # terminate if any QUIT events are present
		for event in pygame.event.get(KEYUP): # get all the KEYUP events
			if event.key == K_ESCAPE:
				self.terminate() # terminate if the KEYUP event was for the Esc key
			pygame.event.post(event) # put the other KEYUP event objects back

	def convertToPixelCoords(self,boxx, boxy):
		# Convert the given xy coordinates of the board to xy
		# coordinates of the location on the screen.
		return (self.Xbound + (boxx * self.BoxSize)), (self.Topbound + (boxy * self.BoxSize))

	def makeTextObjs(self,text, font, color):
	    surf = font.render(text, True, color)
	    return surf, surf.get_rect()

	def setGameVariables(self):
		self.FPS= 25
		self.WindowW= 800
		self.WindowH= 680
		self.BoxSize= 20
		self.BoardW= 20
		self.BoardH= 32
		self.SideFreq= 0.15
		self.DownFreq= 0.1
		self.TemplateW=5
		self.TemplateH=5
		self.Xbound = int((self.WindowW - self.BoardW * self.BoxSize) / 2)
		self.Topbound = self.WindowH - (self.BoardH * self.BoxSize) - 5
		self.BLANK='.'
		pass
	def setColors(self):
		self.White       = (255, 255, 255)
		self.Gray        = (185, 185, 185)
		self.Black       = (  0,   0,   0)
		self.Red         = (155,   0,   0)
		self.LightRed    = (175,  20,  20)
		self.Green       = (  0, 155,   0)
		self.LightGreen  = ( 20, 175,  20)
		self.Blue        = (  0,   0, 155)
		self.LightBlue   = ( 20,  20, 175)
		self.Yellow      = (155, 155,   0)
		self.LightYellow = (175, 175,  20)
		self.Purple      = (255, 51, 255)
		self.LightPurple = (255, 70, 255)
		self.Orange      = (255, 150, 0)
		self.LightOrange = (255, 150, 20)

		self.BorderColor = self.Blue
		self.BgColor = self.Black

		self.TextColor = self.White
		self.TextShadowColor = self.Gray
		self.Colors      = (     self.Blue,      self.Green,      self.Red,      self.Yellow, self.Purple,      self.Orange,      self.White)
		self.LightColors = (self.LightBlue, self.LightGreen, self.LightRed, self.LightYellow, self.LightPurple, self.LightOrange, self.Gray)
		assert len(self.Colors) == len(self.LightColors) 
		pass

	def setShapes(self):
		self.S_Shape_Template = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

		self.Z_Shape_Template = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

		self.I_Shape_Template = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

		self.O_Shape_Template = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

		self.J_Shape_Template = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

		self.L_Shape_Template = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

		self.T_Shape_Template = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]
		self.Special_Shape_Template = [['.....',
					'.....',
					'..OO.',
					'.....',
					'.....']]  
		self.Special_Shape_Template2 = [['.....',
					'..O..',
					'..O..',
					'.....',
					'.....']] 
		self.Special_Shape_Template3 = [['.....',
					'.....',
					'..O..',
					'.....',
					'.....']] 

		self.PIECES = {'S': self.S_Shape_Template,
          'Z': self.Z_Shape_Template,
          'J': self.J_Shape_Template,
          'L': self.L_Shape_Template,
          'I': self.I_Shape_Template,
          'O': self.O_Shape_Template,
          'T': self.T_Shape_Template,
          'D': self.Special_Shape_Template,
          'E': self.Special_Shape_Template2,
          'F': self.Special_Shape_Template3}
		pass

	def updateScore(self):
		lev=self.getLevel()
		sc=self.getScore()
		self.updateLevel(int(sc/100)+1)
		self.updateFreq(0.27 - (lev*0.012))
    	pass



