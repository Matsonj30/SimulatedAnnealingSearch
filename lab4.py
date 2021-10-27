import copy
import random
import math
#Jared Matson
#1570490
#Lab4.py
#A demonstration of the simulated annealing program, does not always find the best solution a the program does not run forever, but
#will find the correction solution ~10-20% of the time with luck

#class Node
#This class represents a possible state in the puzzle
# value = the value of the Node e.g
#[1 8 2]
#[2   4]
#[7 6 5]
#gvalue = the gValue of the Node, e.g the amount of moves it took to get to that state
#parent = the parent Node or previous state of the node
#goodOrBad = if the Node is a result of a bad move
class Node:
    def __init__(self, value, parent, goodOrBad) -> None:
        self.value = value
        self.parent = parent
        self.h = 0
        self.goodOrBad = goodOrBad
    

#def simulated annealing(Current)
#given an initial state, will use simulated annealing to attempt and find the best state
def simulatedAnnealing(current):
    goalFound = False
    t = 1
    alreadyTravelledStates = [current]
    potentialMoves = []
    print("Initial state:")
    printboard(current.value)
    print("")
    while True: #checking to see if goal state was found but randomly escaped
        if(current.value == [[0,1,2],[3,4,5],[6,7,8]]):
            goalFound = True
        t += 1
        T = schedule(t)
        alreadyTravelledStates.append(current)
        if (T == 0):
            print(goalFound)
            return current
        for action in possibleActions(current, alreadyTravelledStates):
            potentialMoves.append(action)
        next = potentialMoves[random.randint(0, len(potentialMoves) - 1)] #random move in list
        #higher manhattanValue = better
        deltaE = manHattanValue(next) - manHattanValue(current)
        if deltaE > 0:
            current = next
            printboard(current.value)
            print("(value = ",end="")
            print(current.h,end="")
            print(")")
            print("")
        else:
            x = random.uniform(0.5,1) #due to how random works, seem to have best luck with higher random numbers (very slightly lower probability of initially accepting bad states)
            y =  math.exp(deltaE/T)
            if x < y: #probabilty of taking worse move
                current = next
                printboard(current.value)
                print("(value = ",end="")
                print(current.h, end="")
                print("), BAD MOVE was chosen")
                print("")
            
        potentialMoves = []
        alreadyTravelledStates = [] #only keep track of current parent node
#schedule(t)
#given t, will return T to use in the annealing process
#parameters : t - current interation number
#Returns : T - temperature to be used in probability
def schedule(t):
    alteredTValue = 5
    while t > 0:
        alteredTValue = alteredTValue - 0.005
        t = t - 1
    return round(alteredTValue,3)

# def printBoard(board)
# Will iterate through the puzzle (2d array) and will print the 
# values to better represent what the 8 number puzzle actually looks like

# Parameters:
# board - the board being printed

# Returns:
# N/A
def printboard(board):
    for row in board:
        for value in row:
            if value == 0:
                print("  ", end='')
            else:
                print(str(value) + " ", end='')
        print("")
        
#Given a state, will return its manhattan distance (0 - mahattan distance)
#Parameters : State - the state you are wanting to get the h value of
#Returns: negative hueristic value
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
# def possibleActions(currentState, alreadyTraveledStates)
# given the current Node and a list of already already travelled states, will determine
# other potential moves that can be made

# Parameters:
# currentState - the Node we want to branch out from
# alreadyTraveledStates - the parent node so it wont travel immediatly backwards

# Returns:
# list of nodes to be randomly selected
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

#print(math.exp(-22/30)) #200 seems highest we can go
#print(math.exp(-10/25)) #200 seems highest we can go
#print(math.exp(-10/50)) #200 seems highest we can go
#print(math.exp(-10/100)) #200 seems highest we can go
#print(math.exp(-10/200)) #200 seems highest we can go
