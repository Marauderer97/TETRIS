import random, time, pygame, sys
import numpy
from pygame.locals import *

class Piece():
	def __init__(self):
		 		self.movingLeft=False
		 		self.movingRight=False
		 		self.movingDown=False
		 		self.fallingPiece=None
		 		pass
	def  getNewPiece(self):
				self.shape = random.choice(list(self.PIECES.keys()))
				if(self.shape == 'D' or self.shape == 'E' or self.shape == 'F'):# spcl color to denote pieces which help clear the board
					tempColor = len(self.Colors)-1
				else:
					tempColor = random.randint(0, len(self.Colors)-2)
				newPiece= {'shape': self.shape,
	       				'rotation': random.randint(0, len(self.PIECES[self.shape]) - 1),
	               		'x': int(self.BoardW / 2) - int(self.TemplateW / 2),
	                	'y': -2, # start it above the board (i.e. less than 0)
	                	'color': tempColor}
				return newPiece		                 

	def moveleft(self):
		 		self.fallingPiece['x'] -=1
		 		self.movingLeft = True
		 		self.movingRight = False
		 		self.lastMoveSidewaysTime = time.time()
		 		pass

	def moveright(self):
		 		self.fallingPiece['x'] +=1
		 		self.movingRight=True
		 		self.movingLeft = False
		 		self.lastMoveSidewaysTime= time.time()
		 		pass

	def rotate(self):
		 		self.fallingPiece['rotation']=(self.fallingPiece['rotation']+1)% len(self.PIECES[self.fallingPiece['shape']])
		 		if not self.isValidPosition(self.board, self.fallingPiece):
					self.fallingPiece['rotation']=(self.fallingPiece['rotation']-1)% len(self.PIECES[self.fallingPiece['shape']])
	def antirotate(self):
				self.fallingPiece['rotation']=(self.fallingPiece['rotation']-1)% len(self.PIECES[self.fallingPiece['shape']])
				if not self.isValidPosition(self.board, self.fallingPiece):
					self.fallingPiece['rotation']=(self.fallingPiece['rotation']+1)% len(self.PIECES[self.fallingPiece['shape']])

	def space(self):
		 		self.movingDown= False
		 		self.movingLeft = False
		 		self.movingRight = False
		 		for i in range(1, self.BoardH):
					if not self.isValidPosition(self.board, self.fallingPiece, adjY=i):
						break
		 		self.fallingPiece['y']+=i-1
		 		pass
	def down(self):
		 	self.movingDown= True
		 	if self.isValidPosition(self.board, self.fallingPiece, adjY=1):
				self.fallingPiece['y'] += 1
			else:
				self.fallingPiece['y'] += 0
		 	self.lastMoveDownTime= time.time()
		 	pass

	def drawNextPiece(self,piece,PIECES):
	    # draw the "next" text
	    nextSurf = self.SmallFont.render('Next:', True, self.TextColor)
	    nextRect = nextSurf.get_rect()
	    nextRect.topleft = (self.WindowW - 120, 80)
	    self.Display.blit(nextSurf, nextRect)
	    # draw the "next" piece
	    self.drawPiece(piece, pixelx=self.WindowW-120, pixely=100,PIECES={})

	def drawPiece(self,piece, pixelx=None, pixely=None,PIECES={}):
	    shapeToDraw = self.PIECES[piece['shape']][piece['rotation']]
	    #print piece['shape'], piece['rotation']
	    #print shapeToDraw
	    if pixelx == None and pixely == None:
	        # if pixelx & pixely hasn't been specified, use the location stoRed in the piece data structure
	        pixelx, pixely = self.convertToPixelCoords(piece['x'], piece['y'])

	    # draw each of the boxes that make up the piece
	    for x in range(self.TemplateW):
	        for y in range(self.TemplateH):
	            if shapeToDraw[y][x] != self.BLANK:
	                self.drawBox(None, None, piece['color'], pixelx + (x * self.BoxSize), pixely + (y * self.BoxSize))

	def drawBox(self,boxx, boxy, color, pixelx=None, pixely=None):
		if color == self.BLANK:
		    return
		if pixelx == None and pixely == None:
		    pixelx, pixely = self.convertToPixelCoords(boxx, boxy)

		pygame.draw.rect(self.Display, self.Colors[color], (pixelx + 1, pixely + 1, self.BoxSize - 1, self.BoxSize - 1))
		pygame.draw.rect(self.Display, self.LightColors[color], (pixelx + 1, pixely + 1, self.BoxSize - 4, self.BoxSize - 4))
		pass

		
