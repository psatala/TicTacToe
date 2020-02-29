import pygame
import os.path
import random
#import NeuralNetworkClass

def main():
    
    #parameters
    height = 700
    width = 700
    noRows = 10
    noColumns = 10
    widthOfLine = 5
    inALine = 5
    populationSize = 15
    numberOfBestIndividuals = 3
    rateOfMutation = 0.02
    numberOfRounds = 10000
    index = 1
    
    #colours
    white = (255, 255, 255)
    grey = (128, 128, 128)
    black = (0, 0, 0)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    colours = ((0, 0, 255), (255, 0, 0))
    fileName = "data10x10_5.txt"
    
    #basic inits
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    done = False
    tileXsize = width / noColumns
    tileYsize = height / noRows
    
    networks = []
    for i in range(populationSize):
        networks.append(NeuralNetworkClass.neuralNetwork(noRows, noColumns, index))
        index += 1

    #text inits
    font = pygame.font.SysFont("Times New Roman", 100)
    text1 = font.render("Blue wins!", True, blue)
    text2 = font.render("Red wins!", True, red)
    text3 = font.render("Draw!", True, white)
    text = [text1, text2, text3]

    #gameplay inits
    pos = (0, 0)
    skillIndex = 0
    isBlueTurn = 1
    stillPlaying = True
    board = [[0 for x in range(noColumns + 2)] for y in range(noRows + 2)]
    drawGrid(screen, grey, height, width, noColumns, noRows)
    drawBox(screen, blue, height, width, widthOfLine)

    #read data from file
    read(networks, noColumns, noRows, index, populationSize, fileName)

    #player inits
    players = (1, 0)   #CHANGE HERE!!!
    if not players[0] and not players[1]:
        for i in  range(numberOfRounds):
            tuple = playOneRound(networks, populationSize, numberOfBestIndividuals, rateOfMutation, board, noColumns, noRows, inALine, screen, colours, height, width, tileXsize, tileYsize, widthOfLine, grey, text, i + 1, skillIndex, index)
            networks = tuple[1]
            index = tuple[2]
            if not tuple[0]:
                break
            skillIndex = check(networks[0], board, noColumns, noRows, inALine, screen, colours, height, width, tileXsize, tileYsize, widthOfLine, grey, index)
        save(networks, noColumns, noRows, index, populationSize, fileName)
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
                    if winDetection(board, x, y, inALine, 1):
                        screen.blit(text1, ((width - text1.get_width()) / 2, (height - text1.get_height()) / 2))
                        stillPlaying = False
                    elif count == noColumns * noRows:
                        screen.blit(text3, ((width - text3.get_width()) / 2, (height - text3.get_height()) / 2))
                        stillPlaying = False

                    #else:                                   #red's turn
                        #temporary code
                        #bot playing as red makes a decision
                    if stillPlaying:
                        position = networks[0].run(board, noColumns, noRows)
                        y = position[0]
                        x = position[1]
                        drawX(screen, red, tileXsize, tileYsize, x - 1, y - 1, widthOfLine)
                        drawBox(screen, blue, height, width, widthOfLine)
                        board[y][x] = 2
                        count += 1
                        if winDetection(board, x, y, inALine, 2):
                            screen.blit(text2, ((width - text2.get_width()) / 2, (height - text2.get_height()) / 2))
                            stillPlaying = False
                        elif count == noColumns * noRows:
                            screen.blit(text3, ((width - text3.get_width()) / 2, (height - text3.get_height()) / 2))
                            stillPlaying = False

                    #isBlueTurn = 1 - isBlueTurn
                
        pygame.display.flip()
        clock.tick(60)

def playOneRound(networks, populationSize, numberOfBestIndividuals, rateOfMutation, board, noColumns, noRows, inALine, screen, colours, height, width, tileXsize, tileYsize, widthOfLine, boxColour, text, roundNumber, skillIndex, index):
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


