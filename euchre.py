from Simulator import Simulator
from Table import GameType
from RandomPlayer import RandomPlayer
import logging
import pymongo
import sys
import db
from BasicPlayer import BasicPlayer

FORMAT = "[%(levelname)s] %(message)s"


def main():

    logging.basicConfig(format=FORMAT, level=logging.WARN, filename="gamelog.txt")
    # @todo: this may not be necessary in the future.
    dbase = db.quick_setup()
    dbase.choices.delete_many({})
    dbase.games.delete_many({})
    dbase.tricks.delete_many({})

    print("Deleted old data. Continuing....")
    sim = Simulator(GameType.PROGRESSIVE, 100000, BasicPlayer)
    sim.run()


if __name__ == "__main__":
    main()
