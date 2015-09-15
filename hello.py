import sys

class Agent(object):
	"""docstring for Agent"""
	def __init__(self, char):
		super(Agent, self).__init__()
		self.char = char
	def out(self):
		sys.stdout.write(self.char)
		sys.stdout.write(' ')
		

def main():

	gridSize = 5

	grid = [[0 for x in xrange(gridSize)] for x in xrange(gridSize)] 

	for i in xrange(gridSize):
		for j in xrange(gridSize):
			grid[i][j] = Agent('a')

	printGrid(grid, gridSize)
	return 

def printGrid(grid, gridSize):

	for i in xrange(gridSize):
		for j in xrange(gridSize):
			grid[i][j].out()
		print "\n"
	return


if __name__ == "__main__":
	main()

