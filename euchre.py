from Simulator import Simulator
from Table import GameType
from RandomPlayer import RandomPlayer
import logging
import pymongo
import sys
from euchre import db

def main():
    # @todo: this may not be necessary in the future.
    db.choices.delete_many({})
    print("Type of mongodb: {}".format(type(db)))
    sim = Simulator(GameType.TRADITIONAL, 10, RandomPlayer)
    sim.run()


if __name__ == "__main__":
    main()
