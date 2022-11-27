import json
import re

GAMESTART = 'GAME-START'
GAMEEND = 'GAME-END'
class Player:
    def __init__(self, name, x, y, status='Live', equipped=None, attack=1, defense=1):
        self.name = name
        self.x = x
        self.y = y
        self.status = status
        self.equipped = equipped
        self.attack = attack
        self.defense = defense

    def move(self,direction):
        if (not self.status == 'Live'):
            return

        currentPosition = {
            'x': self.x,
            'y': self.y
        }

        if (direction == 'N'):
            self.x = self.x - 1
        elif (direction == 'E'):
            self.y = self.y + 1
        elif (direction == 'S'):
            self.x = self.x + 1
        elif (direction == 'W'):
            self.y = self.y - 1

        # Drown if moved out of bounds
        if (self.x < 0 or self.x > 7 or self.y < 0 or self.y > 7):
            self.drown()
            if (self.equipped):
                self.equipped.moveToShore(currentPosition['x'], currentPosition['y'])
        else:
            if (self.equipped):
                self.equipped.move(self.x, self.y)
        existingItem = checkIfItem(self)
        if (existingItem):
            self.equipItem(existingItem)

        existingPlayer = checkIfFight(self);
        if (existingPlayer):
            self.fight(existingPlayer)

    def fight(self, defendingPlayer):
        if (defendingPlayer.defense < (self.attack + 0.5)):
            defendingPlayer.die()
        else:
            self.die()

    def equipItem(self, item):
        if(not self.equipped):
            self.attack = self.attack + item.attack
            self.defense = self.defense + item.defense
            self.equipped=item
            item.picked=True

    def drown(self):
        self.status = 'Drowned'
        self.attack = 0;
        self.defense = 0;
        if (self.equipped):
            self.equipped.picked = False

    def die(self):
        self.status = 'Drowned'
        self.attack = 0;
        self.defense = 0;
        if(self.equipped):
            self.equipped.picked=False

    def returnPosition(self):
        if(self.status == 'Live'):
            return [self.x,self.y]
        else:
            return 'NULL'

    def returnItem(self):
        if(self.equipped):
            return self.equipped.name
        else:
            return 'null'

class Item:
    def __init__(self, name, x, y, attack, defense, picked=False):
        self.name = name
        self.x = x
        self.y = y
        self.attack = attack
        self.defense = defense
        self.picked = picked

    def move(self,x,y):
        self.x = x;
        self.y = y;

    def moveToShore(self,x,y):
        self.x=x;
        self.y=y;


R = Player('R', 0, 0)
B = Player('B', 7, 0)
G = Player('G', 7, 7)
Y = Player('Y', 0, 7)

Axe = Item('A', 2, 2, 2, 0)
Dagger = Item('D', 2, 5, 1, 0)
Helmet = Item('H', 5, 5, 0, 1)
MagicStaff = Item('M', 5, 2, 1, 1)

players = [R, B, G, Y]
items = [Axe, Dagger, Helmet, MagicStaff]


def renderCell(x, y):
    for player in players:
        if player.x == int(x) and player.y == int(y) and player.status == 'Live':
            return player.name
            break

    for item in items:
        if item.x == int(x) and item.y == int(y) and not item.picked:
            return item.name
            break
    return '_'


def checkIfFight(movedPlayer):
    for player in players:
        if player.name != movedPlayer.name and player.x == movedPlayer.x and player.y == movedPlayer.y:
            return player
            break
    return False;


def checkIfItem(movedPlayer):
    for item in items:
        if not item.picked and item.x == movedPlayer.x and item.y == movedPlayer.y:
            return item
            break
    return False;

def printArena():
    grid = []
    i = int(0)
    for x in range(8):
        for y in range(8):
            grid.append(renderCell(x, y))
        print(grid)
        grid = []

def printResult():
    result = {}
    for p in players:
        result[p.name]=[p.returnPosition(),p.status,p.returnItem(),p.attack,p.defense]

    for i in items:
        result[i.name]=[[i.x,i.y],i.picked]

    with open("final_state.json", "w") as outfile:
        json.dump(result, outfile)
    print(result);

print('Initial Arena')

printArena();
print('-----------')

f = open("moves.txt", "r")
gameStarted = False;

for line in f:
    r = re.compile('.{1}:.{1}')
    if(line.strip()==GAMESTART):
        gameStarted=True;

    if(line.strip()==GAMEEND):
        gameStarted=False;

    if r.match(line) is not None and gameStarted:
        playerName=line.split(':')[0].strip()
        direction = line.split(':')[1].strip()
        for p in players:
            if(p.name == playerName):
                p.move((direction))

print('Final Arena')
printArena();
printResult()
