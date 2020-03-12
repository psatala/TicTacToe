#Name: main.py
#Purpose: main file of the program

from game import Game


def main():
    game = Game(nRows=5, nColumns=5, inALine=4, player2=2)  #creation of game object
    game.gameloop()   #main loop of the game



if __name__ == '__main__':
    main()
