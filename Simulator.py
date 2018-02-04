from Table import Table, GameType
from GameState import GameState
from Player import Player
from RandomPlayer import RandomPlayer
import logging
from typing import List, TypeVar

# @todo: This isn't working right. Not sure if its my IDE or something else.
P = TypeVar('P', Player, RandomPlayer)


class Simulator(object):
    def __init__(self, game_type: GameType, num_games: int, player_strategy: P):
        self.game_type = game_type
        self.num_games = num_games

        # @todo Need to make this some sort of specifiable list but not supported by the table.
        self.player_strategy = player_strategy
        self.game_count = 0

    def run_game(self):
        # Play one full game.
        t = Table(self.player_strategy, self.game_type)
        while True:
            if t.game_state.get_state() == GameState.TRICK_START:
                t.print_player_hands()
            t.step_game()

            if t.game_state.get_state() == GameState.GAME_START:
                break
        self.game_count += 1

    def run(self):
        for x in range(0, self.num_games):
            self.run_game()
