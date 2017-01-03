import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

OFF = 0
ON = 255
vals = [ON, OFF]

def randomGrid(N):
    """returns a grid of NxN random values"""
    return np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N,N)

def addGlider(i, j, grid):
    """adds a glider with top left cell at (i, j)"""
    glider = np.array([[0, 0, 255],
                       [255, 0, 255],
                       [0, 255, 255]])
    grid[i:i+3, j:j+3] = glider

def update(frameNum, img, grid, N):
    # copy grid since we require 8 neighbors for calculation
    # and we go line by line
    newGrid = grid.copy()
    for i in range(N):
        for j in range(N):
            # compute 8-neighbor sum using toroidal boundary conditions
            # x and y wrap around so that the simulation take place on a toroidal surface
            total = int((grid[i, (j-1)%N] + grid[i, (j+1)%N] +
                         grid[(i-1)%N, j] + grid[(i+1)%N, j] +
                         grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] +
                         grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N]) / 255)

            # apply conways rules
            if grid[i, j] == ON:
                if(total < 2) or (total > 3):
                    newGrid[i, j] = OFF

            else:
                if total == 3:
                    newGrid[i, j] = ON

    # update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,

# main method
def main():
    # parse arguments
    parser = argparse.ArgumentParser(description="Conway's Game of Life Simulation")

    # add arguments
    parser.add_argument('--grid-size', dest='N', required=False)
    parser.add_argument('--mov-file', dest='movfile', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--glider', action='store_true', required=False)
    args = parser.parse_args()

    # grid size
    N = 100
    if args.N and int(args.N) > 8:
        N = int(args.N)

    # animation update interval
    updateInterval = 50
    if args.interval:
        updateInterval = int(args.interval)

    # make grid
    grid = np.array([])
    if args.glider:
        grid = np.zeros(N*N).reshape(N,N)
        addGlider(1, 1, grid)
    else:
        # randomize grid population
        grid = randomGrid(N)

    # configure animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ),
                                  frames=10, interval=updateInterval,
                                  save_count=50)

    # number of frames?
    # set the output file
    if args.movfile:
        ani.save(args.movfile, fps=30, extra_args=['-vcodec','libx264'])

    plt.show()

# call main
if __name__ == '__main__':
    main()

# grid = np.zeros(N*N).reshape(N, N)
# addGlider(1, 1, grid)

# x = np.array([[0 ,0, 255], [255, 255, 0], [0, 255, 0]])
# plt.imshow(x, interpolation='nearest')
# plt.show()
