import random, itertools, config

class agent(object):
	def __init__(self, initialStatus, (x,y)):
		self.coords = (x,y)
		self.status = initialStatus
		self.statusUpdate = None
		self.neighbours = self.meetNeighbours()
		self.points = 0
		self.emotion = None
		self.coalition = None

	def meetNeighbours(self):
		# Returns all neighbouring agents
		neighbours = []
		(x,y) = self.coords

		# Define the xrange and yrange for coord
		a = [x-1, x, x+1]
		b = [y-1, y, y+1]

		# Clean up outside borders
		a2 = [ x for x in a if x >= 0 and x < config.gridSize ]
		b2 = [ y for y in b if y >= 0 and y < config.gridSize ]

		# Get all permutations
		neighbours = list(itertools.product(a2,b2))

		# You're not your own neighbour, silly!
		neighbours.remove(self.coords)
		return neighbours

	def getNeighbours(self):
		return self.neighbours

	def getStatus(self):
		return self.status

	def getEmotion(self):
		return self.emotion

	def getPoints(self):
		return self.points

	def getGroup(self):
		return self.group
