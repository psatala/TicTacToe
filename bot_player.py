#Name: bot_player.py
#Purpose: file containing BotPlayer class, which handles interaction with the bot


from model import *
import numpy as np



class BotPlayer:


    #constructor
    #parameters are: path to file with a model, number of rows, number of columns, size of hidden layer, board
    #note: not square boards are not yet supported
    def __init__(self, path, nRows, nColumns, sizeHidden, board):
        self.boardGameSize = len(board) - 2

        self.model = Model(2 * nRows * nColumns, sizeHidden, nRows * nColumns)
        self.model.load_state_dict(torch.load(path))
        self.model.eval()



    #function responsible for sampling a move from bot
    #parameters are: board with the current state of the game, current turn
    #return values are: whether or not bot has clicked exit (false - bots don't do that), row of sampled move, column of sampled move
    def sampleMove(self, board, turn):

        #transform and save input
        nnInput = self.transformInput(board, turn)
        nnInput = torch.from_numpy(nnInput).float()
    
        #calculate probability distribution
        self.res = self.model(nnInput)
        self.filterResults(board)
        self.normalize()
    
        #sample move (agent)
        m = torch.distributions.Categorical(self.res)
        index = m.sample()
    
        #get row and column
        row = int(index // self.boardGameSize) + 1
        column = int(index % self.boardGameSize) + 1
    
        return False, row, column





    ################################################################################################################
    #                                             Auxiliary functions                                              #
    ################################################################################################################


    #transform data from board to match model's input
    #parameters are: board with the current state of the game, current turn
    #return values are: numpy array containing transformed input
    def transformInput(self, board, turn):
        boardExtended = np.repeat(board[1:self.boardGameSize + 1, 1:self.boardGameSize + 1].flatten()[:, np.newaxis], 2, axis=1) #create new np array from two copies of sliced board
        boardExtended = boardExtended.transpose()
    
        if turn != 1: 
            boardExtended *= -1; #change perspective for red's move
    
        boardExtended[0][boardExtended[0] < 0] = 0 #filter first copy
        boardExtended[1][boardExtended[1] > 0] = 0 #filter second copy

        boardExtended[1] *= -1
    
        boardExtended = boardExtended.flatten()
    
        return boardExtended



    #filter out the results corresponding to impossible moves
    #parameters are: board with current state of the game
    def filterResults(self, board):
        self.res = self.res.reshape(self.boardGameSize**2)
        for i in range(self.boardGameSize):
            for j in range(self.boardGameSize):
                if board[i + 1][j + 1] != 0:
                    self.res[i * self.boardGameSize + j] = 0



    #normalise probabilities after filtering
    def normalize(self):
        temp = self.res.sum()
        for i in range(len(self.res)):
            self.res[i] /= temp

    