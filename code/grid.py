import random
import csv
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import emotion
from agent import *


class grid(object):
    def __init__(self):
        self.size = config.gridSize
        self.status = ['C', 'D']
        self.coopRate = [None] * config.epochs  # Allocate space for performance
        self.emotions = {}

        self.grid = [[0 for x in xrange(self.size)] for x in xrange(self.size)]
        self.initGrid()
        if config.plot:
            self.plotGrid()
            self.updatePlot(self.grid)

    def getAgent(self, (i, j)):
        return self.grid[i][j]

    def setAgent(self, (i, j), agent):
        self.grid[i][j] = agent

    def initGrid(self):
        # fill grid with agents
        for i in xrange(self.size):
            for j in xrange(self.size):
                # create agents with a random status (action) and give him his location (x,y)
                randI = 0 if random.random() < config.initialCoopRate else 1
                self.grid[i][j] = agent(self.status[randI], (i, j))

    def plotGrid(self):
        # Colors are values
        colorGrid = [[10 if self.grid[i][j].status == 'C' else 0 for j in xrange(self.size)] for i in xrange(self.size)]

        fig = plt.figure(1, (7, 7))
        self.cmap = mpl.colors.ListedColormap(['red', 'yellow'])
        bounds = [0, 3, 6]
        self.norm = mpl.colors.BoundaryNorm(bounds, self.cmap.N)
        img = plt.imshow(colorGrid, interpolation='nearest', cmap=self.cmap, norm=self.norm)

        # make a color bar
        # plt.colorbar(img, cmap=self.cmap, norm=self.norm, boundaries=bounds, ticks=[-5, 0, 5])
        plt.draw()

    # plt.show()

    def updatePlot(self, grid):
        plt.figure(1)
        colorGrid = [[10 if self.grid[i][j].status == 'C' else 0 for j in xrange(self.size)] for i in xrange(self.size)]
        img = plt.imshow(colorGrid, interpolation='nearest', cmap=self.cmap, norm=self.norm)
        plt.draw()

    # plt.savefig('sim_emotion.pdf')

    def printGrid(self):
        for i in xrange(self.size):
            for j in xrange(self.size):
                me = self.getAgent((i, j))
                print "%s (%00.1f)\t" % (me.status, me.points),
            print ""

    def plotResults(self):
        if not config.plot:
            self.plotGrid()
        fig = plt.figure(2, (7, 7))
        plt.xlabel('Epoch')
        plt.ylabel('Cooperation rate')

        xspace = np.array(range(config.epochs))
        yspace = np.array(self.coopRate)

        print "Mean coop " + str(np.mean(yspace))

        with open("output.csv", "wb") as f:
            writer = csv.writer(f)
            for val in self.coopRate:
                writer.writerow([val])

        plt.plot(xspace, yspace)
        plt.draw()
        plt.savefig('results_emotion.pdf')
        plt.show()

    def simulate(self):
        # calculate the IPD and update plot for N epochs
        for epoch in xrange(config.epochs):
            print "\nEpoch: %d" % epoch
            self.emotions = {'Joy': 0, 'Distress': 0, 'Anger': 0, 'Pity': 0, 'Threat': 0, 'Boredom': 0, None: 0}

            # Calc number of cooperators
            cooperators = [[self.getAgent((i, j)).status for j in xrange(self.size)] for i in xrange(self.size)]
            cooperators = [[1 for x in cooperators for y in x if y == 'C']]
            nCooperators = np.sum(cooperators)

            # print np.sum([[self.getAgent((i, j)).emotionless for j in xrange(self.size)] for i in xrange(self.size)])

            # Step 1: Calculate the scores for each agent
            for i in xrange(self.size):
                for j in xrange(self.size):
                    self.play((i, j))

            # Step 2: Determine winner for each square
            newGrid = self.grid
            for i in xrange(self.size):
                for j in xrange(self.size):
                    newGrid[i][j] = self.mostPoints((i, j))

            # Step 3: Apply emotions
            if config.emotions:
                for i in xrange(self.size):
                    for j in xrange(self.size):
                        me = self.getAgent((i, j))
                        if me.emotionless:
                            continue
                        else:
                            neighbours = me.neighbours
                            neighbours = [self.getAgent(coords) for coords in neighbours]
                            me.emotionUpdate = emotion.emotionize(me, neighbours)
                            self.emotions[me.emotion] += 1
                            self.setAgent((i, j), me)
                print "Emotions this round: " + str(self.emotions)

            # Step 4: Update status based on emotions
            if config.emotions:
                for i in xrange(self.size):
                    for j in xrange(self.size):
                        me = self.getAgent((i, j))
                        if me.emotionless:
                            continue
                        else:
                            if me.emotionUpdate == 'Joy':
                                me.statusUpdate = 'C'
                            elif me.emotionUpdate == 'Distress':
                                me.statusUpdate = 'D'
                            elif me.emotionUpdate == 'Pity':
                                me.statusUpdate = 'C'
                            elif me.emotionUpdate == 'Anger':
                                me.statusUpdate = 'D'
                            elif me.emotionUpdate == 'Threat':
                                me.coalition = True
                            elif me.emotionUpdate == 'Boredom':
                                me.coalition = False
                            self.setAgent((i, j), me)

            # Step 5: Update status based on group
            if config.coalitions:
                coalition_size = 0
                n_c_vote = 0
                n_d_vote = 0
                for i in xrange(self.size):
                    for j in xrange(self.size):
                        me = self.getAgent((i, j))
                        if me.coalition:
                            coalition_size += 1
                            if me.statusUpdate == 'C':
                                n_c_vote += 1
                            else:
                                n_d_vote += 1

                print "%d C Vote and %d D Vote" % (n_c_vote, n_d_vote)

                if n_c_vote > n_d_vote:
                    for i in xrange(self.size):
                        for j in xrange(self.size):
                            me = self.getAgent((i, j))
                            if me.coalition:
                                me.statusUpdate = 'C'
                                self.setAgent((i, j), me)
                else:
                    for i in xrange(self.size):
                        for j in xrange(self.size):
                            me = self.getAgent((i, j))
                            if me.coalition:
                                me.statusUpdate = 'D'
                                self.setAgent((i, j), me)
                print "Coalition size: %d" % coalition_size

            # Step 6: Update grid, Plot and Log
            self.grid = newGrid
            for i in xrange(self.size):
                for j in xrange(self.size):
                    me = self.getAgent((i, j))
                    if me.statusUpdate is not None:
                        me.status = me.statusUpdate
                    if config.emotions and not me.emotionless:
                        me.emotion = me.emotionUpdate
                        me.emotionUpdate = None
                    self.setAgent((i, j), me)
            if config.plot:
                self.updatePlot(self.grid)
            self.coopRate[epoch] = nCooperators / float(config.nAgents)
            print "Coop rate: " + str(self.coopRate[epoch])

    def play(self, coords):
        # For each agent, play against all neighbouring opponents
        score = 0
        me = self.getAgent(coords)
        neighbours = me.neighbours
        for coords in neighbours:
            opponent = self.getAgent(coords)
            score += self.pd(me, opponent)

        # print "Agent " + str(me.coords) + " played %s and scored %d points" % (me.status, score)
        me.points = score
        return me

    # each site is occupied by the agent scoring the highest
    # total of points among the eight neighbours and the agent itself
    def mostPoints(self, coords):
        me = self.getAgent(coords)
        me.statusUpdate = None
        highest_points = me.points

        neighbours = me.neighbours
        for coords in neighbours:
            opponent = self.getAgent(coords)
            if opponent.points > highest_points:
                # print "%s got occupied to %s" % (me.status, opponent.status)
                me.statusUpdate = opponent.status
                if config.emotions:
                    me.emotionUpdate = opponent.emotion
                    me.emotionless = opponent.emotionless
                me.coalition = opponent.coalition
                highest_points = opponent.points
        return me

    # Play the prisoner's dilemma
    def pd(self, me, opponent):
        # Coalition members always cooperate among themselves
        if config.coalitions:
            if me.coalition and opponent.coalition:
                return config.R

        if me.status == 'C':
            if opponent.status == 'C':
                return config.R
            else:
                return config.S
        else:
            if opponent.status == 'C':
                return config.T
            else:
                return config.P
