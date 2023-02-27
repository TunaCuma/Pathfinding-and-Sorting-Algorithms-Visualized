from constants import*
from queue import PriorityQueue

def createAbstractGrid(grid, endX, endY):

    absGrid = [[-1 for x in range(grid.yCount )] for x in range(grid.xCount)]

    for i in range(grid.xCount):
        for j in range(grid.yCount):
            if grid.grid[i][j].status in [EMPTY,TRIED,WEIGHTEDNOD]:
                absGrid[i][j] = 0

    absGrid[endX][endY] = 2
    return absGrid

def createAbsGraph(grid, endX, endY):
  
    absGraph = [[-1 for x in range(grid.yCount )] for x in range(grid.xCount)]
    

    for i in range(grid.xCount):
        for j in range(grid.yCount):
            if grid.grid[i][j].status == EMPTY or grid.grid[i][j].status == TRIED or grid.grid[i][j].status == TRAVELER:
                absGraph[i][j] = 1
            elif grid.grid[i][j].status == WEIGHTEDNOD:
                absGraph[i][j] = 2

    absGraph[endX][endY] = 0


    return absGraph

def breadthFirstSearch(grid,startX, startY, endX, endY):
    bfsTraversalOrder = []
    absGrid = createAbstractGrid(grid, endX, endY)
    cache = [[0 for x in range(grid.yCount )] for x in range(grid.xCount)]


    queue = [(startX, startY)]
    bfsTraversalOrder.append(queue[0])

    
    isReached = False
    while queue and not isReached:
        current = queue.pop(0)
        coordinates = [[0,1],[0,-1],[1,0],[-1,0]]
                    
        for coordinate in coordinates:
            if current[0] + coordinate[0] > -1 and current[1] + coordinate[1] > -1 and current[1] + coordinate[1] < 21 and current[0] + coordinate[0]< 51 :
                if absGrid[current[0] + coordinate[0]][current[1] + coordinate[1]] == 0 :
                    absGrid[current[0] + coordinate[0]][current[1] + coordinate[1]] = 1
                    queue.append((current[0] + coordinate[0] , current[1] + coordinate[1]))
                    bfsTraversalOrder.append((current[0] + coordinate[0] , current[1] + coordinate[1]))
                    cache[current[0] + coordinate[0]][current[1] + coordinate[1]] = cache[current[0]][current[1]] + 1
                elif absGrid[current[0] + coordinate[0]][current[1] + coordinate[1]] == 2:
                    isReached = True
                    break
                
    path = []

    while cache[current[0]][current[1]] != 0:
        path.append(current)

        for coordinate in coordinates:
            if current[0] + coordinate[0] > -1 and current[1] + coordinate[1] > -1 and current[1] + coordinate[1] < 21 and current[0] + coordinate[0]< 51 :
                if cache[current[0] + coordinate[0]][current[1] + coordinate[1]] == cache[current[0]][current[1]] - 1:
                    current = (current[0] + coordinate[0], current[1] + coordinate[1])
                    break
    return bfsTraversalOrder, path

def depthFirstSearch(grid, startX, startY, endX, endY):
    dfsTraversalOrder = []
    absGrid = createAbstractGrid(grid, endX, endY)
    cache = [[0 for x in range(grid.yCount )] for x in range(grid.xCount)]

    stack = [(startX,startY)]
    dfsTraversalOrder.append(stack[-1])

    isReached = False
    while stack and not isReached:
        current = stack.pop(-1)
        coordinates = [[0,1],[1,0],[0,-1],[-1,0]]
                    
        for coordinate in coordinates:
            if current[0] + coordinate[0] > -1 and current[1] + coordinate[1] > -1 and current[1] + coordinate[1] < 21 and current[0] + coordinate[0]< 51 :
                if absGrid[current[0] + coordinate[0]][current[1] + coordinate[1]] == 0 :
                    stack.append((current[0] , current[1]))
                    absGrid[current[0] + coordinate[0]][current[1] + coordinate[1]] = 1
                    dfsTraversalOrder.append((current[0] + coordinate[0] , current[1] + coordinate[1]))
                    stack.append((current[0] + coordinate[0] , current[1] + coordinate[1]))
                    cache[current[0] + coordinate[0]][current[1] + coordinate[1]] = cache[current[0]][current[1]] + 1
                    break
                elif absGrid[current[0] + coordinate[0]][current[1] + coordinate[1]] == 2:
                    isReached = True
                    break
    
        path = []

        while cache[current[0]][current[1]] != 0:
            path.append(current)

            for coordinate in coordinates:
                if current[0] + coordinate[0] > -1 and current[1] + coordinate[1] > -1 and current[1] + coordinate[1] < 21 and current[0] + coordinate[0]< 51 :
                    if cache[current[0] + coordinate[0]][current[1] + coordinate[1]] == cache[current[0]][current[1]] - 1:
                        current = (current[0] + coordinate[0], current[1] + coordinate[1])
                        break

    return dfsTraversalOrder , path

