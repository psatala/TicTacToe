'''import numpy as np
import torch
import random
import math

print(torch.__version__)


boardGameSize = 5
boardTotalSize = boardGameSize + 2
inALine = 4
discountRate = 0.9

def transformInput(board, turn):
  boardGameSize = len(board) - 2
  boardExtended = np.repeat(board[1:boardGameSize + 1, 1:boardGameSize + 1].flatten()[:, np.newaxis], 2, axis=1) #create new np array from two copies of sliced board
  boardExtended = boardExtended.transpose()
  
  if turn != 1: 
    boardExtended *= -1 #change perspective for red's move
  
  boardExtended[0][boardExtended[0] < 0] = 0 #filter first copy
  boardExtended[1][boardExtended[1] > 0] = 0 #filter second copy

  boardExtended[1] *= -1
  
  boardExtended = boardExtended.flatten()
  #boardExtended = boardExtended.reshape(1, len(boardExtended))
  
  return boardExtended

class Model(torch.nn.Module):
  def __init__(self, sizeFirst, sizeHidden, sizeLast):
    super(Model, self).__init__()
    self.linear1 = torch.nn.Linear(sizeFirst, sizeHidden, bias = True)
    self.linear2 = torch.nn.Linear(sizeHidden, sizeLast, bias = True)

  def forward(self, x):
    hidden = self.linear1(x)
    hidden = torch.nn.functional.relu(hidden)

    y_pred = self.linear2(hidden)
    y_pred = torch.nn.functional.softmax(y_pred, dim=-1)
    
    return y_pred


model = Model((boardGameSize**2) * 2, 32, boardGameSize**2)

def filterResults(res, board):
  res = res.reshape(boardGameSize**2)
  for i in range(boardGameSize):
    for j in range(boardGameSize):
      if board[i + 1][j + 1] != 0:
        res[i * boardGameSize + j] = 0
  return res

def normalize(res):
  temp = res.sum()
  for i in range(len(res)):
    res[i] /= temp
  return res

def sampleRandom(res, board):
  boardGameSize = len(board) - 2
  tempArray = np.random.permutation(boardGameSize**2)
  for i in range(len(tempArray)):
    if res[tempArray[i]] > 0:
      return tempArray[i]

#mode=1: selfplay
#mode=2: agent vs random opponent
def playGame(model, boardGameSize, inALine, discountRate = 0.9, mode = 1):
  
  #inits
  
  board = np.zeros([boardTotalSize, boardTotalSize], dtype = int)
  
  nMoves = 0
  isWinnerFound = False
  winner = 0
  turn = 1
  
  listOfBoardStates = []
  listOfDecisions = []
  
  random.seed()
  
  #game loop
  
  while not isWinnerFound:
  
    #check draw
    if nMoves == boardGameSize**2:
      break
    nMoves += 1
    
    #transform and save input
    nnInput = transformInput(board, turn)
    nnInput = torch.from_numpy(nnInput).float()
    listOfBoardStates.append(nnInput)
    
    #calculate probability distribution
    res = model(nnInput)
    res = filterResults(res, board)
    res = normalize(res)
    
    
    #sample move (agent)
    m = torch.distributions.Categorical(res)
    index = m.sample()
    
    #sample move (random opponent)
    if mode == 2 and turn == -1:
      index = sampleRandom(res, board)
    
    #make move
    a = (index // boardGameSize) + 1
    b = (index % boardGameSize) + 1
    if board[a][b] != 0:
      print("Noooo!")
    board[a][b] = turn
    
    #save move
    listOfDecisions.append(index)
    
    #check if someone won
    if winDetection(board, b, a, inALine, turn):
      isWinnerFound = True
      winner = turn
    
    #change turn
    turn *= -1
  
  listOfLabels = torch.tensor(listOfDecisions)
  return listOfBoardStates, listOfLabels, winner

def calculateRewards(listOfBoardStates, winner, discountRate = 0.9):
  rewards = torch.zeros([len(listOfBoardStates)], dtype=float)
  if winner != 0:
    rewards[-1] = 1
    rewards[-2] = -1
    for i in range(len(listOfBoardStates) - 3, -1, -1):
      rewards[i] = rewards[i + 2] * discountRate
  
    rewards -= torch.mean(rewards)
    rewards /= torch.std(rewards)
  
  return rewards

def playAgainstRandom(nRounds):
  winCounter = 0

  for i in range(nRounds):
    _, __, winner = playGame(model, boardGameSize, inALine, mode=2)
    if winner == 1:
      winCounter += 1
  
  return winCounter / float(nRounds)

import time

startTime = time.time()
score = playAgainstRandom(100)
endTime = time.time()

score, endTime - startTime

baseLR = 1e-3
epoch = 0
nEpochs = 2 * (10 ** 4)
validateEvery = 10 ** 2
nRoundsOfValidation = 10 ** 2
decayEvery = 5 * (10 ** 3)

optimizer = torch.optim.Adam(model.parameters(), lr = baseLR)

def train(model, optimizer, data):
  for input, lb, rew in data:
    optimizer.zero_grad()
    result = model(input)
    m = torch.distributions.Categorical(result)
    loss = -m.log_prob(lb) * rew
    #print(loss, lb, rew, result)
    if loss == loss:
      loss.backward()
      optimizer.step()

def adjustLR(optimizer, epoch, baseLR, decayEvery):
  for g in optimizer.param_groups:
    g['lr'] = baseLR * (0.1 ** (epoch // decayEvery))

for i in range(nEpochs):
  listOfBoardStates, listOfDecisions, winner = playGame(model, boardGameSize, inALine, discountRate)
  rewards = calculateRewards(listOfBoardStates, winner, discountRate)
  zipper = zip(listOfBoardStates, listOfDecisions, rewards)
  data = list(zipper)
  
  train(model, optimizer, data)
  epoch += 1
  
  adjustLR(optimizer, epoch, baseLR, decayEvery)

  if epoch % validateEvery == 0:
    score = playAgainstRandom(nRoundsOfValidation)
    print(epoch, score)
    for param in optimizer.param_groups:
      print("%.7f" % param['lr'])

for name, param in model.named_parameters():
  if param.requires_grad:
    print(name, param.data)

'''