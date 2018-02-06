import logging
import pymongo
import sys
from GameState import GameState
from Player import Player
from Card import Card

HOST = 'localhost'
PORT = 27017

db = None
client = None


def setup_database(host, port):
    global client
    global db

    try:
        client = pymongo.MongoClient(host, port)
    except pymongo.errors.ConnectionFailure as ex:
        print("Cannot connect to database")
        logging.error("Cannot connect to database")
        sys.exit(1)

    try:
        db = client['euchre']
    except KeyError:
        print("Database euchre does not exist.")
        sys.exit(1)


def quick_setup():
    setup_database(HOST, PORT)
    return db


def get_connection():
    global client

    if not client:
        setup_database(HOST, PORT)
    return client


def get_stats_db():
    global db
    if not db:
        setup_database(HOST, PORT)
    return db


def create_new_trick(game_state: GameState, player: Player, card: Card) -> dict:
    """
    @TODO This should be moved to some database file. IT should't be here.
    :param game_state: The game state object
    :return:
    """
    global db

    new_trick = dict()
    new_trick['trick_num'] = game_state.trick_num
    new_trick['hand_num'] = game_state.num_hands
    new_trick['game_id'] = game_state.game_id
    new_trick['order'] = [player.player_num]
    new_trick[player.name] = '{}'.format(card)

    db.tricks.insert(new_trick)



def update_trick(game_state: GameState, player: Player, card: Card):
    global db

    db.tricks.update(
        {
            '$and': [
                {'trick_num': game_state.trick_num},
                {'hand_num': game_state.num_hands},
                {'game_id': game_state.game_id},
            ]
        },
        {
            '$push': {'order': player.player_num},
            '$set': {player.name: '{}'.format(card)}
        }
    )


def record_hand(game_state: GameState, defending_team_tricks: int, bidding_team_tricks: int, winning_team: int):
    global db
    db.hands.insert(
        {
            'game_id': game_state.game_id,
            'hand_num': game_state.num_hands,
            'defending_team': game_state.defending_team,
            'bidding_team': game_state.bidding_team,
            'dealer': game_state.current_dealer,
            'defending_team_tricks': defending_team_tricks,
            'bidding_team_tricks': bidding_team_tricks,

        }

    )