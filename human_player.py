#Name: human_player.py
#Purpose: file containing HumanPlayer class, which handles interaction with the user

import pygame



class HumanPlayer:


    #constructor
    #parameters are: size of tile in x direction, size of tile in y direction, clock used by the game, frames per second
    def __init__(self, tileXSize, tileYSize, clock, fps = 60):
        self.clock = clock
        self.fps = fps
        self.tileXSize = tileXSize
        self.tileYSize = tileYSize



    #function responsible for sampling move from the user
    #parameters are: board containing current state of the game, whose turn is it (necessary only for BotPlayer)
    #return values are: whether or not player has clicked exit, row of sampled move, column of sampled move
    def sampleMove(self, board, turn):
        done = False
        exitClicked = False

        while not done:
            for event in pygame.event.get():


                if event.type == pygame.QUIT:                   #quit
                    done = True
                    exitClicked = True
            

                elif event.type == pygame.MOUSEBUTTONDOWN:      #get mouse input
                    position = pygame.mouse.get_pos()

                    row, column = self.convertPosition(position)    #convert pixel position into row and column
                    if 0 == board[row][column]:                     #check if given tile is empty
                        done = True


            pygame.display.flip()
            self.clock.tick(self.fps)

        return exitClicked, row, column





    ################################################################################################################
    #                                             Auxiliary functions                                              #
    ################################################################################################################


    #convert pixel position into row and column
    #parameters are: pair of integers indicating x and y of the click
    #return values are: row of sampled move, column of sampled move 
    def convertPosition(self, position):
        column = int(position[0] // self.tileXSize) + 1
        row = int(position[1] // self.tileYSize) + 1
        return row, column



    #wait until a key press
    def waitForKeyPress(self):
        done = False

        while not done:

            for event in pygame.event.get():

                if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    done = True

            pygame.display.flip()
            self.clock.tick(self.fps)
