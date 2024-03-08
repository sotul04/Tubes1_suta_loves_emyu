from game.logic.base import BaseLogic
from game.models import Board, GameObject
from ..util import get_direction,position_equals

def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))

def get_direction(current_x, current_y, dest_x, dest_y,teleports,bots):
    delta_x = clamp(dest_x - current_x, -1, 1)
    delta_y = clamp(dest_y - current_y, -1, 1)
    if not(delta_x==0 or delta_y==0):
        for tele in teleports:
            if tele.x == current_x+delta_x and tele.y == current_y and delta_y!=0:
                delta_x = 0
            elif tele.y == current_y+delta_y and tele.x == current_x and delta_x!=0:
                delta_y = 0
    if not(delta_x==0 or delta_y==0):
        for bot in bots:
            if bot.position.x == current_x+delta_x and bot.position.y == current_y and delta_x!=0:
                delta_y = 0
            elif bot.position.y == current_y+delta_y and bot.position.x == current_x and delta_y!=0:
                delta_x = 0
    if not(delta_x==0 or delta_y==0):
        delta_x = 0
    return (delta_x, delta_y)

def distTotal(point1, point2):
    return abs(point1.x-point2.x) + abs(point1.y-point2.y)

def bestRoute(tele,dest,pos):
    bestDist = distTotal(dest,pos)
    bestDest = dest
    dist = distTotal(pos,tele[0])+distTotal(tele[1],dest)
    if dist<bestDist and pos != tele[0]:
        bestDist = dist
        bestDest = tele[0]
    dist = distTotal(pos,tele[1])+distTotal(tele[0],dest)
    if dist<bestDist and pos != tele[1]:
        bestDist = dist
        bestDest = tele[1]
    return (bestDist,bestDest,dest)

def worthDim(teleports,diamonds,pos):
    minDist = 9999
    poin = 1
    for d in diamonds:
        dist = bestRoute(teleports,d.position,pos)[0]
        if(dist/d.properties.points<minDist/poin and dist != 0):
            minDist = dist
            poin = d.properties.points
    return (minDist,poin)

def bestRatio(poin,dimPos, botPos, diamonds, teleports):
    distDim = bestRoute(teleports,dimPos,botPos)[0]
    closest = worthDim(teleports,diamonds,dimPos)
    return min(distDim/poin,(distDim+closest[0])/(poin+closest[1]))

def bestGoal(teleports,diamonds,bots,botPos,currentDim):
    defDest = 0
    defFound = False
    for dims in diamonds:
        if currentDim==4 and dims.properties.points==2:
            continue
        reachable = True
        ourBest = bestRoute(teleports,dims.position,botPos)
        if not defFound:
            defFound = True
            defDest = ourBest
        for enemy in bots:
            enemyBest = bestRoute(teleports,dims.position,enemy.position) 
            if enemyBest[0]<ourBest[0]:
                reachable = False
                break
        if reachable:
            return ourBest
    return defDest

def betweenPoint(point1,point2,point):
    valid_x = (point1.x<=point.x<=point2.x)or(point2.x<=point.x<=point1.x)
    valid_y = (point1.y<=point.y<=point2.y)or(point2.y<=point.y<=point1.y)
    return valid_x and valid_y

def extraMove(base,botPos,dimPos):
    if betweenPoint(base,botPos,dimPos):
        return 0
    temp = 0
    upperY = max(base.y,botPos.y)
    lowerY = min(base.y,botPos.y)
    upperX = max(base.x,botPos.x)
    lowerX = min(base.x,botPos.x)
    if dimPos.y>upperY:
        temp+=dimPos.y-upperY
    elif dimPos.y<lowerY:
        temp+= lowerY-dimPos.y
    if dimPos.x>upperX:
        temp+=dimPos.x-upperX
    elif dimPos.x<lowerX:
        temp+=lowerX-dimPos.x
    return temp    

class KielBot(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position = 9999

    def next_move(self, board_bot: GameObject, board: Board):
        # Setup
        teleports = []
        bots = []
        diamonds = []
        shuffle = 0
        totalDist = 0
        for x in board.game_objects:
            if(x.type == "BotGameObject"):
                bots.append(x)
            elif x.type == "DiamondGameObject":
                diamonds.append(x)
            elif x.type == "TeleportGameObject":
                teleports.append(x.position)
            elif x.type == "DiamondButtonGameObject":
                shuffle = x.position

        props = board_bot.properties
        botPos = board_bot.position
        base = props.base
        toBase = bestRoute(teleports,base,botPos)

        if props.diamonds==5:
            self.goal = toBase
        elif props.diamonds<3 and (props.milliseconds_left//1000>=20):
            diamonds = sorted(diamonds,key= lambda x: bestRatio(x.properties.points,x.position,botPos,diamonds,teleports))
            self.goal = bestGoal(teleports,diamonds,bots,botPos,props.diamonds)
        else:
            diamonds = sorted(diamonds,key= lambda x: (bestRoute(teleports,x.position,botPos)[0]+bestRoute(teleports,x.position,base)[0],bestRoute(teleports,x.position,botPos)[0]))
            temp = bestGoal(teleports,diamonds,bots,botPos,props.diamonds)
            self.goal = temp
            if props.diamonds>=3:
                if not betweenPoint(botPos,toBase[1],temp[1]) and extraMove(toBase[1],botPos,temp[1])>2:
                    self.goal = toBase

        if self.goal[0]>=bestRoute(teleports,shuffle,botPos)[0]+5 and props.diamonds<3:
            self.goal = bestRoute(teleports,shuffle,botPos)

        if betweenPoint(self.goal[1],botPos,toBase[1]) and not(botPos.x==base.x and botPos.y==base.y):
            self.goal = toBase
        
        FromDestToBase = self.goal[0]+bestRoute(teleports,base,self.goal[2])[0]
        if FromDestToBase>(props.milliseconds_left//1000) and props.diamonds>0 and not betweenPoint(toBase[1],botPos,self.goal[1]):
            self.goal = toBase

        delta_x,delta_y = get_direction(
            botPos.x,
            botPos.y,
            self.goal[1].x,
            self.goal[1].y,
            teleports,
            bots,
        )   
        return delta_x, delta_y