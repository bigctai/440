import random
import numpy as np
from heapq import *
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import time

# Create a 101x101 grid with 30% black and 70% white cells
n = 101
num_grids = 50


class Grid:
    def __init__(self):
        self.grid = np.zeros((n, n))
        # Set black cells (1) and white cells (0) on the grid with 30% black cells
        self.actioncost = {}
        self.hscore = {}
        for i in range(n):
            for j in range(n):
                self.actioncost[i, j] = 1
                if random.random() < 0.3:
                    self.grid[i][j] = 1
        self.grid[0][0] = 0
        self.grid[n-1][n-1] = 0
        self.x_coords = []
        self.y_coords = []
        self.expanded_cells = 0


grids = []
for i in range(num_grids):
    grids.append(Grid())


def heuristic(a, b):
    return (abs(a[0]-b[0]) + abs(a[1] - b[1]))


# a-star algorithm


def a_star_large_g(grid, start, goal):
    # list of 4 directional movements the path can go: up, down, right, left
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    # list where write down the positions that aren't considered again. After each subsequent step, append the current position to this list
    closed_list = set()
    # dictionary that contains all route paths taken in each iteration, contains our 'parent' positions.  At destination, lookup the shortest path from this object.
    came_from = {}
    # dictionary that contains our g-scores
    gscore = {start: 0}
    # dictionary that contains our f-scores
    fscore = {start: heuristic(start, goal)}
    # open list, containing all the positions that are being considered to find the shortest path
    open_list = []
    # pushing the start position and F score onto the open list
    heappush(open_list, (fscore[start],
             100 * fscore[start] - gscore[start], start))

    # want to check for available positions to move to until there are no more options left
    while open_list:
        current = heappop(open_list)[2]
        grid.expanded_cells += 1
        if grid.actioncost[current] == 999:
            data = []
            data.append((-1, -1))
            return data
    # if we've reached the goal (i.e. our current position = the goal position - extract and return the shortest path
        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data
    # otherwise, add current position to closed list
        closed_list.add(current)
    # loop through all possible neighbors, calculating G-Score
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
    # if the neighbor is blocked (1) or is outside the grid, ignore and continue the loop
            if 0 > neighbor[0] or neighbor[0] >= grid.grid.shape[0]:
                continue
            if 0 > neighbor[1] or neighbor[1] >= grid.grid.shape[1]:
                continue
    # if the neighbor is in closed set and the G score is greater than the G score's for that position, then ignore and continue loop
            if neighbor in closed_list:
                continue
            tentative_g_score = gscore[current] + grid.actioncost[neighbor]
    # the G score for the neighbour is less than the other G score's for that position OR if this neighbour is not in the open list
    # (i.e. a new, untested position) then update our lists and add to the open list
            if neighbor not in [i[2] for i in open_list]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                # hscore[neighbor] = heuristic(neighbor)
                fscore[neighbor] = tentative_g_score + \
                    heuristic(neighbor, goal)
                heappush(
                    open_list, (fscore[neighbor], 100 * fscore[neighbor] - gscore[neighbor], neighbor))
            elif tentative_g_score < gscore.get(neighbor, 0):
                gscore[neighbor] = tentative_g_score
                if neighbor == [i[2] for i in open_list]:
                    open_list[i] = open_list[-1]
                    break
                heappop(open_list)
                heapify(open_list)
                fscore[neighbor] = gscore[neighbor] + \
                    heuristic(neighbor, goal)
                # for backward, use gscore[neighbor] as the second argument in the priority queue
                # for forward, use 100 * fscore[start] - gscore[start] as the second argument in the priority queue
                heappush(
                    open_list, (fscore[neighbor], 100 * fscore[neighbor] - gscore[neighbor], neighbor))
    return False


