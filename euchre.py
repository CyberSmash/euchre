from Simulator import Simulator
from Table import GameType
from RandomPlayer import RandomPlayer
import logging

FORMAT = "[%(levelname)s] %(message)s"


def main():
    logging.basicConfig(format=FORMAT, level=logging.DEBUG, filename="gamelog.txt")

    sim = Simulator(GameType.TRADITIONAL, 100, RandomPlayer)
    sim.run()


if __name__ == "__main__":
    main()