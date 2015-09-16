#!/usr/bin/python
import sys
from random import randint

class agent(object):
	"""docstring for agent"""
	def __init__(self, char):
		super(agent, self).__init__()
		self.char = char
	def out(self):
		sys.stdout.write(self.char)
		sys.stdout.write(' ')


class grid(object):
	"""docstring for grid"""
	def __init__(self, gridSize):
		super(grid, self).__init__()
		self.size = gridSize
		self.initGrid()
		self.emotions = ['x', 'o', '+', '-']
	def returnSize(self):
		return self.size
	def initGrid(self):
		self.grid = [[0 for x in xrange(self.size)] for x in xrange(self.size)]
	def fillGrid(self):
		for i in xrange(self.size):
			for j in xrange(self.size):
				emotion = randint(0, len(self.emotions)-1)
				self.grid[i][j] = agent(self.emotions[emotion])
	def printGrid(self):
		for i in xrange(self.size):
			for j in xrange(self.size):
				self.grid[i][j].out()
			print "\n"

def main():

	gridSize = int(raw_input("Grid size? --> "))
	g = grid(gridSize)
	g.fillGrid()
	g.printGrid()
#	printGrid(grid, gridSize)
	return

def printGrid(grid, gridSize):

	return


if __name__ == "__main__":
	main()
