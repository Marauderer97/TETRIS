from random import randint
import numpy
from pygame.locals import *
import pygame,sys,time

class Board():
	def __init__(self):
		self.board=[]

	def BlankBoard(self):
		self.board=[]
		for i in range(self.BoardW):
        		self.board.append([self.BLANK] * self.BoardH)
        		self.boardInitiate()
		return self.board

	def boardInitiate(self):
		self.lastDownTime=time.time()
		self.lastSideWaysTime=time.time()
		self.lastFallTime = time.time()
		self.movingDown = False 
		self.movingLeft = False
		self.movingRight = False
		self.__score = 0
		self.__level=1
		self.__fallFreq=0.27
		pass
	#methods to access and update private variables
	def getScore(self):
			return self.__score
	def updateScore(self, inc):
    		self.__score+=inc

	def getLevel(self):
    		return self.__level
	def updateLevel(self,val):
    		self.__level=val

	def getFreq(self):
    		return self.__fallFreq
	def updateFreq(self,val):
    		self.__fallFreq= val

	def isOnBoard(self,x, y):
    		return (x >= 0 and x < self.BoardW and y < self.BoardH)



	def isCompleteLine(self, y):
    		# Return True if the line filled with boxes with no gaps.
    		for x in range(self.BoardW):
        		if self.board[x][y] == self.BLANK:
            			return False
    		return True

	def addToBoard(self,board, piece,PIECES):
	    # fill in the board based on piece's location, shape, and rotation
	    for x in range(self.TemplateW):
			for y in range(self.TemplateH):
				if PIECES[piece['shape']][piece['rotation']][y][x] != self.BLANK:
					board[x + piece['x']][y + piece['y']] = piece['color']
					if piece['shape'] == 'D' or piece['shape'] == 'F':
						self.lastY = y+ piece['y']
					if piece['shape'] == 'E' or piece['shape'] == 'F':
						self.lastX = x+ piece['x']
	
	def removeSpecialLines(self):
		numLinesRemoved = 0
		y = self.lastY # start y at the bottom of the board
		if y>0:
			for pullDownY in range(y, 0, -1):
				for x in range(self.BoardW):
					self.board[x][pullDownY] = self.board[x][pullDownY-1]
			for x in range(self.BoardW):
				self.board[x][0] = self.BLANK
			numLinesRemoved += 1
		return numLinesRemoved 

	def removeVerticalLine(self):
		x=self.lastX
		if x>0:
			for y in range(self.BoardH):
				self.board[x][y] = self.BLANK


	def removeCompleteLines(self):
    		# Remove any completed lines on the board, move everything above them down, and return the number of complete lines.
    		numLinesRemoved = 0
    		y = self.BoardH - 1 # start y at the bottom of the board
    		while y >= 0:
        		if self.isCompleteLine(y):
            			# Remove the line and pull boxes down by one line.
            			for pullDownY in range(y, 0, -1):
                			for x in range(self.BoardW):
                    				self.board[x][pullDownY] = self.board[x][pullDownY-1]
            			# Set very top line to blank.
            			for x in range(self.BoardW):
                			self.board[x][0] = self.BLANK
            			numLinesRemoved += 1
        		else:
            			y -= 1 # move on to check next row up
    		return numLinesRemoved 

	def isValidPosition(self,board, piece, adjX=0, adjY=0):
	    # Return True if the piece is within the board and not colliding
	    	for x in range(self.TemplateW):
	        		for y in range(self.TemplateH):
						isAboveBoard = y + piece['y'] + adjY < 0
						if isAboveBoard or self.PIECES[piece['shape']][piece['rotation']][y][x] == self.BLANK:
							continue
						if not self.isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
							return False
						if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != self.BLANK:
							return False
	    	return True

	def drawBoard(self,board):
		# draw the border around the board
		pygame.draw.rect(self.Display, self.BorderColor, (self.Xbound - 3, self.Topbound - 7, (self.BoardW * self.BoxSize) + 8, (self.BoardH * self.BoxSize) + 8), 5)
	    # fill the background of the board
		pygame.draw.rect(self.Display, self.BgColor, (self.Xbound, self.Topbound, self.BoxSize * self.BoardW, self.BoxSize * self.BoardH))
	    # draw the individual boxes on the board
		for x in range(self.BoardW):
			for y in range(self.BoardH):
				self.drawBox(x, y, board[x][y])

	def drawStatus(self):
	    # draw the score text
		scoreSurf = self.SmallFont.render('Score: %s' % self.__score, True, self.TextColor)
		scoreRect = scoreSurf.get_rect()
		scoreRect.topleft = (self.WindowW - 150, 20)
		self.Display.blit(scoreSurf, scoreRect)
		levelSurf = self.SmallFont.render('Level: %s' % self.__level, True, self.TextColor)
		levelRect = levelSurf.get_rect()
		levelRect.topleft = (self.WindowW - 150, 40)
		self.Display.blit(levelSurf, levelRect)

	def drawIns(self):
		#displays all instructions
		ins1="left: a or <-"
		ins2="right: d or ->"
		ins3="rotate clock: s"
		ins4="rotate anticlock: q"
		ins5="drop : <space>"
		ins6="POINTS SCHEME"
		ins7="+10 for block"
		ins8="+100 for clearing"
		insSurf = self.SmallFont.render(ins1, True, self.TextColor)
		insRect = insSurf.get_rect()
		insRect.topleft = (self.WindowW - 800, 20)
		self.Display.blit(insSurf, insRect)
		insSurf = self.SmallFont.render(ins2, True, self.TextColor)
		insRect = insSurf.get_rect()
		insRect.topleft = (self.WindowW - 800, 40)
		self.Display.blit(insSurf, insRect)
		insSurf = self.SmallFont.render(ins3, True, self.TextColor)
		insRect = insSurf.get_rect()
		insRect.topleft = (self.WindowW - 800, 60)
		self.Display.blit(insSurf, insRect)
		insSurf = self.SmallFont.render(ins4, True, self.TextColor)
		insRect = insSurf.get_rect()
		insRect.topleft = (self.WindowW - 800, 80)
		self.Display.blit(insSurf, insRect)
		insSurf = self.SmallFont.render(ins5, True, self.TextColor)
		insRect = insSurf.get_rect()
		insRect.topleft = (self.WindowW - 800, 100)
		self.Display.blit(insSurf, insRect)
		insSurf = self.SmallFont.render(ins6, True, self.TextColor)
		insRect = insSurf.get_rect()
		insRect.topleft = (self.WindowW - 800, 140)
		self.Display.blit(insSurf, insRect)
		insSurf = self.SmallFont.render(ins7, True, self.TextColor)
		insRect = insSurf.get_rect()
		insRect.topleft = (self.WindowW - 800, 160)
		self.Display.blit(insSurf, insRect)
		insSurf = self.SmallFont.render(ins8, True, self.TextColor)
		insRect = insSurf.get_rect()
		insRect.topleft = (self.WindowW - 800, 180)
		self.Display.blit(insSurf, insRect)

	