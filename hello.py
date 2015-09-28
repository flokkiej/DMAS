#!/usr/bin/python
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import time
import random

pd_payoff = [[7,0], [10,0]]

class agent(object):
	"""docstring for agent"""
	def __init__(self, color, (x,y)):
		super(agent, self).__init__()
		#self.char = char
		self.color = color
		self.coords = (x,y)
	def out(self):
		sys.stdout.write(self.char)
		sys.stdout.write(' ')
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


class grid(object):
	"""docstring for grid"""
	def __init__(self, gridSize):
		super(grid, self).__init__()
		self.size = gridSize
		self.initGrid()
		#self.emotions = ['x', 'o', '+', '-']
		self.color = [-10, -1, 1, 10]
		self.cGrid = []
	def returnSize(self):
		return self.size
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

		fig = plt.figure(1,(5,5))
		self.cmap = mpl.colors.ListedColormap(['blue','black','red', 'yellow'])
		self.bounds=[-6,-3,0,3,6]
		self.norm = mpl.colors.BoundaryNorm(self.bounds, self.cmap.N)
		img = plt.imshow(self.cGrid, interpolation = 'nearest', cmap = self.cmap, norm = self.norm)

		# make a color bar
		plt.colorbar(img,cmap=self.cmap, norm=self.norm, boundaries = self.bounds,ticks = [-5,0,5])
		plt.draw()
		plt.show()
		return

	def updatePlot(self,randGrid):
		img = plt.imshow(randGrid, interpolation = 'nearest', cmap = self.cmap, norm = self.norm)
		plt.draw()
		return

	def simulate(self, N):
		for i in xrange(N):
			#print random colors 
			randGrid = [[random.random()*(20)-10 for x in xrange(self.size)] for x in xrange(self.size)]
			time.sleep(.5)
			self.updatePlot(randGrid)



def main():
	gridSize = int(sys.argv[1]) if len(sys.argv)>1 else 15
	#print "Grid size: %d\n" % gridSize
	g = grid(gridSize)
	g.fillGrid()
	plt.ion()
	g.plotGrid()
	g.simulate(50)
	return

if __name__ == "__main__":
	main()
