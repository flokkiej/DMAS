#!/usr/bin/python
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import time
import random

import emotion, agent, grid

pd_payoff = [[(3,3), (5,0)], [(0,5), (1,1)]]



def main():
	gridSize = int(sys.argv[1]) if len(sys.argv)>1 else 15
	#print "Grid size: %d\n" % gridSize
	g = grid(gridSize)
	g.fillGrid()
	plt.ion()
	g.plotGrid()
	g.simulate(50)
	plt.ioff()
	#g.play((14,1))
	#a = agent(10, (15,15))
	#print a.returnNeighbours2(15)
	return

if __name__ == "__main__":
	main()
