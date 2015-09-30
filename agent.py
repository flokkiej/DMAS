
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