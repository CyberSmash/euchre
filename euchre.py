from Simulator import Simulator
from Table import GameType
from RandomPlayer import RandomPlayer
import logging
import pymongo
import sys
import db

FORMAT = "[%(levelname)s] %(message)s"


def main():

    logging.basicConfig(format=FORMAT, level=logging.INFO, filename="gamelog.txt")
    # @todo: this may not be necessary in the future.
    dbase = db.quick_setup()
    dbase.choices.delete_many({})
    dbase.games.delete_many({})
    dbase.tricks.delete_many({})

    print("Deleted old data. Continuing....")
    sim = Simulator(GameType.PROGRESSIVE, 1, RandomPlayer)
    sim.run()


if __name__ == "__main__":
    main()
