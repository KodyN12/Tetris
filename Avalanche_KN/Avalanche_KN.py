import pygame
import time
from Shape_KN import Shape  # Import the shape class
from GameBoard_KN import GameBoard  # Import the GameBoard Class
from GameBoard_KN import gameboardheight  # Import the GameBoard Height

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
TURQUOISE = (0, 206, 209)
DARKPURPLE = (66, 30, 66)

# ------INITIALIZATION------
if __name__ == "__main__":
    # Initialize the game engine
    pygame.init()
    # Engine Used for Sounds
    pygame.mixer.init()

    # Setting screen size and other variables
    size = (800, 600)
    screen = pygame.display.set_mode(size)
    xPos = 125
    yPos = 110
    blockSize = 25
    pygame.display.set_caption("Avalanche")
    myFont = pygame.font.Font('freesansbold.ttf', 30)
    HSfont = pygame.font.Font('freesansbold.ttf', 20)
    shape = Shape()  # Use constructor function to create Block object
    nextShape = Shape()  # Construct a new shape to display as the upcoming shape
    gameboard = GameBoard(WHITE, shape.blockList[0].size)  # Use constructor function to create GameBoard object
    name = ""  # Used for storing the players name, by default empty
    delay = 0
    slowtimedelay = 0
    normal = True
    hardcore = False
    print("started with hardcore = ", hardcore, "and normal = ", normal)

    # ---- Play Music ----
    #pygame.mixer.music.load('AvalancheBGM.mp3')
    #pygame.mixer.music.load('SteamGardens.mp3')
    #pygame.mixer.music.play(-1)  # We use -1 to make it a loop

    # ------ Reading and Displaying Files ------
    nameList = [0 for y in range(5)]
    scoreList = [0 for y in range(5)]
    HSfile = open("HighScores.txt", "r")  # Open the text file Highscores

    for i in range(5):
        # Reads in the file without the blank line
        nameList[i] = HSfile.readline().rstrip('\n')

    for i in range(5):
        # Reads in the score without the blank line
        scoreList[i] = HSfile.readline().rstrip('\n')

    # Loop control variable that will become true and close the program when we click the x button
    HSfile.close()  # Closes the Highscores.txt file

    # This will loop until the user clicks the close button
    done = False

    # Whether the game has started or not
    started = False

def keyCheck():
    if event.key == pygame.K_LEFT:
        shape.moveLeft()
    elif event.key == pygame.K_RIGHT:
        shape.moveRight()
    elif event.key == pygame.K_d:
        shape.moveDown()
    elif event.key == pygame.K_UP:
        shape.rotateCW()
    elif event.key == pygame.K_DOWN:
        shape.rotateCCW()
    elif event.key == pygame.K_SPACE:
        gameboard.score += (gameboardheight - shape.blockList[0].gridYpos)
        shape.drop()
    elif event.key == pygame.K_t and gameboard.numslowtime > 0:
        gameboard.numslowtime -= 1  # Subtract 1 from the slow-time powerup
        gameboard.slowtimeon = True  # Set slow-time powerup to active
    elif event.key == pygame.K_s and gameboard.swapshape > 0:
        gameboard.swapshape -= 1
        gameboard.swapshapeon = True


def drawScreen():
    screen.fill(BLACK)
    shape.draw(screen)
    nextShape.drawnextshape(screen)
    gameboard.draw(screen)

    # ------ Score UI ------
    scoretext = myFont.render("Score: " + str(gameboard.score), 1, WHITE)
    screen.blit(scoretext, (375, 300))
    # ------ Line UI ------
    linestext = myFont.render("Lines: " + str(gameboard.numLines), 1, WHITE)
    screen.blit(linestext, (375, 350))

    # ------ Level UI ------
    leveltext = myFont.render("Level: " + str(gameboard.level), 1, WHITE)
    screen.blit(leveltext, (375, 400))

    if normal == True:
        # ------ Powerup UI ------
        poweruptext = myFont.render("Powerups: ", 1, WHITE)
        screen.blit(poweruptext, (50,525))

        # ------ Display the number of slow time powerups available ------
        numslowtimetext = myFont.render(" x" + str(gameboard.numslowtime), 1, WHITE)
        screen.blit(numslowtimetext, (310, 525))
        slowtime_image = pygame.image.load("clock.png")  # Loads the clock image
        screen.blit(slowtime_image, (250,515))

    # ------ Display the number of swap shape powerups available ------
        swapshapetext = myFont.render(" x" + str(gameboard.swapshape), 1, WHITE)
        screen.blit(swapshapetext, (450, 525))
        swapshape_image = pygame.image.load("swap.png")  # Loads the swapshape image
        screen.blit(swapshape_image, (375, 515))

        # ------ Next Shape UI ------
        nextshapetext = myFont.render("Next Shape: ", 1, WHITE)
        screen.blit(nextshapetext, (375, 50))
        pygame.draw.rect(screen, WHITE, [400, 100, 6 * shape.blockList[0].size, 6 * shape.blockList[0].size], 1)
        screen.blit(nextshapetext, (375, 50))

    # ------ Display High Scores ------
    highscoretext = myFont.render("High Scores", 1, WHITE)
    screen.blit(highscoretext, (575, 50))
    pygame.draw.rect(screen, WHITE, [575,100,200,400], 1)

    for i in range(5):
        hsnametext = HSfont.render(str(nameList[i]), 1, WHITE)
        hsscoretext = HSfont.render(str(scoreList[i]), 1, WHITE)
        screen.blit(hsnametext, (580, i * 25 + 125))
        screen.blit(hsscoretext, (700, i * 25 + 125))

    # ----- Display Player Name ------
    playernametext = myFont.render("Player: " + name, 1, WHITE)
    screen.blit(playernametext, (550,525))

    pygame.display.flip()  # Updates the screen with everything we've drawn (Must be at the bottom)

