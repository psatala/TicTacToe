import numpy as np
import pygame
import random

class Game:

    #constants
    PLAYER_HUMAN = 1
    PLAYER_BOT = 2
    
    #colour constants
    WHITE = (255, 255, 255)
    GREY = (128, 128, 128)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)

    #general parameters
    nRows = 10
    nColumns = 10
    inALine = 5
    player1 = PLAYER_HUMAN
    player2 = PLAYER_BOT

    #graphical parameters
    height = 700
    width = 700
    widthOfLine = 5



    def __init__(self, nRows, nColumns, inALine, height, width, widthOfLine, player1, player2):
        #parameter assignment
        self.nRows = nRows
        self.nColumns = nColumns
        self.inALine = inALine
        self.height = height
        self.width = width
        self.widthOfLine = widthOfLine
        self.player1 = player1
        self.player2 = player2

        #board storing positions of all O's and X's
        self.board = np.zeros([self.nRows + 2, self.nColumns + 2], dtype = int)

    
        #basic inits
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        
        self.tileXsize = width / nColumns
        self.tileYsize = height / nRows
    
        self.gameFinished = False
        self.turn = 1     # 1 -> blue's turn, -1 -> red's turn

        #text inits
        self.font = pygame.font.SysFont("Times New Roman", 100)
        self.text1 = self.font.render("Blue wins!", True, self.BLUE)
        self.text2 = self.font.render("Red wins!", True, self.RED)
        self.text3 = self.font.render("Draw!", True, self.WHITE)


    ################################################################################################################
    #                                             Gameplay functions                                               #
    ################################################################################################################


    def gameloop(self):

        #setup
        winner = 0
        nMoves = 0
        self.drawBox(self.BLUE)
        self.drawGrid(self.GREY)
        
        #main loop
        while not self.gameFinished:
           
            column, row = self.sampleAction()
            self.updateBoard(column, row)
            nMoves += 1

            if self.detectWin(column, row):              #win detected
                winner = self.turn
                self.gameFinished = True
            elif nMoves == self.nRows * self.nColumns:   #draw
                winner = 0
                self.gameFinished = True

            self.draw(self.BLUE, self.RED, column, row)
            


    def sampleAction(self):

        #select player based on turn
        if self.turn == 1:
            currentPlayer = self.player1
        else:
            currentPlayer = self.player2

        #sample move from current player
        if currentPlayer == self.PLAYER_HUMAN:
            pass
            #TODO: column, row = sampleHuman(self.board)  #human controller
        else:
            pass
            #TODO: column, row = sampleBot(self.board)    #bot controller

        return column, row


    def updateBoard(self, column, row):
        self.board[row][column] = self.turn


    def detectWin(self, column, row):

        moveX = [1, 0, 1, 1]   #move in x direction
        moveY = [0, 1, 1, -1]  #move in y direction

        for i in range(4):
            sum = 1
            for j in range(1, self.inALine):
                if(self.board[row + j * moveY[i]][column + j * moveX[i]] != self.turn):
                    break
                sum += 1
            for j in range(1, self.inALine):
                if(self.board[row - j * moveY[i]][column - j * moveX[i]] != self.turn):
                    break
                sum += 1
            if sum >= self.inALine:
                return True
    
        #no winner yet
        return False


    ################################################################################################################
    #                                             Drawing functions                                                #
    ################################################################################################################


    #general draw function responsible for drawing O or X and a new box
    def draw(self, colour, otherColour, column, row):
        if self.turn == 1:
            self.drawO(colour, column - 1, row - 1)
            self.drawBox(otherColour)
        else:
            self.drawX(otherColour, column - 1, row - 1)
            self.drawBox(colour)


    #draw cross
    def drawX(self, colour, column, row):
        pygame.draw.line(self.screen, colour, ((column + 1/8) * self.tileXsize, (row + 1/8) * self.tileYsize), ((column + 7/8) * self.tileXsize, (row + 7/8) * self.tileYsize), self.widthOfLine)
        pygame.draw.line(self.screen, colour, ((column + 7/8) * self.tileXsize, (row + 1/8) * self.tileYsize), ((column + 1/8) * self.tileXsize, (row + 7/8) * self.tileYsize), self.widthOfLine)


    #draw circle
    def drawO(self, colour, column, row):
        pygame.draw.ellipse(self.screen, colour, ((column + 1/8) * self.tileXsize, (row + 1/8) * self.tileYsize, self.tileXsize * 3/4, self.tileYsize * 3/4), self.widthOfLine)


    #draw grid
    def drawGrid(self, colour):
        for i in range(1, self.nColumns):
            pygame.draw.line(self.screen, colour, (i * self.width / self.nColumns, 0), (i * self.width / self.nColumns, self.height))
        for i in range(1, self.nRows):
            pygame.draw.line(self.screen, colour, (0, i * self.height / self.nRows), (self.width, i * self.height / self.nRows))


    #draw box
    def drawBox(self, colour):
        pygame.draw.rect(self.screen, colour, (0, 0, self.width, self.height), self.widthOfLine)


    #print result
    def printResult(self, winner):
        if winner == 1:       #blue won
            text = self.text1
        elif winner == -1:    #red won
            text = self.text2
        else:                 #draw
            text = self.text3

        #print appropriate text
        screen.blit(text, ((width - text.get_width()) / 2, (height - text.get_height()) / 2))



def main():
    
    
    
    #main loop
    count = 0
    while not done:
        for event in pygame.event.get():


            if event.type == pygame.QUIT:                   #quit
                #save(networks, noColumns, noRows, index, populationSize, fileName)
                done = True
            

            elif event.type == pygame.MOUSEBUTTONDOWN:      #get mouse input
                pos = pygame.mouse.get_pos()
        pygame.display.flip()
        clock.tick(60)



if __name__ == '__main__':
    main()
