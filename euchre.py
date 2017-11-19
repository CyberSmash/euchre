from Table import Table
from GameState import GameState
from Player import Player
from RandomPlayer import RandomPlayer


def main():

    t = Table(player_type=RandomPlayer)
    while t.game_state.get_state() != GameState.BIDDING_RND_1:
        t.step_game()

    for player in t.players:
        print(player)

    while t.game_state.get_state() != GameState.HAND_END:
        t.step_game()

    print(t.get_dealer())

if __name__ == "__main__":
    main()