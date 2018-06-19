from IPython.display import clear_output
import random

# this function prints grid and all instances of objects
def makeGrid(rows, cols, monsters, player, eggs, door):
    for y in range(rows):
        print(' ---'*cols)
        for x in range(cols):
            monster_egg = False
            for monster in monsters:
                if monster.coords == [x, y] and x == cols - 1 and monster_egg == False:
                    print('| m |', end='')
                    monster_egg = True
                elif monster.coords == [x, y] and monster_egg == False:
                    print('| m ', end='')
                    monster_egg = True

            for egg in eggs:
                if egg.coords == [x, y] and x == cols - 1 and monster_egg == False:
                    print('| e |', end='')
                    monster_egg = True
                elif egg.coords == [x, y] and monster_egg == False:
                    print('| e ', end='')
                    monster_egg = True

            if player.coords == [x, y] and x == cols - 1 and monster_egg == False:
                print('| p |', end='')
            elif player.coords == [x, y] and monster_egg == False:
                print('| p ', end='')

            elif door.coords == [x, y] and x == cols - 1 and monster_egg == False:
                print('| d |', end='')
            elif door.coords == [x, y] and monster_egg == False:
                print('| d ', end='')

            elif x == cols - 1 and monster_egg == False:
                print('|   |', end='')
            elif monster_egg == False:
                print('|   ', end='')
        print()
        if y == rows - 1:
            print(' ---'*cols)

class Monster():
    def __init__(self, coords):
        self.coords = coords

    def initCoords(self, rows, cols):
        self.coords = [random.randint(0, cols-1), random.randint(0, rows-1)]

class Player():
    def __init__(self, coords, eggs_collected=0):
        self.coords = coords
        self.eggs_collected = eggs_collected

    def initCoords(self, rows, cols, monsters):
        # initialize first coords
        self.coords = [random.randint(0, cols-1), random.randint(0, rows-1)]
        # check and loop until coords are not same as monster
        for monster in monsters:
            while monster.coords == self.coords:
                self.coords = [random.randint(0, cols-1), random.randint(0, rows-1)]

    def movePlayer(self):
        ans = input('Where would you like to move? ')
        if ans == 'up':
            self.coords = [self.coords[0], self.coords[1] - 1]
        elif ans == 'down':
            self.coords = [self.coords[0], self.coords[1] + 1]
        elif ans == 'left':
            self.coords = [self.coords[0] - 1, self.coords[1]]
        elif ans == 'right':
            self.coords = [self.coords[0] + 1, self.coords[1]]

    def checkEgg(self, eggs):
        # check and loop until coords are not same as other eggs
        for egg in eggs:
            # clear eggs if collected
            if self.coords == egg.coords:
                self.eggs_collected += 1
                egg.coords = [-1, -1]

class Egg():
    def __init__(self, coords):
        self.coords = coords

    def initCoords(self, rows, cols):
        self.coords = [random.randint(0, cols-1), random.randint(0, rows-1)]

class Door():
    def __init__(self, coords):
        self.coords = coords

    def initCoords(self, rows, cols):
        self.coords = [random.randint(0, cols-1), random.randint(0, rows-1)]

# create a game over function
def game_over(player, monsters, door, num_eggs):
    for monster in monsters:
        if player.coords == monster.coords:
            return 1
    if player.coords == door.coords and num_eggs == player.eggs_collected:
        return 2
    return False

# initialize game over flag
flag = False

level = 0

# main outer initializing loop
while True:
    # size of grid
    rows = 5 + level
    cols = 5 + level
    level += 1

    # objects for game
    monsters = [Monster([0, 0]) for i in range(level)]
    player = Player([1, 1])
    eggs = [Egg([2, 2]) for i in range(level)]
    door = Door([3, 3])

    # randomly initiating coordinates for start
    for monster in monsters:
        monster.initCoords(rows, cols)
    player.initCoords(rows, cols, monsters)
    for egg in eggs:
        egg.initCoords(rows, cols)
    door.initCoords(rows, cols)


    # main game loop
    while True:
        clear_output()
        # show grid
        makeGrid(rows, cols, monsters, player, eggs, door)
        # move player
        player.movePlayer()
        player.checkEgg(eggs)

        # check game_over
        flag = game_over(player, monsters, door, 1)

        if flag == 1:
            print('You were eaten by the monster!')
            level -= 1
            break
        elif flag == 2:
            print('Congrats you beat this level!')
            break

    ans = input('Would you like to play again? ')
    if ans == 'no':
        break
