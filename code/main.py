#!/usr/bin/python
import sys
import numpy as np
import random

import emotion, grid
from grid import *


def main():
	gridSize = int(sys.argv[1]) if len(sys.argv)>1 else 15
	g = grid(gridSize)
	g.fillGrid()
	plt.ion()
	g.plotGrid()
	g.plotRate()
	g.simulate(50)
	plt.ioff()
	return

if __name__ == "__main__":
	main()
