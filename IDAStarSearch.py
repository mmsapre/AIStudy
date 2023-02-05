import heapq

COST = 3

EMPTY = ' '
MARK = '@'
WALL = chr(9608)

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]




class Grid:
    def __init__(self, x, y , start , goal):
        self.x = x
        self.y = y
        self.start = start
        self.goal = goal
        self.walls = []

    def bounds(self, idx):
        (x1, y1) = idx
        return 0 <= x1 < self.x and 0 <= y1 < self.y

    def shift(self, idx):
        return idx not in self.walls

    def neighbhors(self, idx):
        (x1, y1) = idx
        results = [(x1 + 1, y1), (x1, y1 + 1), (x1 - 1, y1), (x1, y1 - 1)]
        results = filter(self.bounds, results)
        results = filter(self.shift, results)
        return results

    def get_manhattan_distance_withcost(self, start, end):
        (start_x, start_y) = start
        (end_x, end_y) = end
        cost_x, cost_y = COST, COST
        if end_x > start_x:
            cost_x = 5
        distance_x = abs(start_x - end_x)
        distance_y = abs(start_y - end_y)
        cost = (cost_x * distance_x) + (cost_y * distance_y)
        return cost


def astarsearch(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    from_grid = {}
    cost_ton = {}
    from_grid[start] = None
    cost_ton[start] = 0

    while not frontier.empty():

        current = frontier.get()

        if current == goal:
            break

        for next in graph.neighbhors(current):

            interim_cost = cost_ton[current] + graph.get_manhattan_distance_withcost(current, next)
            #print(interim_cost)
            if next not in cost_ton or interim_cost < cost_ton[next]:
                cost_ton[next] = interim_cost
                #values = interim_cost + graph.get_manhattan_distance_withcost(next, goal)
                values = interim_cost
                frontier.put(next, values)
                from_grid[next] = current
    return from_grid, cost_ton

def draw_tile(graph, id, style, width):
    #print(style)
    r = " - "
    idWall = id
    if 'number' in style and id in style['number']: r = "%d" % style['number'][id]
    if 'point_to' in style and style['point_to'].get(id, None) is not None:
        (x1, y1) = id
        (x2, y2) = style['point_to'][id]

        if x2 == x1 + 1: r = "E"
        if x2 == x1 - 1: r = "W"
        if y2 == y1 + 1: r = "N"
        if y2 == y1 - 1: r = "S"

    if 'start' in style and id == style['start']:

        r = "I"
    if 'goal' in style and id == style['goal']:
        r = "O"
    if 'path' in style and id in style['path']:

        if id == graph.start:
            r = "S"
        elif id == graph.goal:
            r = "G"
        else:
            r = "*"
    if id in graph.walls: r = WALL
    return r

def draw_grid(graph, width=2, **style ):
    for y in range(graph.y):
        for x in range(graph.x):
            print("%%-%ds" % width % draw_tile(graph, (x, y), style, width), end="")
        print()

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start) # optional
    path.reverse() # optional
    return path

def findPathCost(finalPath,cost,goal):
    return cost.get(goal)
start, goal = (0, 4), (5, 4)
diagram4 = Grid(6, 7, start , goal)
diagram4.walls = [(1, 1), (1, 2), (1, 5),(1,6)]


diagram4.start = start
diagram4.goal = goal
from_grid,cost_ton = astarsearch(diagram4, start, goal)
finalPath=reconstruct_path(from_grid, start=start, goal=goal)
draw_grid(diagram4, width=3, path=finalPath)
print(finalPath)
print(findPathCost(finalPath,cost_ton,goal))