def checkHighScores():
    newHighScore = False
    tempnamelist = [0 for y in range(5)]
    tempscorelist = [0 for y in range(5)]
    for i in range(5):
        if gameboard.score > int(scoreList[i]) and newHighScore == False:
            newHighScore = True
            tempscorelist[i] = gameboard.score
            tempnamelist[i] = name
        elif newHighScore == True:
            tempscorelist[i] = scoreList[i-1]
            tempnamelist[i] = nameList[i-1]
        else:
            tempscorelist[i] = scoreList[i]
            tempnamelist[i] = nameList[i]

    for i in range(5):
        scoreList[i] = tempscorelist[i]
        nameList[i] = tempnamelist[i]

    HSfile = open("HighScores.txt", "w")
    for i in range(5):
        HSfile.write(nameList[i] + "\r\n")

    for i in range(5):
        HSfile.write(str(scoreList[i]) + "\r\n")
    HSfile.close()



# ---- Title Screen ----
while not started:
    titlescreen = pygame.image.load("Backdrop.png")
    enterednametext = myFont.render("Please type your name in:", 1, WHITE)
    nametext = myFont.render(name,1,WHITE)
    screen.blit(enterednametext, (200,200))
    screen.blit(nametext,(300,250))
    pygame.display.flip()
    screen.blit(titlescreen, (0,0))
    # ---- Main Event Loop ----

    # pygame.event.get(): --> Computer is 'listening' for an event
    # Events could be Keypressed, Mouseclicked, etc.
    for event in pygame.event.get():

        # If the event type is QUIT
        if event.type == pygame.QUIT:
            done = True
            started = True

        # If the event type is when the user presses a key on the keyboard
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_1:
                hardcore = True
                normal = False
                print(hardcore, normal)

            # If the ASCII numbers are between 33 and 126 and the length of the name is less than 10
            if event.key >= 58 and event.key <= 126 and len(name) < 10:
                name = name + chr(event.key)  # Adds another character to the name

            if event.key == pygame.K_BACKSPACE:
                name = name[:-1]  # Splice the array

            if event.key == pygame.K_RETURN:
                if name == "":  # If the name is empty
                    name = "Player1"
                started = True  # Start the game

            if event.key == pygame.K_RETURN:
                started = True


# ----------- Main Program Loop ------------
while not done:
    # -------- Main Event Loop --------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            keyCheck()

    delay += 1
    if delay >= 10:
        shape.falling()
        delay = 0

    # If our slow-time powerup is active, count until 50 ticks, then turn off slow-time
    if gameboard.slowtimeon:
        slowtimedelay += 1
        if slowtimedelay > 50:
            slowtimedelay = 0
            gameboard.slowtimeon = False

    # This swaps the shape if we have the powerup and it's being used
    if gameboard.swapshapeon:
        shape = nextShape
        nextShape = Shape()
        gameboard.swapshapeon = False

    # If our shape has finished moving, draw a new shape
    if not shape.active:
        gameboard.clearFullRows()
        shape = nextShape  # Create a new shape object
        nextShape = Shape()

    # Checks to see if we lost or not and then resets the gameboard if we have\
    if gameboard.checkloss():
        checkHighScores()
        gameboard = GameBoard(WHITE, shape.blockList[0].size)
        delay = 0
        slowtimedelay = 0
        shape = Shape()
        nextShape = Shape()

    drawScreen()

    if 0.115 - gameboard.level * 0.015 >= 0:
        # Puts in a one tenth of a second delay, giving the user time to react
        time.sleep(0.115 - gameboard.level * 0.015 + gameboard.slowtimeon * 0.1)
