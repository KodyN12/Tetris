import pygame

class Block():
    #Constructor
    def __init__(self, colour, gridXpos, gridYpos):
        self.colour = colour
        self.gridXpos = int(gridXpos) # The x position according to the game board grid
        self.gridYpos = int(gridYpos) # The y position according to the game board grid
        self.size = 25

    def draw(self, screen):
        #Draw a red rectangle on the screen
        pygame.draw.rect(screen, self.colour, [self.gridXpos * self.size, self.gridYpos * self.size, self.size-1, self.size-1], 0)
