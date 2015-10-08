import random, config, sys
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import emotion
from agent import *

class grid(object):
	def __init__(self):
		self.size = config.gridSize
		self.status = ['C', 'D']
		self.coopRate = [None] * config.epochs # Allocate space for performance

		self.grid = [[0 for x in xrange(self.size)] for x in xrange(self.size)]
		self.initGrid()
		self.plotGrid()
		self.updatePlot(self.grid)

	def getAgent(self, (i,j)):
		return self.grid[i][j]

	def initGrid(self):
		# fill grid with agents
		for i in xrange(self.size):
			for j in xrange(self.size):
				#create agents with a random status (action) and give him his location (x,y)
				randI = 0 if random.random() < config.initialCoopRate else 1
				self.grid[i][j] = agent(self.status[randI], (i,j))

	def plotGrid(self):
		#Colors are values
		colorGrid = [[10 if self.grid[i][j].status == 'C' else 0 for j in xrange(self.size)] for i in xrange(self.size)]

		fig = plt.figure(1,(7,7))
		self.cmap = mpl.colors.ListedColormap(['red', 'yellow'])
		bounds=[0,3,6]
		self.norm = mpl.colors.BoundaryNorm(bounds, self.cmap.N)
		img = plt.imshow(colorGrid, interpolation = 'nearest', cmap = self.cmap, norm = self.norm)

		# make a color bar
		plt.colorbar(img,cmap=self.cmap, norm=self.norm, boundaries = bounds,ticks = [-5,0,5])
		plt.draw()
		plt.show()

	def updatePlot(self,grid):
		plt.figure(1)
		colorGrid = [[10 if self.grid[i][j].status == 'C' else 0 for j in xrange(self.size)] for i in xrange(self.size)]
		img = plt.imshow(colorGrid, interpolation = 'nearest', cmap = self.cmap, norm = self.norm)
		plt.draw()
		#plt.savefig('sim.pdf')

	def plotResults(self):
		fig = plt.figure(2,(7,7))
		plt.xlabel('Epoch')
		plt.ylabel('Cooperation rate')

		xspace = np.array(range(config.epochs))
		yspace = np.array(self.coopRate)
		print self.coopRate

		plt.plot(xspace,yspace)
		plt.draw()
		plt.show()

	def updateRateplot(self, rate, x):
		self.coopRate[x] = rate

	def simulate(self):
		# calculate the IPD and update plot for N epochs
		for epoch in xrange(config.epochs):
			print "Epoch: %d" % epoch
			raw_input("Press key to continue")
			cooperators = [[self.getAgent((i,j)).status for j in xrange(self.size)] for i in xrange(self.size)]
			cooperators = [[1 for x in cooperators for y in x if y == 'C']]
			nCooperators = np.sum(cooperators)

			# Step 1: Calculate the scores for each agent
			scoreGrid = [[self.play((i,j)) for j in xrange(self.size)] for i in xrange(self.size)]

			# Step 2: Determine winner for each square
			newGrid = self.grid
			for i in xrange(self.size):
				for j in xrange(self.size):
					newGrid[i][j] = self.mostPoints((i,j))

			# Step 3: Apply emotions
			if config.emotions:
				print "Adding drama"
				for i in xrange(self.size):
					for j in xrange(self.size):
						me = self.getAgent((i,j))
						neighbours = me.getNeighbours()
						neighbours = [self.getAgent(coords) for coords in neighbours]
						me.emotion = emotion.emotionize(me, neighbours)

			# Step 4: Update status based on emotions
			if config.emotions:
				print "Changing actions based on emotions"
				for i in xrange(self.size):
					for j in xrange(self.size):
						me = self.getAgent((i,j))
						if me.emotion == 'Joy':
							me.status = 'C'
						elif me.emotion == 'Distress':
							me.status = 'D'

			# TODO
			# Step 5: Update status based on group
			if config.coalitions:
				print "Coalitions may overrule your action now"

			# Step 6: Update grid, Plot and Log
			self.grid = newGrid
			for i in xrange(self.size):
				for j in xrange(self.size):
					me = self.getAgent((i,j))
					if not me.statusUpdate: pass
					else: me.status = me.statusUpdate
			self.updatePlot(self.grid)
			self.updateRateplot((nCooperators/float(config.nAgents)),epoch)

	def play(self, coords):
		# For each agent, play against all neighbouring opponents
		score = 0
		me = self.getAgent(coords)
		neighbours = me.getNeighbours()
		for coords in neighbours:
			opponent = self.getAgent(coords)
			score += self.pd(me,opponent)

		print "Agent " + str(me.coords) + " played %s and scored %d points" % (me.status, score)
		me.points = score
		return me

	# each site is occupied by the agent scoring the highest
	# total of points among the eight neighbours and the agent itself
	def mostPoints(self, coords):
		me = self.getAgent(coords)
		me.statusUpdate = None
		highest_points = me.points

		neighbours = me.getNeighbours()
		for coords in neighbours:
			opponent = self.getAgent(coords)
			if opponent.points > highest_points:
				# print "%s got occupied to %s" % (me.status, opponent.status)
				me.statusUpdate = opponent.status
				highest_points = opponent.points
		return me

	# Play the prisoner's dilemma
	def pd(self, me, opponent):
		if me.status == 'C':
			if opponent.status == 'C': return config.R
			else: return config.S
		else:
			if opponent.status == 'C': return config.T
			else: return config.P
