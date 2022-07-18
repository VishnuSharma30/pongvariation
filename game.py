# 8. Write a game, in PyGame, where the player character needs to travel between
# two goals as many times as possible without getting hit. The goals are on the
# opposite sides of the screen. Place obstacles that the player cannot move
# through and that the enemies bounce off. At the start of the game, new
# enemies are spawned at a random location moving at a random velocity once
# per second. During game play, the enemies are spawned with increasing
# frequency. Best mark for game I enjoy the most.

# import pygame and pygame zero to get GUI
import pygame
import pgzrun
# import randint to get random starting pos of ball
from random import randint

# set the width and height of the game window
WIDTH = 1000
HEIGHT = 1000

# set the fps that the game will run in - locked at 30fps to keep the one second timings
fps = 30
# allows counting of time using fps
fpsClock = pygame.time.Clock()
# counts number of frames it has been
count = int()
# checks if the player has gained a point to prevent multiple scores counting at once
scoreStatus = True
# True means leave from left, False means leave from right
whichGoal = True

# variables to help check if it is possible to level up
condition = 1
conditionCheck = False

# the score is the number of times the player reaches the goal
s1 = 0

# keeps track if game is over, default False since game isn't over
gameover = False

# create the two goals that the player has to reach
# goal1 is the left goal (goal1.pos is the location) and same goes with goal2 and zone and player and obstacle
goal1 = Actor("paddle")
goal1.pos = 10, 500
goal2 = Actor("paddle")
goal2.pos = 990, 500
player = Actor("player")
player.pos = 36, 500
zone1 = Actor("mid")
zone1.pos = 60, 500
zone2 = Actor("mid")
zone2.pos = 940, 500
obstacle = Actor("obstacle")
obstacle.pos = 250, 500

# keeps track of the obstacles' locations
obLoc = []

# keeps track of how long it has been since the game began
time = int()

# changing this value changes the frequency of enemy spawn
threshold = 29

# keeps track of each enemy sprite
enemies = []
# keeps track of the slope (angle of direction) of the different enemies
directions = []
# keeps track of the direction of the different enemies
leftright = []

# keeps track of multiple obstacles
obstacles = []

# makes new enemies when requested; requires positions x, y and slope d, direction l
def newEnemy(x, y, d, l):
    # creates enemy with enemy image file
    enemy = Actor("enemy")
    # sets the location of enemy spawn
    enemy.pos = x, y
    # keeps track of enemy sprite, direction (speed & path)
    enemies.append(enemy)
    directions.append(d)
    leftright.append(l)

# makes new enemies when requested; requires positions x, y and slope d, direction l
def newObstacle(x, y):
    # creates obstacle with obstacle image file
    obstacle = Actor("obstacle")
    # sets the location of obstacle spawn
    obstacle.pos = x, y
    # keeps track of obstacle sprite, location
    obstacles.append(obstacle)
    obLoc.append(obstacle.pos)

# create the first enemy, random in direction and slope
newEnemy(randint(73, 900), randint(35, 900), randint(0, 3), randint(0, 2))

# create the first obstacle, random in location
newObstacle(randint(73, 900), randint(35, 900))

