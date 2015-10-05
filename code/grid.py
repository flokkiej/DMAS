import random
import matplotlib.pyplot as plt
import matplotlib as mpl
import time
from agent import *

pd_payoff = [[(3,3), (5,0)], [(0,5), (1,1)]]


class grid(object):
	"""docstring for grid"""
	def __init__(self, gridSize):
		super(grid, self).__init__()
		self.size = gridSize
		self.initGrid()
		#self.emotions = ['x', 'o', '+', '-']
		self.color = [0, 10]
		self.cGrid = []
	def returnSize(self):
		return self.size
	def getAgent(self, (i,j)):
		return self.grid[i][j]
	def initGrid(self):
		self.grid = [[0 for x in xrange(self.size)] for x in xrange(self.size)]
	def fillGrid(self):
		# fills grid with agents
		for i in xrange(self.size):
			for j in xrange(self.size):
				#create agents with a random color(emo) and give him his location (x,y)				
				randI = random.randint(0, len(self.color)-1)
				self.grid[i][j] = agent(self.color[randI], (i,j))
	def printGrid(self):
		# redundant.
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
		
		cGrid = colorGrid

		fig = plt.figure(1,(7,7))
		self.cmap = mpl.colors.ListedColormap(['red', 'yellow'])
		bounds=[0,3,6]
		self.norm = mpl.colors.BoundaryNorm(bounds, self.cmap.N)
		img = plt.imshow(cGrid, interpolation = 'nearest', cmap = self.cmap, norm = self.norm)

		# make a color bar
		plt.colorbar(img,cmap=self.cmap, norm=self.norm, boundaries = bounds,ticks = [-5,0,5])
		plt.draw()
		plt.show()
		return

	def updatePlot(self,grid):
		colorGrid = [[0 for x in xrange(self.size)] for x in xrange(self.size)]
		for i in xrange(self.size):
			for j in xrange(self.size):
				colorGrid[i][j] = self.grid[i][j].color
		
		img = plt.imshow(colorGrid, interpolation = 'nearest', cmap = self.cmap, norm = self.norm)
		plt.draw()
		#plt.savefig('sim.pdf')
		return

	def simulate(self, N):
		# calculate the IPD and update plot for N epochs
		for i in xrange(N):
			time.sleep(.5)
			newGrid = self.grid
			for i in xrange(self.size):
				for j in xrange(self.size):
					newGrid[i][j] = self.play((i,j))
			self.grid = newGrid
			self.updatePlot(newGrid)
		return

	def play(self, (x,y)):
		# For each agent play against all (relevant) neighbouring opponents
		me = self.getAgent((x,y))
		neighbours = me.returnNeighbours(self.size)
		sum = 0
		for (x, y) in neighbours:
			opponent = self.getAgent((x,y))
			self.pd(me,opponent)
		return me

	def pd(self,me,opponent):
		#Implement PD based on Emotions here (probably)

		act1 = me.action
		act2 = opponent.action
		(me_score, opp_score) = pd_payoff[act1][act2]

		
		me.points = me_score
		opponent.score = opp_score
		swp = me.action
		me.action = opponent.action
		me.color = me.points
		opponent.action = swp
		opponent.color = opponent.points


		return (me_score, opp_score)

	def getDesirability(self,me):
		return emotion.desirability(me)

	def getPraiseworthyness(self, me, other):
		return emotion.praiseworthyness(me,other)