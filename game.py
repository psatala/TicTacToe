import numpy as np
import random

from .human_player import *

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


    def __init__(self, nRows = 10, nColumns = 10, inALine = 5, height = 700, width = 700, widthOfLine = 5, player1 = 1, player2 = 2):
        #parameter assignment
        self.nRows = nRows
        self.nColumns = nColumns
        self.inALine = inALine
        self.height = height
        self.width = width
        self.widthOfLine = widthOfLine


        #board storing positions of all O's and X's
        self.board = np.zeros([self.nRows + 2, self.nColumns + 2], dtype = int)

    
        #basic inits
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        
        self.tileXSize = width / nColumns
        self.tileYSize = height / nRows
    
        self.gameFinished = False
        self.turn = 1     # 1 -> blue's turn, -1 -> red's turn

        #text inits
        self.font = pygame.font.SysFont("Times New Roman", 100)
        self.text1 = self.font.render("Blue wins!", True, self.BLUE)
        self.text2 = self.font.render("Red wins!", True, self.RED)
        self.text3 = self.font.render("Draw!", True, self.WHITE)


        #player creation
        if player1 == self.PLAYER_HUMAN:
            self.player1 = HumanPlayer(self.tileXSize, self.tileYSize, self.clock)
        #TODO
        #else:
        #    self.player1 = BotPlayer()

        if player2 == self.PLAYER_HUMAN:
            self.player2 = HumanPlayer(self.tileXSize, self.tileYSize, self.clock)
        #TODO
        #else:
        #    self.player2 = BotPlayer()




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
           
            exitClicked, row, column = self.sampleAction()
            if exitClicked:
                self.gameFinished = True
            else:
                self.updateBoard(row, column)
                nMoves += 1

                if self.detectWin(row, column):              #win detected
                    winner = self.turn
                    self.gameFinished = True
                elif nMoves == self.nRows * self.nColumns:   #draw
                    winner = 0
                    self.gameFinished = True

                self.draw(self.BLUE, self.RED, column, row)
            
        self.printResult(winner)


    def sampleAction(self):

        #select player based on turn
        if self.turn == 1:
            currentPlayer = self.player1
        else:
            currentPlayer = self.player2

        #sample move from current player
        if isinstance(currentPlayer, HumanPlayer):
            exitClicked, row, column = currentPlayer.sampleMove(self.board)
        else:
            pass
            #TODO exitClicked, row, column = currentPlayer.sampleMove(self.board)    #bot controller
            #TODO remove if statement

        return exitClicked, row, column


    def updateBoard(self, row, column):
        self.board[row][column] = self.turn


    def detectWin(self, row, column):

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
        pygame.draw.line(self.screen, colour, ((column + 1/8) * self.tileXSize, (row + 1/8) * self.tileYSize), ((column + 7/8) * self.tileXSize, (row + 7/8) * self.tileYSize), self.widthOfLine)
        pygame.draw.line(self.screen, colour, ((column + 7/8) * self.tileXSize, (row + 1/8) * self.tileYSize), ((column + 1/8) * self.tileXSize, (row + 7/8) * self.tileYSize), self.widthOfLine)


    #draw circle
    def drawO(self, colour, column, row):
        pygame.draw.ellipse(self.screen, colour, ((column + 1/8) * self.tileXSize, (row + 1/8) * self.tileYSize, self.tileXSize * 3/4, self.tileYSize * 3/4), self.widthOfLine)


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
        self.screen.blit(text, ((self.width - text.get_width()) / 2, (self.height - text.get_height()) / 2))


def main():
    game = Game(nRows=5, nColumns=5, inALine=4, player2=1)
    game.gameloop()

if __name__ == '__main__':
    main()
