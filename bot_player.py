from model import *
import numpy as np

class BotPlayer:


  def __init__(self, path, nRows, nColumns, sizeHidden, board):
    self.boardGameSize = len(board) - 2

    self.model = Model(2 * nRows * nColumns, sizeHidden, nRows * nColumns)
    self.model.load_state_dict(torch.load(path))
    self.model.eval()


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
    
    row = int(index // self.boardGameSize) + 1
    column = int(index % self.boardGameSize) + 1
    
    return False, row, column



  ################################################################################################################
  #                                             Auxiliary functions                                              #
  ################################################################################################################


  def transformInput(self, board, turn):       #transform data from board to match model's input
    boardExtended = np.repeat(board[1:self.boardGameSize + 1, 1:self.boardGameSize + 1].flatten()[:, np.newaxis], 2, axis=1) #create new np array from two copies of sliced board
    boardExtended = boardExtended.transpose()
    
    if turn != 1: 
      boardExtended *= -1; #change perspective for red's move
    
    boardExtended[0][boardExtended[0] < 0] = 0 #filter first copy
    boardExtended[1][boardExtended[1] > 0] = 0 #filter second copy

    boardExtended[1] *= -1
    
    boardExtended = boardExtended.flatten()
    
    return boardExtended


  def filterResults(self, board):      #filter out the results corresponding to impossible moves
    self.res = self.res.reshape(self.boardGameSize**2)
    for i in range(self.boardGameSize):
      for j in range(self.boardGameSize):
        if board[i + 1][j + 1] != 0:
          self.res[i * self.boardGameSize + j] = 0



  def normalize(self):                 #normalise probabilities after filtering
    temp = self.res.sum()
    for i in range(len(self.res)):
      self.res[i] /= temp