def a_star_small_g(grid, start, goal):
    # list of 4 directional movements the path can go: up, down, right, left
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    # list where write down the positions that aren't considered again. After each subsequent step, append the current position to this list
    closed_list = set()
    # dictionary that contains all route paths taken in each iteration, contains our 'parent' positions.  At destination, lookup the shortest path from this object.
    came_from = {}
    # dictionary that contains our g-scores
    gscore = {start: 0}
    # dictionary that contains our f-scores
    fscore = {start: heuristic(start, goal)}
    # open list, containing all the positions that are being considered to find the shortest path
    open_list = []
    # pushing the start position and F score onto the open list
    heappush(open_list, (fscore[start], start))

    # want to check for available positions to move to until there are no more options left
    while open_list:
        min = 0
        for i in range(len(open_list)):
            if open_list[0][0] == open_list[i][0]:
                if gscore[open_list[0][1]] > gscore[open_list[i][1]]:
                    min = i
            else:
                break
        open_list[min] = open_list[-1]
        current = heappop(open_list)[1]
        grid.expanded_cells += 1
        if grid.actioncost[current] == 999:
            data = []
            data.append((-1, -1))
            return data
    # if we've reached the goal (i.e. our current position = the goal position - extract and return the shortest path
        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data
    # otherwise, add current position to closed list
        closed_list.add(current)
    # loop through all possible neighbors, calculating G-Score
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
    # if the neighbor is blocked (1) or is outside the grid, ignore and continue the loop
            if 0 > neighbor[0] or neighbor[0] >= grid.grid.shape[0]:
                continue
            if 0 > neighbor[1] or neighbor[1] >= grid.grid.shape[1]:
                continue
    # if the neighbor is in closed set and the G score is greater than the G score's for that position, then ignore and continue loop
            if neighbor in closed_list:
                continue
            tentative_g_score = gscore[current] + grid.actioncost[neighbor]
    # the G score for the neighbour is less than the other G score's for that position OR if this neighbour is not in the open list
    # (i.e. a new, untested position) then update our lists and add to the open list
            if neighbor not in [i[1] for i in open_list]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                # hscore[neighbor] = heuristic(neighbor)
                fscore[neighbor] = tentative_g_score + \
                    heuristic(neighbor, goal)
                heappush(
                    open_list, (fscore[neighbor], neighbor))
            elif tentative_g_score < gscore.get(neighbor, 0):
                gscore[neighbor] = tentative_g_score
                if neighbor == [i[1] for i in open_list]:
                    open_list[i] = open_list[-1]
                    break
                heappop(open_list)
                heapify(open_list)
                fscore[neighbor] = gscore[neighbor] + \
                    heuristic(neighbor, goal)
                # for backward, use gscore[neighbor] as the second argument in the priority queue
                # for forward, use 100 * fscore[start] - gscore[start] as the second argument in the priority queue
                heappush(
                    open_list, (fscore[neighbor], neighbor))
    return False


def adaptive_a_star(grid, start, goal):
    # list of 4 directional movements the path can go: up, down, right, left
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    # list where write down the positions that aren't considered again. After each subsequent step, append the current position to this list
    closed_list = set()
    # dictionary that contains all route paths taken in each iteration, contains our 'parent' positions.  At destination, lookup the shortest path from this object.
    came_from = {}
    # dictionary that contains our g-scores
    gscore = {start: 0}
    # dictionary that contains our f-scores
    fscore = {start: heuristic(start, goal)}
    # open list, containing all the positions that are being considered to find the shortest path
    open_list = []
    # pushing the start position and F score onto the open list
    heappush(open_list, (fscore[start], 100 *
             fscore[start] - gscore[start], start))

    # want to check for available positions to move to until there are no more options left
    while open_list:
        current = heappop(open_list)[2]
        grid.expanded_cells += 1
        if grid.actioncost[current] == 999:
            data = []
            data.append((-1, -1))
            return data
    # if we've reached the goal (i.e. our current position = the goal position - extract and return the shortest path
        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                grid.hscore[current] = gscore[goal] - gscore[current]
                current = came_from[current]
            return data
    # otherwise, add current position to closed list
        closed_list.add(current)
    # loop through all possible neighbors, calculating G-Score
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
    # if the neighbor is blocked (1) or is outside the grid, ignore and continue the loop
            if 0 > neighbor[0] or neighbor[0] >= grid.grid.shape[0]:
                continue
            if 0 > neighbor[1] or neighbor[1] >= grid.grid.shape[1]:
                continue
    # if the neighbor is in closed set and the G score is greater than the G score's for that position, then ignore and continue loop
            if neighbor in closed_list:
                continue
            tentative_g_score = gscore[current] + grid.actioncost[neighbor]
    # the G score for the neighbour is less than the other G score's for that position OR if this neighbour is not in the open list
    # (i.e. a new, untested position) then update our lists and add to the open list
            if neighbor not in [i[2]for i in open_list]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                if neighbor in grid.hscore:
                    fscore[neighbor] = tentative_g_score + \
                        grid.hscore[neighbor]
                else:
                    fscore[neighbor] = tentative_g_score + \
                        heuristic(neighbor, goal)
                heappush(
                    open_list, (fscore[neighbor], 100*fscore[neighbor] - gscore[neighbor], neighbor))
            elif tentative_g_score < gscore.get(neighbor, 0):
                gscore[neighbor] = tentative_g_score
                if neighbor == [i[2] for i in open_list]:
                    open_list[i] = open_list[-1]
                    break
                heappop(open_list)
                heapify(open_list)
                if neighbor in grid.hscore:
                    fscore[neighbor] = tentative_g_score + \
                        grid.hscore[neighbor]
                else:
                    fscore[neighbor] = tentative_g_score + \
                        heuristic(neighbor, goal)
                heappush(
                    open_list, (fscore[neighbor], 100*fscore[neighbor] - gscore[neighbor], neighbor))

    return False


