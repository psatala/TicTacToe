import torch

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