def greedyBestSearch(grid,startX, startY, endX, endY):
    greedyBestSearchTraversalOrder = []
    absGrid = createAbstractGrid(grid,endX,endY)
    cache = [[0 for x in range(grid.yCount )] for x in range(grid.xCount)]

    stack = [(startX,startY)]
    greedyBestSearchTraversalOrder.append(stack[-1])


    isReached = False
    while stack and not isReached:
        current = stack.pop(-1)
        coordinates = []


        if endX == current[0]:
            if (endY > current[1]):
                coordinates = [(0,1),(1,0),(-1,0),(0,-1)]
            else:
                coordinates = [(0,-1),(1,0),(-1,0),(0,1)]
        elif endY == current[1]:
            if (endX > current[0]):
                coordinates = [(1,0),(0,-1),(0,1),(-1,0)]
            else:
                coordinates = [(-1,0),(0,-1),(0,1),(1,0)]
        elif endX > current[0] and endY > current[1]:
            if endX - current[0] > endY - current[1]:
                coordinates = [(1,0),(0,1),(0,-1),(-1,0)]
            else:
                coordinates = [(0,1),(1,0),(-1,0),(0,-1)]
        elif endX > current[0] and endY < current[1]: 
            if endX - current[0] > current[1] - endY:
                coordinates = [(1,0),(0,-1),(0,1),(-1,0)]
            else:
                coordinates = [(0,-1),(1,0),(-1,0),(0,1)]
        elif endY > current[1]:
            if current[0] - endX > endY - current[1]:
                coordinates = [(-1,0),(0,1),(0,-1),(1,0)]
            else:
                coordinates = [(0,1),(-1,0),(1,0),(0,-1)]
        else:
            if current[0] - endX > current[1] - endY:
                coordinates = [(-1,0),(0,-1),(0,1),(1,0)]
            else:
                coordinates = [(0,-1),(-1,0),(1,0),(0,1)]

        for coordinate in coordinates:
            if current[0] + coordinate[0] > -1 and current[1] + coordinate[1] > -1 and current[1] + coordinate[1] < 21 and current[0] + coordinate[0]< 51 :
                if absGrid[current[0] + coordinate[0]][current[1] + coordinate[1]] == 0 :
                    stack.append((current[0] , current[1]))
                    absGrid[current[0] + coordinate[0]][current[1] + coordinate[1]] = 1
                    greedyBestSearchTraversalOrder.append((current[0] + coordinate[0] , current[1] + coordinate[1]))
                    stack.append((current[0] + coordinate[0] , current[1] + coordinate[1]))
                    cache[current[0] + coordinate[0]][current[1] + coordinate[1]] = cache[current[0]][current[1]] + 1
                    break
                elif absGrid[current[0] + coordinate[0]][current[1] + coordinate[1]] == 2:
                    isReached = True
                    break
        
    path = []

    while cache[current[0]][current[1]] != 0:
        path.append(current)

        for coordinate in coordinates:
            if current[0] + coordinate[0] > -1 and current[1] + coordinate[1] > -1 and current[1] + coordinate[1] < 21 and current[0] + coordinate[0]< 51 :
                if cache[current[0] + coordinate[0]][current[1] + coordinate[1]] == cache[current[0]][current[1]] - 1:
                    current = (current[0] + coordinate[0], current[1] + coordinate[1])
                    break

    return greedyBestSearchTraversalOrder, path