def repeated_forward_large_g(grid):
    start = (0, 0)
    goal = (n-1, n-1)
    grid.hscore[start] = heuristic(start, goal)
    while start != goal:
        route = a_star_large_g(grid, start, goal)
        if route[0] == (-1, -1):
            return route
        route = route + [start]
        route = route[::-1]
        for i in range(len(route)):
            coords = route[i]
            if grid.grid[coords[0]][coords[1]] == 1:
                grid.actioncost[coords[0], coords[1]] = 999
                start = route[i-1]
                break
            grid.x_coords.append(route[i][0])
            grid.y_coords.append(route[i][1])
            if i == len(route) - 1:
                start = route[i]
    return route


def repeated_forward_small_g(grid):
    start = (0, 0)
    goal = (n-1, n-1)
    grid.hscore[start] = heuristic(start, goal)
    while start != goal:
        route = a_star_small_g(grid, start, goal)
        if route[0] == (-1, -1):
            return route
        route = route + [start]
        route = route[::-1]
        for i in range(len(route)):
            coords = route[i]
            if grid.grid[coords[0]][coords[1]] == 1:
                grid.actioncost[coords[0], coords[1]] = 999
                start = route[i-1]
                break
            grid.x_coords.append(route[i][0])
            grid.y_coords.append(route[i][1])
            if i == len(route) - 1:
                start = route[i]
    return route


def repeated_backward_a_star(grid):
    start = (0, 0)
    goal = (n-1, n-1)
    grid.hscore[goal] = heuristic(start, goal)
    while start != goal:
        route = a_star_large_g(grid, goal, start)
        if route[0] == (-1, -1):
            return route
        route = route + [goal]
        route = route[::-1]
        for i in range(len(route)):
            coords = route[i]
            if grid.grid[coords[0]][coords[1]] == 1:
                grid.actioncost[coords[0], coords[1]] = 999
                goal = route[i-1]
                break
            grid.x_coords.append(route[i][0])
            grid.y_coords.append(route[i][1])
            if i == len(route) - 1:
                goal = route[i]
    return route


def repeated_adaptive_a_star(grid):
    start = (0, 0)
    goal = (n-1, n-1)
    grid.hscore[start] = heuristic(start, goal)
    while start != goal:
        route = adaptive_a_star(grid, start, goal)
        if route[0] == (-1, -1):
            return route
        route = route + [start]
        route = route[::-1]
        for i in range(len(route)):
            coords = route[i]
            if grid.grid[coords[0]][coords[1]] == 1:
                grid.actioncost[coords[0], coords[1]] = 999
                start = route[i-1]
                break
            # this should probably go in the a* portion
            grid.x_coords.append(route[i][0])
            grid.y_coords.append(route[i][1])
            if i == len(route) - 1:
                start = route[i]
    return route


def clearGrid(grid):
    grid.expanded_cells = 0
    grid.actioncost = {}
    for i in range(n):
        for j in range(n):
            grid.actioncost[i, j] = 1
    grid.hscore = {}
    grid.x_coords = []
    grid.y_coords = []

    # plot map and path


expanded_cells_forward_large_g = 0
expanded_cells_backward = 0
expanded_cells_forward_small_g = 0
expanded_cells_adaptive = 0
valid_grids = 0
for i in range(num_grids):
    route = repeated_forward_small_g(grids[i])
    if not route[0] == (-1, -1):
        expanded_cells_forward_small_g += grids[i].expanded_cells
        valid_grids += 1
        print("expanded cells: " + str(grids[i].expanded_cells))
    clearGrid(grids[i])
    print("hi")
print("Expanded Cells for repeated forward A* favoring small g values: " +
      str(expanded_cells_forward_small_g/valid_grids))
for i in range(num_grids):
    route = repeated_forward_large_g(grids[i])
    if not route[0] == (-1, -1):
        print("expanded cells: " + str(grids[i].expanded_cells))
        expanded_cells_forward_large_g += grids[i].expanded_cells
    clearGrid(grids[i])
print("Expanded Cells for repeated forward A* favoring large g values: " +
      str(expanded_cells_forward_large_g/valid_grids))
for i in range(num_grids):
    route = repeated_backward_a_star(grids[i])
    if not route[0] == (-1, -1):
        expanded_cells_backward += grids[i].expanded_cells
        print("expanded cells: " + str(grids[i].expanded_cells))
    clearGrid(grids[i])
print("Expanded Cells for repeated backward A*: " +
      str(expanded_cells_backward/valid_grids))
for i in range(num_grids):
    route = repeated_adaptive_a_star(grids[i])
    if not route[0] == (-1, -1):
        print("expanded cells: " + str(grids[i].expanded_cells))
        expanded_cells_adaptive += grids[i].expanded_cells
    clearGrid(grids[i])
print("Expanded Cells for adaptive A*: " +
      str(expanded_cells_adaptive/valid_grids))

#fig, ax = plt.subplots(figsize=(10, 10))

#ax.imshow(grids[i].grid, cmap='binary')
#ax.scatter(0, 0, marker="*", color="yellow", s=100)
#ax.scatter(n-1, n-1, marker="*", color="red", s=100)
#ax.plot(grids[i].y_coords, grids[i].x_coords, color="orange")
# plt.show()