def newGeneration(scores, networks, populationSize, numberOfBestIndividuals, rateOfMutation, index):
    scores.sort()
    newPopulation = []
    for i in range(numberOfBestIndividuals):
        newPopulation.append(networks[scores[populationSize - i - 1][1]])
    for i in range(numberOfBestIndividuals):
        for j in range(numberOfBestIndividuals):
            child = NeuralNetworkClass.neuralNetwork(1, networks[0].sizeOfLayers, index)
            index += 1
            newPopulation.append(crossAndMutate((newPopulation[i], newPopulation[j]), child, rateOfMutation))
    for i in range(numberOfBestIndividuals):
        newPopulation.append(NeuralNetworkClass.neuralNetwork(1, networks[0].sizeOfLayers, index))
        index += 1
    
    del networks
    populationSize = len(newPopulation)
    return (newPopulation, index)



def crossAndMutate(parents, child, rateOfMutation):
    
    for j in range(child.numberOfLayers - 1):
        for k in range(child.sizeOfLayers):
            for l in range(child.sizeOfLayers):
                
                #crossing edges
                child.layers[j][k].edges[l].weight = parents[random.randint(0, 1)].layers[j][k].edges[l].weight
                #applying mutations to edges
                if not random.randint(0, 1/rateOfMutation):
                    child.layers[j][k].edges[l].weight = random.uniform(child.rangeOfWeightValues, child.rangeOfWeightValues)
            
            #crossing nodes from every but last layer
            child.layers[j][k].bias = parents[random.randint(0, 1)].layers[j][k].bias
            #applying mutations to them
            if not random.randint(0, 1/rateOfMutation):
                child.layers[j][k].bias = random.uniform(child.rangeOfWeightValues, child.rangeOfWeightValues)
    
    for j in range(child.sizeOfLayers):
        #crossing nodes from last layer
        child.layers[child.numberOfLayers - 1][j].bias = parents[random.randint(0, 1)].layers[child.numberOfLayers - 1][j].bias
        #applying mutations to them
        if not random.randint(0, 1/rateOfMutation):
            child.layers[child.numberOfLayers - 1][j].bias = random.uniform(child.rangeOfWeightValues, child.rangeOfWeightValues)

    return child



#function responsible for bot vs bot matches
def botVSbot(networks, board, noColumns, noRows, inALine, screen, colours, height, width, tileXsize, tileYsize, widthOfLine, boxColour, firstPlayerIndex, secondPlayerIndex, drawMode):
    
    board = [[0 for x in range(noColumns + 2)] for y in range(noRows + 2)]
    if drawMode:
        drawGrid(screen, boxColour, height, width, noColumns, noRows)
    turnIndex = firstPlayerIndex
    turn = 0
    count = 0
    stillPlaying = True
    while stillPlaying:
        count +=1
        position = networks[turnIndex].run(board, noColumns, noRows)
        y = position[0]
        x = position[1]
        board[y][x] = turn + 1

        #interacting with a screen
        #fpsCounter = 10
        if drawMode:
            draw(screen, colours[turn], boxColour, height, width, x, y, tileXsize, tileYsize, widthOfLine, turn)
        #speed test
        #if not count % 10:
        #    screen.fill((0, 0, 0))
        #    font = pygame.font.SysFont("Times New Roman", 20)
        #    text = font.render(str(count), True, boxColour)
        #    screen.blit(text, ((width - text.get_width()) / 2, (height - text.get_height()) / 2))
        
        pygame.display.flip()
        #clock.tick(fpsCounter)

        if winDetection(board, x, y, inALine, turn + 1):
            stillPlaying = False
            return turnIndex
        if count == noColumns * noRows:
            return -1
       
        #new turn       
        if turnIndex == firstPlayerIndex:
            turnIndex = secondPlayerIndex
        else:
            turnIndex = firstPlayerIndex
        turn = 1 - turn

#checking how good is the best guy against a random opponent
def check(pro, board, noColumns, noRows, inALine, screen, colours, height, width, tileXsize, tileYsize, widthOfLine, boxColour, index):
    counter = 0
    for i in range(50):
        noob = NeuralNetworkClass.neuralNetwork(noRows, noColumns, index)
        firstMatch = botVSbot([pro, noob], board, noColumns, noRows, inALine, screen, colours, height, width, tileXsize, tileYsize, widthOfLine, boxColour, 0, 1, 0)
        secondMatch = botVSbot([noob, pro], board, noColumns, noRows, inALine, screen, colours, height, width, tileXsize, tileYsize, widthOfLine, boxColour, 0, 1, 0)
        if firstMatch == 0:
            counter += 1
        elif firstMatch == -1:
            counter += 0.5
        if secondMatch == 1:
            counter += 1
        elif secondMatch == -1:
            counter += 0.5
    return counter / 100

