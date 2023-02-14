import random
import numpy as np
import matplotlib.pyplot as plt

# Generate 50 grids
n = 101
num_grids = 50
grids = []
paths = []

# Define DFS function
def dfs(grid, start, end):
    stack = [start]
    visited = set()

    while stack:
        x, y = stack.pop()
        if (x, y) == end:
            return True
        if 0 <= x < n and 0 <= y < n and grid[x][y] == 0 and (x, y) not in visited:
            visited.add((x, y))
            stack.append((x-1, y))
            stack.append((x+1, y))
            stack.append((x, y-1))
            stack.append((x, y+1))

    return False

for i in range(num_grids):
    # Create a 50x50 grid with 30% black and 70% white cells
    grid = np.zeros((n,n))

    # Set black cells (1) and white cells (0) on the grid with 30% black cells
    for i in range(n):
        for j in range(n):
            if random.random() < 0.3:
                grid[i][j] = 1

    # Set the start and end points
    start = (0,0)
    end = (n-1,n-1)

    # Run DFS on the grid
    if dfs(grid, start, end):
        print("Path found")
        paths.append(True)
    else:
        print("Path not found")
        paths.append(False)

    # Store the grid
    grids.append(grid)



# Visualize the grids with the paths
for i in range(num_grids):
    plt.subplot(5, 10, i+1)
    plt.imshow(grids[i], cmap='binary')
    plt.xticks([])
    plt.yticks([])
    if paths[i]:
        # Highlight the start and end points
        plt.scatter(start[1], start[0], marker='o', s=100, color='r')
        plt.scatter(end[1], end[0], marker='o', s=100, color='g')

# Show the plots
plt.show()
