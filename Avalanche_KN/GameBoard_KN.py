import pygame

gameboardwidth = 12 # The number of blocksize width the gameboard is
gameboardheight = 20 # The number of blocksize height the gameboard is
# Checks to see if the spot is occupied by a block or not
activeBoardSpot = [[0 for y in range(gameboardheight)] for x in range(gameboardwidth)]
# What colour to draw the block on the grid
activeBoardColor = [[0 for y in range(gameboardheight)] for x in range(gameboardwidth)]

BLACK = (0,0,0)  # Colour Black
pygame.init()
linesound = pygame.mixer.Sound('clearline.wav')


# Gameboard class needs a colour, multiplier
class GameBoard():
    # Gameboard Constructor: Our game board's width and height are multiplier's of the block's size
    def __init__(self, colour, blocksize):
        self.bordercolour = colour
        self.multiplier = blocksize
        self.score = 0
        self.numLines = 0
        self.tempLevelTracker = 0
        self.level = 1
        self.numslowtime = 0
        self.slowtimeon = False  # Checks if slow-time powerup is active
        self.swapshape = 0
        self.swapshapeon = False  # Chekcs if swap-shape powerup is active

        # Make every square in the grid inactive with the colour black
        for i in range(gameboardwidth):
            for j in range(gameboardheight):
                activeBoardSpot[i][j] = False  # Initialize it to inactive
                activeBoardColor[i][j] = (0,0,0)  # Initialize it to black

    # Draw a game board rectangle on the screen
    def draw(self, screen):
        pygame.draw.rect(screen, self.bordercolour, [0, 0, gameboardwidth * self.multiplier, gameboardheight * self.multiplier], 1)

        for i in range(gameboardwidth):
            for j in range(gameboardheight):
                if activeBoardSpot[i][j]:
                    pygame.draw.rect(screen, activeBoardColor[i][j], [i * self.multiplier, j * self.multiplier, self.multiplier -1, self.multiplier -1], 0)

    # Check to see if we have lost or not
    def checkloss(self):
        for i in range(gameboardwidth):
            if activeBoardSpot[i][0]:
                return True
        return False

    # Checks to see if we completed a line
    def isCompleteLine(self, rowNum):
        for i in range (gameboardwidth):
            if activeBoardSpot[i][rowNum] == False:
                return False
        return True

    # Clears out the completed row
    def clearFullRows(self):
        for j in range(gameboardheight):
            if self.isCompleteLine(j):  # If it's a complete line, shift it accordingly
                linesound.play()  # Plays the clearline sound effect
                self.score += 100
                self.numLines += 1
                self.tempLevelTracker += 1
                # If we clear 10 lines, increase the score
                if self.tempLevelTracker == 10:
                    self.level += 1
                    #if self.level % 2 != 0:
                    self.numslowtime += 1  # Add a slow-time powerup
                    #elif self.level % 2 == 0:
                    self.swapshape += 1  # Add a swap-shape powerup
                    self.tempLevelTracker = 0
                # 1st Param: Used to specify which position to start in
                # 2nd Param: Specifies which position to stop in
                # 3rd Param: Specifies the incrementation, meaning how much you count up or down
                for c in range(j, 1, -1):  # From top to bottom of the gameboard
                    # Shift leftover blocks down
                    for i in range(gameboardwidth):
                        activeBoardSpot[i][c] = activeBoardSpot[i][c-1]
                        activeBoardColor[i][c] = activeBoardColor[i][c - 1]

                    for r in range(gameboardwidth):
                        activeBoardSpot[r][0] = False
                        activeBoardColor[r][0] = BLACK