#general draw function responsible for drawing O or X and a new box
def draw(screen, colour, otherColour, height, width, column, row, tileXsize, tileYsize, widthOfLine, turn):
    if turn == 0:
        drawO(screen, colour, tileXsize, tileYsize, column - 1, row - 1, widthOfLine)
    else:
        drawX(screen, colour, tileXsize, tileYsize, column - 1, row - 1, widthOfLine)
    drawBox(screen, otherColour, height, width, widthOfLine)

#draw grid
def drawGrid(screen, colour, height, width, noColumns, noRows):
    for i in range(1, noColumns):
        pygame.draw.line(screen, colour, (i * width / noColumns, 0), (i * width / noColumns, height))
    for i in range(1, noRows):
        pygame.draw.line(screen, colour, (0, i * height / noRows), (width, i * height / noRows))


#draw cross
def drawX(screen, colour, tileXsize, tileYsize, column, row, widthOfLine):
    pygame.draw.line(screen, colour, ((column + 1/8) * tileXsize, (row + 1/8) * tileYsize), ((column + 7/8) * tileXsize, (row + 7/8) * tileYsize), widthOfLine)
    pygame.draw.line(screen, colour, ((column + 7/8) * tileXsize, (row + 1/8) * tileYsize), ((column + 1/8) * tileXsize, (row + 7/8) * tileYsize), widthOfLine)


#draw circle
def drawO(screen, colour, tileXsize, tileYsize, column, row, widthOfLine):
    pygame.draw.ellipse(screen, colour, ((column + 1/8) * tileXsize, (row + 1/8) * tileYsize, tileXsize * 3/4, tileYsize * 3/4), widthOfLine)


#draw box
def drawBox(screen, colour, height, width, widthOfLine):
    pygame.draw.rect(screen, colour, (0, 0, width, height), widthOfLine)

#win detection
def winDetection(board, x, y, inALine, value):

    moveX = [1, 0, 1, 1]   #move in x direction
    moveY = [0, 1, 1, -1]  #move in y direction

    for i in range(4):
        sum = 1
        for j in range(1, inALine):
            if(board[y + j * moveY[i]][x + j * moveX[i]] != value):
               break
            sum += 1
        for j in range(1, inALine):
            if(board[y - j * moveY[i]][x - j * moveX[i]] != value):
               break
            sum += 1
        if sum >= inALine:
            return True
    
    #no winner yet
    return False

#fuction responsbile for saving progress to a text file
def save(networks, noColumns, noRows, index, populationSize, fileName):
    dataFile = open(fileName, "w")
    
    dataFile.write(str(noColumns) + "\n")
    dataFile.write(str(noRows) + "\n")
    dataFile.write(str(index) + "\n")

    for i in range(populationSize):
        dataFile.write(str(networks[i].index) + "\n")
        for j in range(networks[i].numberOfLayers - 1):
            for k in range(networks[i].sizeOfLayers):
                for l in range(networks[i].sizeOfLayers):
                    dataFile.write(str(networks[i].layers[j][k].edges[l].weight) + "\n")
                dataFile.write(str(networks[i].layers[j][k].bias) + "\n")
        for j in range(networks[i].sizeOfLayers):
            dataFile.write(str(networks[i].layers[networks[i].numberOfLayers - 1][j].bias) + "\n")

    dataFile.close()

#function responsible for reading saved progress from a file
def read(networks, noColumns, noRows, index, populationSize, fileName):
    if not os.path.isfile(fileName):
        return
    
    dataFile = open(fileName, "r")
    
    noColumns = int(dataFile.readline())
    noRows = int(dataFile.readline())
    index = int(dataFile.readline())

    for i in range(populationSize):
        networks[i].index = int(dataFile.readline())
        for j in range(networks[i].numberOfLayers - 1):
            for k in range(networks[i].sizeOfLayers):
                for l in range(networks[i].sizeOfLayers):
                    networks[i].layers[j][k].edges[l].weight = float(dataFile.readline())
                networks[i].layers[j][k].bias = float(dataFile.readline())
        for j in range(networks[i].sizeOfLayers):
            networks[i].layers[networks[i].numberOfLayers - 1][j].bias = float(dataFile.readline())

    dataFile.close()

if __name__ == '__main__':
    main()
