from operator import add
import random

name = "Caliban"

myHistory = []
myLength = 1
oldPelletPos = [-1, -1]

def getDist(arg0, arg1):
    vector = [arg1[i]-arg0[i] for i in range(len(arg0))]
    distance = sum([abs(i) for i in vector])
    return [vector, distance]

def isTurningBack(myPos, direction):
    global myLength, myHistory
    mapOutput = {"left": [-1, 0],
                 "right": [1, 0],
                 "up": [0, -1],
                 "down": [0, 1]}
    newPos = list(map(add, myPos, mapOutput[direction]))
    return newPos in myHistory[-myLength:]

def reset():
    global myLength, myHistory, oldPelletPos
    myLength = 1
    myHistory = []
    oldPelletPos = [-1, -1]

def move(myPos, enemyPos, pelletPos):
    global myLength, oldPelletPos
    toReturn = ""
    enemyVector, enemyDistance = getDist(myPos, enemyPos)
    pelletVector, pelletDistance = getDist(myPos, pelletPos)

    if myPos == oldPelletPos:
        myLength += 1

    if enemyDistance < pelletDistance:
        if enemyVector[0] < enemyVector[1]:
            toReturn = "left" if enemyVector[0]>0 else "right"
        else:
            toReturn = "up" if enemyVector[1]>0 else "down"
    else:
        if pelletVector[0] < pelletVector[1]:
            toReturn = "right" if pelletVector[0]>0 else "left"
        else:
            toReturn = "down" if pelletVector[1]>0 else "up"

    attempts = 0
    while isTurningBack(myPos, toReturn):
        toReturn = random.choice(["left", "right", "up", "down"])
        attempts += 1
        if attempts > 100:
            break
    myHistory.append(myPos)
    oldPelletPos = pelletPos
    return toReturn
