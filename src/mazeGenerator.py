import random

# Joshua Lin - November 12, 2026
# Provides a sample maze layout for the Maze minigame.
# Will be replaced with the randomized maze generator.

PATH = 0
WALL = 1
START = 2
DESTINATION = 3
PORTAL = 4

#Jack Larson 11/15/2026
#Generates a maze using a random depth first search.
#Sets the starting point as a random location and the end as the first dead end.
#Tracks dead ends to some extent to allow for implementation of portals if so choosen.
#(Currently portals have no effect and are not included in maze generation.)
def generateMaze(rows, cols, seed):
    #default to waffle pattern
    maze = []

    for y in range(0,rows):
        row = []
        for x in range(0,cols):
            row.append(min(1,(y+1)%2+(x+1)%2))
        maze.append(row)



    #make rand
    rand = random.Random(seed)

    #empty burnt
    burnt = []
    #random start
    border = [(1+2*rand.randint(0,rows//2-1),1+2*rand.randint(0,cols//2-1))]
    #set start as start point for player as well
    maze[border[0][0]][border[0][1]] = 2
    #no dead ends yet
    deadEnds = []

    while(len(border) > 0):
        #grab top of stack
        index = len(border)-1
        point = border[index]

        #start with all possible directions
        directions = [(1,0),(0,1),(-1,0),(0,-1)]

        #remove by distance to wall
        if(point[0] == 1):
            directions.remove((-1,0))
        if(point[0] == rows-2):
            directions.remove((1,0))
        if(point[1] == 1):
            directions.remove((0,-1))
        if(point[1] == cols-2):
            directions.remove((0,1))

        #remove by burnt
        for direction in directions[:]:
            potential = (point[0]+2*direction[0],point[1]+2*direction[1])
            if(potential in burnt):
                directions.remove(direction)

        #possible dead end, pop stack and mark end if needed
        if(len(directions) == 0):
            border.remove(point)
            if point not in burnt:
                deadEnds.append(point)
                burnt.append(point)
            continue

        #remove wall and add to stack
        vector = directions[rand.randint(0,len(directions)-1)]
        maze[point[0]+vector[0]][point[1]+vector[1]] = 0
        border.append((point[0]+2*vector[0],point[1]+2*vector[1]))
        #burn point
        if(point not in burnt):
            burnt.append(point)
    
    #pull random end to make the dest
    destinationIndex = rand.randint(0, len(deadEnds)-1)
    destination = deadEnds[destinationIndex]
    maze[destination[0]][destination[1]] = 3
    deadEnds.remove(destination)


    #add portals if possible
    if len(deadEnds) >= 2:
        for i in range(0,2):
            portalIndex = rand.randint(0, len(deadEnds)-1)
            portal = deadEnds[portalIndex]
            maze[portal[0]][portal[1]] = 4
            deadEnds.remove(portal)


    return maze
