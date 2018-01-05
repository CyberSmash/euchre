from Table import Table
from GameState import GameState
from Player import Player
from RandomPlayer import RandomPlayer
import logging


FORMAT = "[%(levelname)s] %(message)s"

def print_player_hands(players):
    for player in players:
        logging.info(player)

def main():
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)


    t = Table(player_type=RandomPlayer)
    while t.game_state.get_state() != GameState.BIDDING_RND_1:
        t.step_game()

    print_player_hands(t.players)

    while t.game_state.get_state() != GameState.HAND_END:
        if t.game_state.get_state() == GameState.TRICK_START:
            print_player_hands(t.players)
        t.step_game()

    logging.info(t.get_dealer())

if __name__ == "__main__":
    main()