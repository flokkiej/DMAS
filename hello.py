#!/usr/bin/python
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import time
import random

pd_payoff = [[(3,3), (5,0)], [(0,5), (1,1)]]


def desirability(me):
	lastscore = me.lastRound
	emotion = me.returnEmotion()
	D = lastscore - 2
	return D

def praiseworthyness(me, other):
	me_emo = me.returnEmotion()
	other_emo = other.returnEmotion()
	return





class agent(object):
	"""docstring for agent"""
	def __init__(self, color, (x,y)):
		super(agent, self).__init__()
		#self.char = char
		self.color = color
		self.coords = (x,y)
		# Joy, Anger
		self.emotions = ['Joy', 'Anger']
		self.thresholds = [1,1]
		self.lastRound = 0
		self.points = 0
		#self.neighbours = self.returnNeighbours2(self.size)
		self.lastAction = 0
		self.action = random.randint(0,1)

	def out(self):
		sys.stdout.write((str) (self.color))
		sys.stdout.write(' ')
	'''
	def returnNeighbours(self):
		(x,y) = self.coords
		neighbours = lambda x, y :[(x2, y2) for x2 in range(x-1, x+2)
			for y2 in range(y-1, y+2)
			if (-1 < x <= grid.returnSize and
				-1 < y <= grid.returnSize and
				(x != x2 or y != y2) and
				(0 <= x2 <= grid.returnSize) and
				(0 <= y2 <= grid.returnSize))]
		return neighbours(x,y)
	'''
	def returnNeighbours2(self,size):
		size = size-1
		(x,y) = self.coords
		if (x == 0 and y<size):
			return [(0,y+1),(1,y+1),(1,y)]
		if (x == size and y==size):
			return []
		if (x == size and y<size):
			return [(x, y+1)]
		if (y == size and x<size):
			return [(x+1,y-1),(x+1,y)]
		return [(x,y+1),(x+1,y+1),(x+1,y),(x+1,y-1)]

	def getColor(self, (x,y)):
		return self.color
	def returnEmotion(self):
		return self.emotions
	def returnLastPDround(self):
		return self.lastRound
	def returnPoints(self):
		return self.points

class grid(object):
	"""docstring for grid"""
	def __init__(self, gridSize):
		super(grid, self).__init__()
		self.size = gridSize
		self.initGrid()
		#self.emotions = ['x', 'o', '+', '-']
		self.color = [-10, 10]
		self.cGrid = []
	def returnSize(self):
		return self.size
	def getAgent(self, (i,j)):
		return self.grid[i][j]
	def initGrid(self):
		self.grid = [[0 for x in xrange(self.size)] for x in xrange(self.size)]
	def fillGrid(self):
		for i in xrange(self.size):
			for j in xrange(self.size):
				randI = random.randint(0, len(self.color)-1)
				self.grid[i][j] = agent(self.color[randI], (i,j))
				#self.grid[i][j] = agent(self.emotions[randI], self.color[randI], (i,j))
	def printGrid(self):
		for i in xrange(self.size):
			for j in xrange(self.size):
				self.grid[i][j].out()
			print "\n"
	def plotGrid(self):
		#Colors are values
		colorGrid = [[0 for x in xrange(self.size)] for x in xrange(self.size)]
		for i in xrange(self.size):
			for j in xrange(self.size):
				colorGrid[i][j] = self.grid[i][j].color
		
		self.cGrid = colorGrid

		fig = plt.figure(1,(7,7))
		self.cmap = mpl.colors.ListedColormap(['blue','black','red', 'yellow'])
		self.bounds=[-6,-3,0,3,6]
		self.norm = mpl.colors.BoundaryNorm(self.bounds, self.cmap.N)
		img = plt.imshow(self.cGrid, interpolation = 'nearest', cmap = self.cmap, norm = self.norm)

		# make a color bar
		plt.colorbar(img,cmap=self.cmap, norm=self.norm, boundaries = self.bounds,ticks = [-5,0,5])
		plt.draw()
		plt.show()
		return

	def updatePlot(self,grid):
		colorGrid = [[0 for x in xrange(self.size)] for x in xrange(self.size)]
		for i in xrange(self.size):
			for j in xrange(self.size):
				colorGrid[i][j] = self.grid[i][j].color
		
		#cGrid = colorGrid
		img = plt.imshow(colorGrid, interpolation = 'nearest', cmap = self.cmap, norm = self.norm)
		plt.draw()
		return

	def simulate(self, N):
		for i in xrange(N):
			#print random colors 
			#randGrid = [[random.random()*(20)-10 for x in xrange(self.size)] for x in xrange(self.size)]
			time.sleep(.5)
			newGrid = self.grid
			#print(self.size)
			for i in xrange(self.size):
				for j in xrange(self.size):
					newGrid[i][j] = self.play((i,j))
			self.grid = newGrid
			self.updatePlot(newGrid)
			#print self.grid[13][14].returnNeighbours2(15)
			#print "score: " + str(self.grid[14][14].score) + " action: " + str(self.grid[14][14].action)

	def play(self, (x,y)):
		me = self.getAgent((x,y))
		neighbours = me.returnNeighbours2(self.size)
		#print neighbours
		#self.printGrid()
		#nPlays = len(neighbours)-1
		sum = 0
		for (x, y) in neighbours:
			#print x, y
			opponent = self.getAgent((x,y))
			self.pd(me,opponent)
		return me

	def pd(self,me,opponent):
		act1 = me.action
		act2 = opponent.action
		(me_score, opp_score) = pd_payoff[act1][act2]

		#Implement PD based on Emotions here (probably)
		me.points = me.points +me_score
		opponent.score = opponent.points + opp_score
		swp = me.action
		me.action = opponent.action
		me.color = me.points
		opponent.action = me.action
		opponent.color = opponent.points


		return (me_score, opp_score)

	def getDesirability(self,me):
		return desirability(me)

	def getPraiseworthyness(self, me, other):
		return praiseworthyness(me,other)


def main():
	gridSize = int(sys.argv[1]) if len(sys.argv)>1 else 15
	#print "Grid size: %d\n" % gridSize
	g = grid(gridSize)
	g.fillGrid()
	plt.ion()
	g.plotGrid()
	g.simulate(50)
	plt.ioff()
	#g.play((14,1))
	#a = agent(10, (15,15))
	#print a.returnNeighbours2(15)
	return

if __name__ == "__main__":
	main()