# the game "engine" - a loop of sorts that runs over and over
def update():
    # uses some global variables (the scores, the enemies, the directions, the slopes, if game over or not)
    global s1, enemies, directions, leftright, gameover, count, scoreStatus, obstacles, whichGoal, obLoc, time, threshold
    # sets the direction the character is moving for later
    left = False
    right = False
    up = False
    down = False
    # check the type of input
    # up down left right can move player in any direction
    if keyboard.left:
        # if moving right, changes the character's x coordinate by -6
        player.x -= 6
        # if character's location is less than 35, prevents character from moving by adding 6 back
        if player.x < 35:
            player.x += 6
        # tells the program that the character has moved left
        left = True
    elif keyboard.right:
        # if moving left, changes the character's x coordinate by +6
        player.x += 6
        # if character's location is higher than 965, prevents character from moving by removing 6
        if player.x > 965:
            player.x -= 6
        # tells the program that the character has moved right
        right = True
    elif keyboard.up:
        # if moving up, decreases character's y coordinate by 6
        player.y -= 6
        # if player's location is less than 37, removes movement
        if player.y < 37:
            player.y += 6
        # tells the program that the character has moved up
        up = True
    elif keyboard.down:
        # if moving down, increases character's y coordinate by 6
        player.y += 6
        # if player's location is greater than 963, removes movenet
        if player.y > 963:
            player.y -= 6
        # tells the program that the character has moved down
        down = True
    # checks the movement of the enemies
    for i in range(len(enemies)):
        # if the enemy is moving to the left, subtract 1 from x to move it left and subtract the slope to move y
        if leftright[i]:
            enemies[i].x -= 1
            enemies[i].y -= directions[i]
        # if enemy is moving to right, add 1 to x to move it right and add the slope to move y
        else:
            enemies[i].x += 1
            enemies[i].y += directions[i]
        # if the enemy hits the ceiling
        if enemies[i].y <= 18:
            # reverse the slope so it falls down
            directions[i] = -directions[i]
        # if the enemy hits the floor
        elif enemies[i].y >= 982:
            # reverse the slope so it goes up
            directions[i] = -directions[i]
        # if the enemy hits the...
        if enemies[i].x <= 82:
            # reverse the slope of the original enemy so it reflects
            directions[i] = -directions[i]
            # reverses direction of the original enemy
            leftright[i] = 0
        elif enemies[i].x >= 921:
            # reverse the slope of the original enemy so it reflects
            directions[i] = -directions[i]
            # reverses direction of the original enemy
            leftright[i] = 1
        # if the player comes in contact with any enenmy
        if (enemies[i].x -17) < player.x < (enemies[i].x + 17):
            if (enemies[i].y -18) < player.y < (enemies[i].y + 18):
                # gameover
                gameover = True
        # for every obstacle
        for j in obLoc:
            # if enemies come in contact with the obstacle
            if (j[0] + 31) >= enemies[i].x >= (j[0] - 31):
                if (j[1] + 54) >= enemies[i].y >= (j[1] - 54):
                    # reverse the slope of the original enemy so it reflects
                    directions[i] = -directions[i]
                    # reverses direction of the original enemy
                    if leftright[i] == 0:
                        leftright[i] = 1
                    else:
                        leftright[i] = 0
            # another way to check if enemies come in contact with obstacle
            elif (j[1] + 54) >= enemies[i].y >= (j[1] - 54):
                if (j[0] + 31) >= enemies[i].x >= (j[0] - 31):
                    # reverse the slope of the original enemy so it reflects
                    directions[i] = -directions[i]
            # if the player comes in contact with obstacle
            if (j[0] - 31) <= player.x <= (j[0] + 31):
                if (j[1] + 54) >= player.y >= (j[1] - 54):
                    # if the player's movement was left, right, up, or down cancels the player's movement
                    if left:
                        player.x += 6
                    elif right:
                        player.x -= 6
                    elif up:
                        player.y += 6
                    elif down:
                        player.y -= 6
    # if player has gained a point, set it to False after it leaves the score zone
    if scoreStatus:
        if 40 < player.x < 950:
            scoreStatus = False
        elif 950 > player.x > 40:
            scoreStatus = False
    # otherwise, give the player a point, depending on location
    else:
        # checks which goal the player is at
        if player.x == 36:
            # checks which goal the player gained a point from before
            if not whichGoal:
                # increases score by 1
                s1 += 1
                # checks the number of obstacles on the screen
                if len(obstacles) == 5:
                    # set length as number of obstacles
                    length = len(obstacles)
                    # gets rid of all obstacles
                    obstacles = []
                    # creates new obstacles for the return journey
                    for lengths in range(length):
                        newObstacle(randint(73, 900), randint(35, 900))
                else:
                    length = len(obstacles)
                    obstacles = []
                    for lengths in range(length + 1):
                        newObstacle(randint(73, 900), randint(35, 900))
                # allows game to know that player scored
                scoreStatus = True
                # allows game to know which goal the player scored in
                whichGoal = True
                # clears out location of obstacles
                obLoc = []
                # adds obstacle location to obLoc again
                for ob in obstacles:
                    obLoc.append(ob.pos)
        elif player.x == 960:
            # checks which goal the player gained a point from before
            if whichGoal:
                # increases score by 1
                s1 += 1
                # checks the number of obstacles on the screen
                if len(obstacles) == 5:
                    # set length as number of obstacles
                    length = len(obstacles)
                    # gets rid of all obstacles
                    obstacles = []
                    # creates new obstacles for the return journey
                    for lengths in range(length):
                        newObstacle(randint(73, 900), randint(35, 900))
                else:
                    length = len(obstacles)
                    obstacles = []
                    for lengths in range(length + 1):
                        newObstacle(randint(73, 900), randint(35, 900))
                # allows game to know that player scored
                scoreStatus = True
                # allows game to know which goal the player scored in
                whichGoal = False
                # clears out location of obstacles
                obLoc = []
                # adds obstacle location to obLoc again
                for ob in obstacles:
                    obLoc.append(ob.pos)
    # checks number of frames since last
    count += 1
    # checks total time elapsed
    time += 1
    # if 5 seconds (30 frames per second times 5) has passed, decrease time needed until new enemy can spawn
    if time % 150 == 0:
        threshold -= 1
    # if the time since last enemy has reached the threshold,
    if count == threshold:
        # create new enemy,
        newEnemy(randint(73, 900), randint(35, 900), randint(0, 3), randint(0, 2))
        # and reset timer to zero
        count = 0
    # set the framerate of the game
    fpsClock.tick(fps)

# makes the screen and allows user to play the game
def draw():
    # sets out some global variables to use
    global condition, conditionCheck
    # sets background image to bg
    screen.blit("bg", (0,0))
    # if the game is over
    if gameover:
        screen.fill("black")
        screen.draw.text("GAME OVER", center=(500, 430), fontsize=70)
        screen.draw.text("Final Score - {0}".format(str(s1)), center=(500, 550), fontsize=40)
    # if game not over
    else:
        # displays the current score of the game
        screen.draw.text(str(s1), (450, 10))
        # displays current "level"
        screen.draw.text("Level {}".format(condition), (550, 10))
        # if the score reaches a multiple of 5 and eligible to level up
        if s1 % 5 == 0 and not conditionCheck:
            # increases level
            condition = int(s1/5) + 1
            # disallow level up
            conditionCheck = True
        # allow level up again
        elif s1 % 5 != 0:
            conditionCheck = False
        # draw in the two goals and zones onto the screen
        goal1.draw()
        goal2.draw()
        zone1.draw()
        zone2.draw()
        # draw in the player
        player.draw()
        # draw each enemy
        for enemy in enemies:
            enemy.draw()
        # draw each obstacle
        for obstacle in obstacles:
            obstacle.draw()

# runs the game
pgzrun.go()