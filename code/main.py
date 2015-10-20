#!/usr/bin/python
#
# The main program, initializes the grid and initiates the game
# By Stefan Bussemaker, Folkert de Vries, Sybren R\"omer
import grid
import matplotlib.pyplot as plt


def main():
    g = grid.grid()
    plt.ion()
    g.simulate()
    plt.ioff()
    g.plotResults()


if __name__ == "__main__":
    main()
