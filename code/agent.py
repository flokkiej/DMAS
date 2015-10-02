import random

class agent(object):
	"""docstring for agent"""
	def __init__(self, color, (x,y)):
		super(agent, self).__init__()
		self.color = color
		self.coords = (x,y)
		# Joy, Anger
		self.emotions = ['Joy', 'Anger']
		self.thresholds = [1,1]
		self.lastRound = 0
		self.points = 0
		self.lastAction = 0
		self.neighbours = []
		self.action = random.randint(0,1)

	def out(self):
		sys.stdout.write((str) (self.color))
		sys.stdout.write(' ')

	def returnNeighbours(self,size):
		# Returns only neighbours towards NE,E,SE and S
		# For sake of the algorithm
		if self.neighbours == []:
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
		else:
			return self.neighbours

	def getColor(self, (x,y)):
		return self.color
	def returnEmotion(self):
		return self.emotions
	def returnLastPDround(self):
		return self.lastRound
	def returnPoints(self):
		return self.points