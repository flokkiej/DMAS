#!/usr/bin/python
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from random import randint

class agent(object):
	"""docstring for agent"""
	def __init__(self, char, color, (x,y)):
		super(agent, self).__init__()
		self.char = char
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
		self.emotions = ['x', 'o', '+', '-']
		self.color = [-10, -1, 1, 10]
	def returnSize(self):
		return self.size
	def initGrid(self):
		self.grid = [[0 for x in xrange(self.size)] for x in xrange(self.size)]
	def fillGrid(self):
		for i in xrange(self.size):
			for j in xrange(self.size):
				randI = randint(0, len(self.emotions)-1)
				self.grid[i][j] = agent(self.emotions[randI], self.color[randI], (i,j))
	def printGrid(self):
		for i in xrange(self.size):
			for j in xrange(self.size):
				self.grid[i][j].out()
			print "\n"
	def plotGrid(self):
		colorGrid = [[0 for x in xrange(self.size)] for x in xrange(self.size)]
		for i in xrange(self.size):
			for j in xrange(self.size):
				colorGrid[i][j] = self.grid[i][j].color
		#print colorGrid

		fig = plt.figure(1,(5,5))
		cmap = mpl.colors.ListedColormap(['blue','black','red', 'yellow'])
		bounds=[-6,-3,0,3,6]
		norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
		img = plt.imshow(colorGrid, interpolation = 'nearest', cmap = cmap, norm = norm)

		# make a color bar
		plt.colorbar(img,cmap=cmap, norm=norm, boundaries = bounds,ticks = [-5,0,5])

		plt.show()
		return

def main():
	gridSize = int(sys.argv[1]) if len(sys.argv)>1 else 15
	print "Grid size: %d\n" % gridSize
	g = grid(gridSize)
	g.fillGrid()
	g.plotGrid()

	#testa = agent('x', 'r',(1,1))
	#print testa.returnNeighbours()
	return

if __name__ == "__main__":
	main()
