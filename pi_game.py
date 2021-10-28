from os import system, name as OSname
from getkey import getkey, keys
from cursor import hide
from threading import Thread
from random import randint
from sys import stdout
from time import sleep

# color codes
green = '\033[92m'
red = '\033[91m'
normal = '\033[0m'
speed = .20
food_index = 0
IMG_body = f'{green}π{normal}'
IMG_border = "○"
IMG_empty = " "
length = 20
width = 18
snakeBody = [5, 3]  # start position
foodPos = [5, 7]  # food start position

doc_pi = "3.1415926535897932384626433832795028841971693993751058204944592307816406286208998628034825342117067982148086513282306647093844609550582231725359408128481117450284102701938521105559644622948954930381964428810975665933446128475648233786783165271201909145648566923460348610454326648213393607602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989"

# initializing
hide()
border = 0
points = 1
running = True
order, old = "null", "null"
world = [[IMG_empty]*length for i in range(width)]
x, y = snakeBody[0], snakeBody[1]
world[x][y] = IMG_body
world[foodPos[0]][foodPos[1]] = red + doc_pi[food_index] + normal

# setup border
for i in world:
    world[border][0] = IMG_border
    world[border][-1] = IMG_border
    border += 1
world[0] = IMG_border*len(world[0])
world[-1] = IMG_border*len(world[-1])

# clear screen
def clear(t = 0):
    sleep(t)
    system('cls' if OSname == 'nt' else 'clear')

# special print
def printt(string, delay = 0.005):
    for character in string:
        stdout.write(character)
        stdout.flush()
        sleep(delay)
    print("")

# display map
def display():
    print("\033[H",end="")
    for row in world:
        print(" ".join(map(str,row)))

# generating food at random position
def genfood():
    pos1 = randint(1, width-2)
    pos2 = randint(1, length-2)
    if world[pos1][pos2] == IMG_empty:
        global food_index
        food_index += 1
        world[pos1][pos2] = red + doc_pi[food_index] + normal
    else:
        genfood()

# update game board
def update(nx = 0, ny = 0):
    global x, y, points, running
    x += nx
    y += ny
    snakeBody.append(x)
    snakeBody.append(y)
  
    if world[x][y] == IMG_empty:
        world[snakeBody[0]][snakeBody[1]] = IMG_empty
        del snakeBody[1]
        del snakeBody[0]
    if red in world[x][y]:
        points += 1
        genfood()
    if world[x][y] == IMG_border or world[x][y] == IMG_body:
        running = False
    else:
        try: world[x][y] = IMG_body
        except: running = False

# snake movement
def move():
    global old
    if order == "up":
        update(-1, 0) 
        old = "up"
    if order == "down":
        update(1, 0)
        old = "down"
    if order == "left":
        update(0, -1)
        old = "left"
    if order == "right":
        update(0, 1)
        old = "right"
    display()

# detect key entered by the user
def keypress(key):
    global order
    if key == keys.UP and old != "down" or key == "w" and old != "down": order = "up"
    if key == keys.DOWN and old != "up" or key == "s" and old != "up": order = "down"
    if key == keys.LEFT and old != "right" or key == "a" and old != "right": order = "left"
    if key == keys.RIGHT and old != "left" or key == "d" and old != "left": order = "right"

# keyboard entries
class KeyboardThread(Thread):
    def __init__(self, input_cbk = None, name='keyboard-input-thread'):
        self.input_cbk = input_cbk
        super(KeyboardThread, self).__init__(name=name)
        self.start()

    def run(self):
        while running:
            self.input_cbk(getkey())

# main program
printt("Use W-A-S-D or ←↕→ to move", 0.05)
clear(1)
kthread = KeyboardThread(keypress)
while running:
    move()
    sleep(speed)
print("You died... You Got: ")
print(''.join(doc_pi[:food_index+1]))