def Dijkstra(grid,startX, startY, endX, endY):
    DijkstraTraversalOrder = []
    path =  []
    absGraph = createAbsGraph(grid, endX, endY)
    
    distances = [[10000 for x in range(grid.yCount )] for x in range(grid.xCount)]
    distances[startX][startY] = 0

    pq = PriorityQueue()
    pq.put((0,(startX,startY)))

    DijkstraTraversalOrder.append((startX,startY))

    
    isReached = False
    coordinates = [[0,1],[0,-1],[1,0],[-1,0]]
    
    while pq and not isReached:
        current = pq.get()
                    
        for coordinate in coordinates:
            if current[1][0] + coordinate[0] > -1 and current[1][1] + coordinate[1] > -1 and current[1][1] + coordinate[1] < 21 and current[1][0] + coordinate[0]< 51 and absGraph[current[1][0] + coordinate[0]][current[1][1] + coordinate[1]] > 0:
                if distances[current[1][0] + coordinate[0]][current[1][1] + coordinate[1]] > current[0] + absGraph[current[1][0] + coordinate[0]][current[1][1] + coordinate[1]]:
                    distances[current[1][0] + coordinate[0]][current[1][1] + coordinate[1]] = current[0] + absGraph[current[1][0] + coordinate[0]][current[1][1] + coordinate[1]]
                    pq.put((distances[current[1][0] + coordinate[0]][current[1][1] + coordinate[1]], (current[1][0] + coordinate[0],current[1][1] + coordinate[1])))
                    DijkstraTraversalOrder.append((current[1][0] + coordinate[0],current[1][1] + coordinate[1]))
            elif current[1][0] + coordinate[0] == endX and current[1][1] + coordinate[1] == endY:
                distances[current[1][0] + coordinate[0]][current[1][1] + coordinate[1]] = current[0] + absGraph[current[1][0] + coordinate[0]][current[1][1] + coordinate[1]]
                isReached = True
    

    while current[0] != 0:
        path.append(current[1])

        for coordinate in coordinates:
            if current[1][0] + coordinate[0] > -1 and current[1][1] + coordinate[1] > -1 and current[1][1] + coordinate[1] < 21 and current[1][0] + coordinate[0]< 51 :
                if current[0] == distances[current[1][0] + coordinate[0]][current[1][1] + coordinate[1]] + absGraph[current[1][0] ][current[1][1]]:
                    current = (distances[current[1][0] + coordinate[0]][current[1][1] + coordinate[1]],(current[1][0] + coordinate[0], current[1][1] + coordinate[1]))
                    break

    return DijkstraTraversalOrder, path

def aStar(grid, start, end):
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = dict()
    distances = [[10000 for x in range(grid.yCount )] for x in range(grid.xCount)]
    distances[start[0]][start[1]] = 0
    came_from[start] = None
    absGraph = createAbsGraph(grid,end[0],end[1])
    aStarTraversal = []

    coordinates = [[0,1],[0,-1],[1,0],[-1,0]]
    isReached = False
    while not frontier.empty() and not isReached:
        current = frontier.get()
        aStarTraversal.append(current[1])

        if current[1] == end:
            break
        

        for coordinate in coordinates:
            if current[1][0] + coordinate[0] > -1 and current[1][1] + coordinate[1] > -1 and current[1][1] + coordinate[1] < 21 and current[1][0] + coordinate[0]< 51 and absGraph[current[1][0] + coordinate[0]][current[1][1] + coordinate[1]] > 0:
                if distances[current[1][0] + coordinate[0]][current[1][1] + coordinate[1]] > distances[current[1][0]][current[1][1]] + absGraph[current[1][0] + coordinate[0]][current[1][1] + coordinate[1]]:
                    distances[current[1][0] + coordinate[0]][current[1][1] + coordinate[1]] = distances[current[1][0]][current[1][1]] + absGraph[current[1][0] + coordinate[0]][current[1][1] + coordinate[1]]
                    priority = distances[current[1][0] + coordinate[0]][current[1][1] + coordinate[1]] + abs(end[0] - (current[1][0] + coordinate[0])) + abs(end[1] - (current[1][1] + coordinate[1]))
                    frontier.put((priority, (current[1][0] + coordinate[0],current[1][1] + coordinate[1])))
                    came_from[(current[1][0] + coordinate[0],current[1][1] + coordinate[1])] = (current[1])
            elif current[1][0] + coordinate[0] == end[0] and current[1][1] + coordinate[1] == end[1]:
                distances[current[1][0] + coordinate[0]][current[1][1] + coordinate[1]] = current[0] + absGraph[current[1][0] + coordinate[0]][current[1][1] + coordinate[1]]
                isReached = True

    path = []
    pathTemp = current[1]
    while came_from[pathTemp]:
        path.append(pathTemp)
        pathTemp = came_from[pathTemp]
    
    return aStarTraversal , path