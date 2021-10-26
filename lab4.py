import copy
import random
import math

class Node:
    def __init__(self, value, parent, goodOrBad) -> None:
        self.value = value
        self.parent = parent
        self.h = 0
        self.goodOrBad = goodOrBad
    


def simulatedAnnealing(current):
    t = 1
    alreadyTravelledStates = [current]
    potentialMoves = []
    print("Initial state:")
    printboard(current.value)
    print("")
    while True:
        t += 1
        T = schedule(t)
        if (T == 0):
            return current
        for action in possibleActions(current, alreadyTravelledStates):
            potentialMoves.append(action)
        next = potentialMoves[random.randint(0, len(potentialMoves) - 1)]
        #higher manhattanValue = better
        deltaE = manHattanValue(next) - manHattanValue(current)
        if deltaE > 0:
            alreadyTravelledStates.append(next)
            current = next
            printboard(current.value)
            print("(value = ",end="")
            print(current.h,end="")
            print(")")
            print("")
        else:
            print(math.exp(deltaE/T))
            if random.uniform(0,1) < math.exp(deltaE/T): #math is backwards here , will always go here
                alreadyTravelledStates.append(next)
                current = next
                printboard(current.value)
                print("(value = ",end="")
                print(current.h, end="")
                print("), BAD MOVE was chosen")
                print("")
        potentialMoves = []

def schedule(t):
    alteredTValue = 5
    while t > 0:
        alteredTValue = alteredTValue - 0.01
        t = t - 1
    return alteredTValue

def printboard(board):
    for row in board:
        for value in row:
            if value == 0:
                print("  ", end='')
            else:
                print(str(value) + " ", end='')
        print("")
        

def manHattanValue(state):
    HValue = 0
    oneGoal = (0,1)
    twoGoal = (0,2)
    threeGoal = (1,0)
    fourGoal = (1,1)
    fiveGoal = (1,2)
    sixGoal = (2,0)
    sevenGoal = (2,1)
    eightGoal = (2,2)
    value = state.value
    for row in range(3):
            for col in range(3):
                if value[row][col] == 1:
                    HValue += abs(oneGoal[0] - row)
                    HValue += abs(oneGoal[1] - col)
                elif value[row][col] == 2:
                    HValue += abs(twoGoal[0] - row)
                    HValue += abs(twoGoal[1] - col)
                elif value[row][col] == 3:
                    HValue += abs(threeGoal[0] - row)
                    HValue += abs(threeGoal[1] - col)
                elif value[row][col] == 4:
                    HValue += abs(fourGoal[0] - row)
                    HValue += abs(fourGoal[1] - col)
                elif value[row][col] == 5:
                    HValue += abs(fiveGoal[0] - row)
                    HValue += abs(fiveGoal[1] - col)
                elif value[row][col] == 6:
                    HValue += abs(sixGoal[0] - row)
                    HValue += abs(sixGoal[1] - col)
                elif value[row][col] == 7:
                    HValue += abs(sevenGoal[0] - row)
                    HValue += abs(sevenGoal[1] - col)
                elif value[row][col] == 8:
                    HValue += abs(eightGoal[0] - row)
                    HValue += abs(eightGoal[1] - col)
    state.h = 0 - HValue
    return(0-HValue)

def possibleActions(currentState, alreadyTraveledStates):
    currentStateValue = currentState.value #grab the 2d array value from the node
    possibleActionsList = []
    NewZeroLocations = []
    ZeroRow = -1 
    ZeroCol = -1
    for row in range(3):  #find where the empty tile is
        for col in range(3):
            if currentStateValue[row][col] == 0:
                ZeroRow = row
                ZeroCol = col

    
    moveZeroUp = [ZeroRow -1, ZeroCol] #coords of the empty stone if it moved up
    moveZeroDown = [ZeroRow + 1, ZeroCol] #coords of the empty stone if it moved down
    moveZeroRight = [ZeroRow, ZeroCol + 1] #coords of the empty stone if it moved right
    moveZeroLeft = [ZeroRow, ZeroCol - 1] #coords of the empty stone if it moved left

    #boundary check, if in bounds, add to a list
    if(moveZeroUp[0] > -1):
        NewZeroLocations.append(moveZeroUp)
    if(moveZeroDown[0] < 3):
        NewZeroLocations.append(moveZeroDown)
    if(moveZeroRight[1] < 3):
        NewZeroLocations.append(moveZeroRight)
    if(moveZeroLeft[1] > -1):
        NewZeroLocations.append(moveZeroLeft)
    #these are the places the empty stone can move
    #for each of these options, we will find what the new board state is
    for option in NewZeroLocations:
        possibleActionTemp = copy.deepcopy(currentStateValue)  #giving same address 
        temp = currentStateValue[option[0]][option[1]] #get value that is to be swapped with 0
        possibleActionTemp[option[0]][option[1]] = 0 #put zero into that spot
        possibleActionTemp[ZeroRow][ZeroCol] = temp #put the temporary value into the zero position
        duplicateFound = False
        for i in range(len(alreadyTraveledStates)): #make sure this state has not already been explored
            if(alreadyTraveledStates[i].value == possibleActionTemp):
                duplicateFound = True
        if(duplicateFound == True):
            continue
        else:
             possibleActionsList.append(Node(possibleActionTemp, currentState, "N/A")) #duplicate found, make a new Node 
    
    return(possibleActionsList) #return list of Nodes with new states


   # def Value
#x=Node([[8,1,2],[3,4,5],[6,7,0]], None, "N/A")
simulatedAnnealing(Node([[1,2,3],[4,5,8],[6,7,0]], None, "N/A"))
#print(manHattanValue(x))
#print(schedule(100))
#print(random.uniform(0,1))
#print(math.exp(-5/5)) #200 seems highest we can go