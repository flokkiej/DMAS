import itertools
import config
import random


class agent(object):
    def __init__(self, initialStatus, (x, y)):
        self.coords = (x, y)
        self.status = initialStatus
        self.statusUpdate = None
        self.neighbours = self.meetNeighbours()
        self.points = 0
        if config.emotions:
            rand = random.random()
            if rand > config.emotionsRate:
                self.emotionless = True
            else:
                self.emotionless = False
            self.emotion = None
            self.emotionUpdate = None
        self.coalition = False

    def meetNeighbours(self):
        # Returns all neighbouring agents
        neighbours = []
        (x, y) = self.coords

        # Define the xrange and yrange for coord
        a = [x - 1, x, x + 1]
        b = [y - 1, y, y + 1]

        # Clean up outside borders
        a2 = [x for x in a if x >= 0 and x < config.gridSize]
        b2 = [y for y in b if y >= 0 and y < config.gridSize]

        # Get all permutations
        neighbours = list(itertools.product(a2, b2))

        # You also play with yourself
        # neighbours.remove(self.coords)
        return neighbours
