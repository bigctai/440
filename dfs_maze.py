import random
import numpy as np
import matplotlib.pyplot as plt

# Create a 101x101 grid with 30% black and 70% white cells
n = 101
grid = np.zeros((n,n))

# Set black cells (1) and white cells (0) on the grid with 30% black cells
for i in range(n):
    for j in range(n):
        if random.random() < 0.3:
            grid[i][j] = 1

# Set the start and end points
start = (0,0)
end = (n-1,n-1)

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

# Run DFS on the grid
if dfs(grid, start, end):
    print("Path found")
else:
    print("Path not found")

# Visualize the grid with the path
plt.imshow(grid, cmap='binary')
plt.xticks([])
plt.yticks([])

# Highlight the start and end points
plt.scatter(start[1], start[0], marker='o', s=100, color='r')
plt.scatter(end[1], end[0], marker='o', s=100, color='g')

# Show the plot
plt.show()

