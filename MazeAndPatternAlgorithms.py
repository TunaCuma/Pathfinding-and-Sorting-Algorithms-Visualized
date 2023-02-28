from constants import Constants
import random

def frame(grid,x,y):#yield can be implemented here
    for i in range(y):
        if grid.grid[0][i].status == Constants.EMPTY:
            yield
            grid.grid[0][i].change_status(Constants.WALL)
        if grid.grid[x-1][i].status == Constants.EMPTY:
            yield
            grid.grid[x-1][i].change_status(Constants.WALL)
    for i in range(x):
        if grid.grid[i][0].status == Constants.EMPTY:
            yield
            grid.grid[i][0].change_status(Constants.WALL)
        if grid.grid[i][y-1].status == Constants.EMPTY:
            yield
            grid.grid[i][y-1].change_status(Constants.WALL)
    grid.frameFinished = True

def RecursionMaze(grid,xstart,xend,ystart,yend,skew= None):
    height = yend-ystart+1
    width = xend-xstart+1
    if width ==1 or height ==1:
        return

    if skew == Constants.HORIZONTAL:
        choice = choiceOfWay(0,80)
    elif skew == Constants.VERTICAL:
        choice = choiceOfWay(0,20)
    else:
        choice = choiceOfWay((height-width)*1.5)
    funcs = []

    if choice == Constants.HORIZONTAL:
        wally = ystart + (random.randint(1,height//2)*2)-1
        while grid.grid[xstart-1][wally].status == Constants.EMPTY or grid.grid[xend+1][wally].status == Constants.EMPTY:
            wally = ystart + (random.randint(1,height//2)*2)-1
        hole = (random.randint(0,width//2)*2)

        for i in range(width):
            if i != hole and grid.grid[xstart+ i][wally].status==Constants.EMPTY:
                yield
                grid.grid[xstart+ i][wally].change_status(Constants.WALL)
        
        funcs.append(RecursionMaze(grid,xstart,xend,ystart,wally-1,skew))
        funcs.append(RecursionMaze(grid,xstart,xend,wally+1,yend,skew))

        for func in funcs:
            try:
                yield from func
            except StopIteration:
                funcs.remove(func)

    elif choice == Constants.VERTICAL:
        wallx = xstart + (random.randint(1,width//2)*2)-1
        while grid.grid[wallx][ystart-1].status == Constants.EMPTY or grid.grid[wallx][yend+1].status == Constants.EMPTY:
            wallx = xstart + (random.randint(1,width//2)*2)-1

        hole = (random.randint(0,height//2)*2)

        for i in range(height):
            if i != hole and grid.grid[wallx][ystart+ i].status ==Constants.EMPTY:
                yield
                grid.grid[wallx][ystart+ i].change_status(Constants.WALL)

        funcs.append(RecursionMaze(grid,xstart,wallx-1,ystart,yend,skew))
        funcs.append(RecursionMaze(grid,wallx+1,xend,ystart,yend,skew))

        for func in funcs:
            try:
                yield from func
            except StopIteration:
                funcs.remove(func)

def choiceOfWay(skewAmount,horizontalOdds = 50):
    horizontalOdds += skewAmount
    if random.randint(1,100) < horizontalOdds:
        return Constants.HORIZONTAL
    else:
        return Constants.VERTICAL

def basicMaze(grid):
    for i in range(grid.xCount):
        for j in range(grid.yCount):
            if grid.grid[i][j].status == Constants.EMPTY and 1 == random.randint(1,5):
                grid.grid[i][j].change_status(Constants.WALL)

def basicWeighted(grid):
    for i in range(grid.xCount):
        for j in range(grid.yCount):
            if grid.grid[i][j].status == Constants.EMPTY and 1 == random.randint(1,5):
                grid.grid[i][j].change_status(Constants.WEIGHTEDNOD)


def stairsPattern(grid):
    y = grid.yCount
    for i in range(grid.xCount-1):
        
        if y-i-1 >1:
            if grid.grid[i][y-i-1].status == Constants.EMPTY:
                grid.grid[i][y-i-1].change_status(Constants.WALL)
        elif i-y+3 < y-1:
            if grid.grid[i][i-y+3].status == Constants.EMPTY:
                grid.grid[i][i-y+3].change_status(Constants.WALL)
        elif 2*y-i+14 >1:
            if grid.grid[i][2*y-i+14].status == Constants.EMPTY:
                grid.grid[i][2*y-i+14].change_status(Constants.WALL)

def basicMaze(grid):
    for i in range(grid.xCount):
        for j in range(grid.yCount):
            if grid.grid[i][j].status == Constants.EMPTY and 1 == random.randint(1,5):
                grid.grid[i][j].change_status(Constants.WALL)

def basicWeighted(grid):
    for i in range(grid.xCount):
        for j in range(grid.yCount):
            if grid.grid[i][j].status == Constants.EMPTY and 1 == random.randint(1,5):
                grid.grid[i][j].change_status(Constants.WEIGHTEDNOD)

