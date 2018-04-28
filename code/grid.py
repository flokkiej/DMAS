import random
import csv
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import emotion
from agent import *


class grid(object):
	"""docstring for grid"""
	def __init__(self, gridSize):
		super(grid, self).__init__()
		self.size = gridSize
		self.initGrid()
		#self.emotions = ['x', 'o', '+', '-']
		self.color = [0, 10]
		self.cGrid = []
		self.cooprate = 0
		self.pltcooprate = []
		self.pltx = []
		self.Nactions = 0

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

	def updatePlot(self,grid):
		plt.figure(1)
		colorGrid = [[0 for x in xrange(self.size)] for x in xrange(self.size)]
		for i in xrange(self.size):
			for j in xrange(self.size):
				colorGrid[i][j] = self.grid[i][j].color

		img = plt.imshow(colorGrid, interpolation = 'nearest', cmap = self.cmap, norm = self.norm)
		plt.draw()
		#plt.savefig('sim.pdf')

	def plotRate(self):
		fig = plt.figure(2,(7,7))
		#plt.plot()
		plt.xlabel('Epoch')
		plt.ylabel('Mutual cooperation rate')
		plt.draw()
		plt.show()

	def updateRateplot(self,rate, x):
		plt.figure(2)
#		print self.pltx
#		print self.pltcooprate
		self.pltx.append(x)
		self.pltcooprate.append(rate)
		xspace = np.array(self.pltx)
		yspace = np.array(self.pltcooprate)
		plt.plot(xspace,yspace)
		plt.draw()


	def simulate(self, N):
		# calculate the IPD and update plot for N epochs
		for n in xrange(N):
			self.cooprate = 0
			self.Nactions = 0
			#time.sleep(.5)
			newGrid = self.grid
			for i in xrange(self.size):
				for j in xrange(self.size):
					newGrid[i][j] = self.play((i,j))
			self.grid = newGrid
			self.updatePlot(newGrid)
			self.updateRateplot((self.cooprate/float(self.Nactions)),n)


	def play(self, (x,y)):
		# For each agent play against all (relevant) neighbouring opponents
		me = self.getAgent((x,y))
		neighbours = me.returnNeighbours(self.size)
		for (x, y) in neighbours:
			opponent = self.getAgent((x,y))
			self.pd(me,opponent)
		#give agent predominent color
		length = len(me.hist)
		c = sum(me.hist)
		# sum is amount of defectors.
		if c < (length/2):
			me.color = 10
		else:
			me.color = 0
		me.hist = []
		return me

	def pd(self,me,opponent):
		#Implement PD based on Emotions here (probably)

		act1 = me.action
		act2 = opponent.action
		(me_score, opp_score) = pd_payoff[act1][act2]


		me.points = me_score
		opponent.points = opp_score
		me.hist.append(me.action)
		opponent.hist.append(opponent.action)
		swp = me.action
		me.action = opponent.action
		#me.color = me.points
		opponent.action = swp
		#opponent.color = opponent.points

		if me.action == 0 and opponent.action == 0:
			self.cooprate = self.cooprate +1
		self.Nactions = self.Nactions +1
		return (me_score, opp_score)

	def getDesirability(self,me):
		return emotion.desirability(me)

	def getPraiseworthyness(self, me, other):
		return emotion.praiseworthyness(me,other)
