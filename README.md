# TicTacToe
The aim of this hobbyist project was to create a model capable of playing an extended version of TicTacToe (aka [Gomoku](https://en.wikipedia.org/wiki/Gomoku)).
The chosen approach was a reinforcement learning method known as policy gradient (with the help of discounted rewards). The model itself
is a simple fully connected neural network with one hidden layer. Training is done through self-play - the model is playing against itself
and then actions which led to victory are encouraged, while actions which led to loss are discouraged.

## Execution
To execute the program yourself, download the repository and then type `python main.py` in a directory where the repository is stored.
Please note that in order to execute the program you will need *pytorch*, *numpy* and *pygame* modules as well as *Python* itself.

## Results
To simplify the problem, a smaller board was chosen (5x5 with 4 in a line to win).
The trained model is capable of beating an opponent making completely random decisions around 90% of the time. This means that
you would have to be blind not to beat it yourself.
The results are rather disappointing due to a few reasons:
* self-play is usually not a stable (or easy) method of training a model
* reinforcement learning often requires a lot of computation power - probably much more than during the development of this project
* the problem itself is far from trivial - Gomoku is quite similar to Go, a game which has only recently been mastered by AI

Nevertheless, this project achieved a simple goal - develop a model trained entirely through self-play which is clearly better than doing
completely random moves.

## Future improvements
* improve training process
* use more sophisticated model (e.g. a Convolutional Neural Network)
* pair the neural network with Monte Carlo Tree Search - this should improve stability of self-play
* add menu
* add support for non-square boards
