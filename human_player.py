import pygame

class HumanPlayer:


    def __init__(self, tileXSize, tileYSize, clock, fps = 60):
        self.clock = clock
        self.fps = fps
        self.tileXSize = tileXSize
        self.tileYSize = tileYSize


    def sampleMove(self, board):
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


    #convert pixel position into row and column
    def convertPosition(self, position):
        column = (position[0] // self.tileXSize) + 1
        row = (position[1] // self.tileYSize) + 1
        return row, column