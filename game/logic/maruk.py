from random import randint
from typing import Optional, List

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction,clamp

def indexValid(x, y: int, width, height):
    return 0 <= x < width and 0 <= y < height

def getStep2Way(currPos, destPos : Position) -> (int,int):
    x_distance = abs(currPos.x - destPos.x)
    y_distance = abs(currPos.y - destPos.y)
    return x_distance, y_distance

class MarukLogic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
    
    def stepDistance(self, object1: GameObject, object2 : GameObject) -> int:
        x_distance = abs(object1.position.x - object2.position.x)
        y_distance = abs(object1.position.y - object2.position.y)
        distance = x_distance+y_distance
        return distance
    
    def getDistance(self, pos1: Position, pos2: Position) -> int:
        x_distance = abs(pos1.x - pos2.x)
        y_distance = abs(pos1.y - pos2.y)
        distance = x_distance+y_distance
        return distance
    
    def getDistanceToBase(self, bot : GameObject) -> int:
        x_distance = abs(bot.properties.base.x - bot.position.x)
        y_distance = abs(bot.properties.base.y - bot.position.y)
        distance = x_distance+y_distance
        return distance

    def evaluateDiamond(self, listDiamond: List[GameObject], board_bot: GameObject, listOfOtherBots : List[GameObject]): # return (List of [diamondPos : Position, distance : int, relativeDistance : int, point : int] : Position)
        evaluation = []
        countDiamonds = len(listDiamond)
        countBots = len(listOfOtherBots)
        for i in range (countDiamonds):
            dist = self.stepDistance(board_bot,listDiamond[i])
            point = listDiamond[i].properties.points
            temp_eval = [listDiamond[i].position,dist,0,point,0]
            for bots in listOfOtherBots:
                temp_eval[4] += self.stepDistance(listDiamond[i],bots)
            for j in range (countDiamonds):
                if (i == j):
                    continue
                temp_eval[2] += self.stepDistance(listDiamond[i],listDiamond[j])
            evaluation.append(temp_eval)
        return evaluation
    
    def getDirection(self, currP : Position, destP : Position, isVertical : int) -> (int, int):
        delta_x = clamp(destP.x - currP.x, -1, 1)
        delta_y = clamp(destP.y - currP.y, -1, 1)
        if delta_x != 0 and delta_y != 0:
            if isVertical == 1:
                delta_x = 0
            else:
                delta_y = 0
        if delta_x == 0 and delta_y == 0:
            delta_x = 1
        return delta_x, delta_y
    
    def isEqualPosition(self, pos1 : Position, pos2 : Position) -> bool :
        return pos1.x == pos2.x and pos1.y == pos2.y
    
    def getDiamondPriorityValue(self, posDiamond : Position, posBase : Position, distance : int, relativeDistance : int, point : int, otherbots : int) -> float:
        value = self.getDistance(posDiamond, posBase)
        value = distance*distance * relativeDistance * value
        value = value/((point+2)*(otherbots+1)**2)
        return value
        
    def checkNextMoveCrash(self, xmove : int, ymove:int, currPos: Position, listObst : List[GameObject]) -> bool :
        nextPos = Position(0, 0)
        nextPos.x = currPos.x+xmove
        nextPos.y = currPos.y+ymove
        found = False
        for i in listObst:
            if self.isEqualPosition(nextPos, i.position):
                print("CRASH!!..",i.type, i.position)
                found = True
                break
        return found

    def getSaveDirection(self,matrix ,currPos : Position, destPos : Position, listObst : List[GameObject], bwitdh : int, bheight: int) -> (int, int):
        xmove, ymove = self.getDirection(currPos, destPos, randint(0,1))
        xstep , ystep = getStep2Way(currPos, destPos)
        if self.checkNextMoveCrash(xmove, ymove, currPos, listObst) :
            print("Obstacle exists")
            print(f"CurrentPos:",currPos)
            print(f"Past move: {xmove}, {ymove}")
            for i in listObst:
                print(i.position, i.type)
            currx = currPos.x
            curry = currPos.y
            destx = destPos.x
            desty = destPos.y
            if (ymove != 0):
                if currx == destx:
                    idx = 0
                    if indexValid(currx-1, curry+ymove, bwitdh, bheight):
                        if matrix[currx-1][curry+ymove]:
                            return 0,ymove
                        idx = -1
                    if indexValid(currx+1, curry+ymove, bwitdh, bheight):
                        if matrix[currx+1][curry+ymove]:
                            return 0,ymove
                        idx = 1
                    if (idx == -1):
                        return -1,0
                    else:
                        return 1,0
                elif currx < destx:
                    if matrix[currx+1][curry+ymove]:
                        return 0,ymove
                    else:
                        return 1,0
                else:
                    if matrix[currx-1][curry+ymove]:
                        return 0,ymove
                    else:
                        return -1,0
            else:
                if curry == desty:
                    idx = 0
                    if indexValid(currx+xmove, curry-1, bwitdh, bheight):
                        if matrix[currx+xmove][curry-1]:
                            return xmove,0
                        idx = -1
                    if indexValid(currx+xmove, curry+1, bwitdh, bheight):
                        if matrix[currx+xmove][curry+1]:
                            return xmove,0
                        idx = 1
                    if (idx == -1):
                        return 0,-1
                    else:
                        return 0,1
                elif curry > desty:
                    if matrix[currx+xmove][curry-1]:
                        return xmove,0
                    else:
                        return 0,-1
                else:
                    if matrix[currx+xmove][curry+1]:
                        return xmove,0
                    else:
                        return 0,1
        return xmove, ymove
    
    def isInAreaMove(self, currPos : Position, destPos : Position, insideArea : Position) -> bool:
        x = (currPos.x >= insideArea.x and destPos.x <= insideArea.x) or (currPos.x <= insideArea.x and destPos.x >= insideArea.x) 
        y = (currPos.y >= insideArea.y and destPos.y <= insideArea.y) or (currPos.y <= insideArea.y and destPos.y >= insideArea.y) 
        if (currPos.x == insideArea.x and currPos.y == insideArea.y):
            return False
        return x and y
    
    def getBotToAttack(self, currPos : Position, listOfOtherBots : [GameObject]):
        countBots = len(listOfOtherBots)
        if countBots != 0:
            currentBot = [listOfOtherBots[0].position,0] 
            for i in range (countBots):
                dist = self.getDistance(currPos,listOfOtherBots[i].position)
                distToBase = self.getDistance(listOfOtherBots[i].position, listOfOtherBots[i].properties.base)
                if dist < distToBase:
                    if listOfOtherBots[i].properties.diamonds > 0:
                        if currentBot[1] < listOfOtherBots[i].properties.diamonds+listOfOtherBots[i].properties.score:
                            currentBot = [listOfOtherBots[i].position, listOfOtherBots[i].properties.diamonds+listOfOtherBots[i].properties.score]
            return currentBot[0]
        return None
    
    def pickDiamond(self, listOfDiamonds : List[GameObject], board_bot : GameObject, listOfOtherBots : List[GameObject]):
        evaluateD = self.evaluateDiamond(listOfDiamonds, board_bot, listOfOtherBots)
        countDiamonds = len(evaluateD)
        if (countDiamonds > 0):
            getDiamond = (evaluateD[0],float("inf"))
            for i in range (countDiamonds):
                valueOfi = self.getDiamondPriorityValue(evaluateD[i][0], board_bot.properties.base, evaluateD[i][1], evaluateD[i][2], evaluateD[i][3], evaluateD[i][4])
                if (valueOfi < getDiamond[1] and evaluateD[i][3]+board_bot.properties.diamonds <= board_bot.properties.inventory_size):
                    getDiamond = (evaluateD[i], valueOfi)
            print(getDiamond)
            diamondPick = getDiamond[0][0]
            return diamondPick
        return None

    def next_move(self, board_bot: GameObject, board: Board):

        listOfDiamonds = []
        listOfOtherBots = []
        listOfTeleport = []

        boardWidth = board.width
        boardHeight = board.height

        print(board_bot.properties.diamonds)
        print(board_bot.properties.score)

        redButton = None
        
        matrix = [[False for j in range(boardHeight)] for i in range(boardWidth)]

        # Selection of Game Objects
        for i in board.game_objects:
            if i.type == "DiamondGameObject":
                listOfDiamonds.append(i)
            elif i.type == "BotGameObject":
                if i.properties.name != board_bot.properties.name:
                    listOfOtherBots.append(i)
            elif i.type == "TeleportGameObject":
                matrix[i.position.x][i.position.y] = True
                listOfTeleport.append(i)
            elif i.type == "DiamondButtonGameObject":
                redButton = i

        # initialize the time limit

        base = board_bot.properties.base
        time_left = int(board_bot.properties.milliseconds_left//1000)

        # Start evaluate the next move

        if time_left <= self.getDistanceToBase(board_bot):

            if board_bot.properties.diamonds != 0:
                if (not self.isEqualPosition(board_bot.position, board_bot.properties.base)):

                    priorityDiamond = self.pickDiamond(listOfDiamonds, board_bot, listOfOtherBots)

                    if priorityDiamond != None and self.isInAreaMove(board_bot.position, board_bot.properties.base, priorityDiamond):
                        return self.getSaveDirection(matrix,board_bot.position, priorityDiamond, listOfTeleport, boardWidth, boardHeight)

                    if self.isInAreaMove(board_bot.position, board_bot.properties.base, redButton.position):
                        return self.getSaveDirection(matrix, board_bot.position, redButton.position, listOfTeleport,boardWidth, boardHeight)
                    
                    return self.getSaveDirection(matrix,board_bot.position,board_bot.properties.base, listOfTeleport,boardWidth, boardHeight)
                
                else:
                    return 1,0
            else:
                priorityDiamond = self.pickDiamond(listOfDiamonds, board_bot, listOfOtherBots)

                if (priorityDiamond != None) and self.isInAreaMove(board_bot.position, board_bot.properties.base, priorityDiamond):
                    return self.getSaveDirection(matrix,board_bot.position, priorityDiamond, listOfTeleport, boardWidth, boardHeight)
                
                else:
                    attackBot = self.getBotToAttack(board_bot.position, listOfOtherBots)

                    if attackBot != None:
                        return self.getSaveDirection(matrix,board_bot.position, attackBot, listOfTeleport,boardWidth, boardHeight)

                    elif  not self.isEqualPosition(board_bot.position, board_bot.properties.base):
                        return self.getSaveDirection(matrix,board_bot.position,board_bot.properties.base, listOfTeleport,boardWidth, boardHeight)

                    else:
                        return 1,0
        else:
            if (board_bot.properties.diamonds < board_bot.properties.inventory_size):
                
                priorityDiamond = self.pickDiamond(listOfDiamonds, board_bot, listOfOtherBots)
                
                if (priorityDiamond != None):
                    print("Priority:",priorityDiamond)
                    diamondPick = priorityDiamond

                    if self.isInAreaMove(board_bot.position, diamondPick, board_bot.properties.base):
                        print("Base first")
                        return self.getSaveDirection(matrix,board_bot.position,board_bot.properties.base, listOfTeleport,boardWidth, boardHeight)

                    elif board_bot.properties.diamonds > 0 and self.getDistance(diamondPick, board_bot.position) >= 2.1*self.getDistance(board_bot.position, board_bot.properties.base):

                        if self.isInAreaMove(board_bot.position, board_bot.properties.base, redButton.position):
                            return self.getSaveDirection(matrix, board_bot.position, redButton.position, listOfTeleport,boardWidth, boardHeight)

                        return self.getSaveDirection(matrix,board_bot.position,board_bot.properties.base, listOfTeleport,boardWidth, boardHeight)

                    print("Current pos:",board_bot.position)

                    return self.getSaveDirection(matrix,board_bot.position,diamondPick, listOfTeleport,boardWidth, boardHeight)
                
                else:
                    return 0,1
            
            else:
                return self.getSaveDirection(matrix,board_bot.position,board_bot.properties.base, listOfTeleport,boardWidth, boardHeight)
                
