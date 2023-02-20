import random
import numpy as np
from heapq import *
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

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

def heuristic(a, b):
    return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2

#a-star algorithm
def a_star(grid, start, end):
    #list of 4 directional movements the path can go: up, down, right, left
    neighbors = [(0,1),(0,-1),(1,0),(-1,0)]
    #list where write down the positions that aren't considered again. After each subsequent step, append the current position to this list
    close_set = set()
    #dictionary that contains all route paths taken in each iteration, contains our 'parent' positions.  At destination, lookup the shortest path from this object.
    came_from = {}
    #dictionary that contains our g-scores by iteration
    gscore = {start:0}
    #dictionary that contains our f-scores by iteration
    fscore = {start:heuristic(start, end)}
    #open list, containing all the positions that are being considered to find the shortest path
    oheap = []
    #pushing the start position and F score onto the open list
    heappush(oheap, (fscore[start], start))
    
    while oheap:

        current = heappop(oheap)[1]

        if current == end:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j            
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[0] < grid.shape[0]:
                if 0 <= neighbor[1] < grid.shape[1]:                
                    if grid[neighbor[0]][neighbor[1]] == 1:
                        continue
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue
                
            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue
                
            if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, end)
                heappush(oheap, (fscore[neighbor], neighbor))
                
    return False

route = a_star(grid, start, end)
route = route + [start]
route = route[::-1]
print(route)

x_coords = []
y_coords = []

for i in (range(0,len(route))):
    x = route[i][0]
    y = route[i][1]
    x_coords.append(x)
    y_coords.append(y)

# plot map and path

fig, ax = plt.subplots(figsize=(10,10))
ax.imshow(grid, cmap='binary')
ax.scatter(start[1],start[0], marker = "*", color = "yellow", s = 100)
ax.scatter(end[1],end[0], marker = "*", color = "red", s = 100)
ax.plot(y_coords,x_coords, color = "orange")

plt.show()