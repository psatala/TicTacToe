import numpy as np
import pygame
import random

class Game:
    
    #general parameters
    nRows = 10
    nColumns = 10
    inALine = 5

    #graphical parameters
    height = 700
    width = 700
    widthOfLine = 5

    #player constants
    PLAYER_HUMAN = 1
    PLAYER_BOT = 2


    def __init__(self, nRows, nColumns, inALine, height, width, widthOfLine):
        #parameter assignment
        self.nRows = nRows
        self.nColumns = nColumns
        self.inALine = inALine
        self.height = height
        self.width = width
        self.widthOfLine = widthOfLine
        

        #board storing positions of all O's and X's
        self.board = np.zeros([self.nRows + 2, self.nColumns + 2], dtype = int)

        #colours
        self.white = (255, 255, 255)
        self.grey = (128, 128, 128)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)
        self.colours = (self.blue, self.red)
    
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
        self.text1 = self.font.render("Blue wins!", True, self.blue)
        self.text2 = self.font.render("Red wins!", True, self.red)
        self.text3 = self.font.render("Draw!", True, self.white)
        self.text = [self.text1, self.text2, self.text3]


    ################################################################################################################
    #                                             Gameplay functions                                               #
    ################################################################################################################
    '''
    def Gameloop
    def SampleAction(player)
    def updateBoard
    '''

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
    def draw(self, colour, otherColour, column, row, turn):
        if turn == 0:
            self.drawO(colour, column - 1, row - 1)
        else:
            self.drawX(colour, column - 1, row - 1)
        self.drawBox(otherColour)


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





def main():
    
    
    
    
    #gameplay inits
    pos = (0, 0)
    skillIndex = 0
    isBlueTurn = 1
    stillPlaying = True
    board = [[0 for x in range(noColumns + 2)] for y in range(noRows + 2)]
    drawGrid(screen, grey, height, width, noColumns, noRows)
    drawBox(screen, blue, height, width, widthOfLine)

    #read data from file
    #read(networks, noColumns, noRows, index, populationSize, fileName)

    #player inits
    players = (1, 0)   #CHANGE HERE!!!
    if not players[0] and not players[1]:
        for i in  range(numberOfRounds):
            #tuple = playOneRound(networks, populationSize, numberOfBestIndividuals, rateOfMutation, board, noColumns, noRows, inALine, screen, colours, height, width, tileXsize, tileYsize, widthOfLine, grey, text, i + 1, skillIndex, index)
            #networks = tuple[1]
            #index = tuple[2]
            #if not tuple[0]:
            #    break
            #skillIndex = check(networks[0], board, noColumns, noRows, inALine, screen, colours, height, width, tileXsize, tileYsize, widthOfLine, grey, index)
        #save(networks, noColumns, noRows, index, populationSize, fileName)
            pass
        done = True
        stillPlaying = False

    #main loop
    count = 0
    while not done:
        for event in pygame.event.get():


            if event.type == pygame.QUIT:                   #quit
                #save(networks, noColumns, noRows, index, populationSize, fileName)
                done = True
            

            elif event.type == pygame.MOUSEBUTTONDOWN:      #get mouse input
                pos = pygame.mouse.get_pos()
                x = int(pos[0] / tileXsize) + 1
                y = int(pos[1] / tileYsize) + 1
                if not board[y][x] and stillPlaying:

                    #if isBlueTurn:                          #blue's turn
                    drawO(screen, blue, tileXsize, tileYsize, x - 1, y - 1, widthOfLine)
                    drawBox(screen, red, height, width, widthOfLine)
                    board[y][x] = 1
                    count += 1
                    '''if winDetection(board, x, y, inALine, 1):
                        screen.blit(text1, ((width - text1.get_width()) / 2, (height - text1.get_height()) / 2))
                        stillPlaying = False
                    elif count == noColumns * noRows:
                        screen.blit(text3, ((width - text3.get_width()) / 2, (height - text3.get_height()) / 2))
                        stillPlaying = False'''

                    #else:                                   #red's turn
                        #temporary code
                        #bot playing as red makes a decision
                    if stillPlaying:
                        #position = networks[0].run(board, noColumns, noRows)
                        #y = position[0]
                        #x = position[1]
                        drawX(screen, red, tileXsize, tileYsize, x - 1, y - 1, widthOfLine)
                        drawBox(screen, blue, height, width, widthOfLine)
                        board[y][x] = 2
                        count += 1
                        '''if winDetection(board, x, y, inALine, 2):
                            screen.blit(text2, ((width - text2.get_width()) / 2, (height - text2.get_height()) / 2))
                            stillPlaying = False
                        elif count == noColumns * noRows:
                            screen.blit(text3, ((width - text3.get_width()) / 2, (height - text3.get_height()) / 2))
                            stillPlaying = False'''

                    #isBlueTurn = 1 - isBlueTurn
                
        pygame.display.flip()
        clock.tick(60)

'''def playOneRound(networks, populationSize, numberOfBestIndividuals, rateOfMutation, board, noColumns, noRows, inALine, screen, colours, height, width, tileXsize, tileYsize, widthOfLine, boxColour, text, roundNumber, skillIndex, index):
    #inits
    scores = [[0 for j in range(2)] for i in range(populationSize)]
    for i in range(populationSize):
        scores[i][1] = i
    delayTime = 1000
    font = pygame.font.SysFont("Times New Roman", 30)
    gameNumber = 0

    #core
    for i in range(populationSize):
        for j in range(populationSize):
            if i != j:
                gameNumber += 1
                screen.fill((0, 0, 0))
                number1 = font.render(str(roundNumber), True, (255, 255, 255))
                screen.blit(number1, (0, 0))
                number2 = font.render(str(gameNumber), True, (255, 255, 255))
                screen.blit(number2, (0, 30))
                number3 = font.render(str(skillIndex), True, (255, 255, 255))
                screen.blit(number3, (0, 60))
                if populationSize >= 3:
                    number4 = font.render(str(networks[0].index) + " " + str(networks[1].index) + " " + str(networks[2].index), True, (255, 255, 255))
                    screen.blit(number4, (0, 90))
                winner = botVSbot(networks, board, noColumns, noRows, inALine, screen, colours, height, width, tileXsize, tileYsize, widthOfLine, boxColour, i, j, 0)
                if winner == -1:
                    scores[i][0] += 1
                    scores[j][0] += 1
                    #screen.blit(text[2], ((width - text[2].get_width()) / 2, (height - text[2].get_height()) / 2))
                else:
                    scores[winner][0] += 3
                    #if winner == i:
                    #    winner = 0
                    #else:
                    #    winner = 1
                    #screen.blit(text[winner], ((width - text[winner].get_width()) / 2, (height - text[winner].get_height()) / 2))
                    
                    #pygame.time.delay(delayTime)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return (False, networks, index)
    
    #giving birth to a new generation
    tempTuple = newGeneration(scores, networks, populationSize, numberOfBestIndividuals, rateOfMutation, index)
    networks = tempTuple[0]
    index = tempTuple[1]
    return (True, networks, index)
'''



if __name__ == '__main__':
    main()
