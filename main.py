from game import Game

def main():
    game = Game(nRows=5, nColumns=5, inALine=4, player2=1)
    game.gameloop()

if __name__ == '__main__':
    main()
