from Card import Card
from GameState import GameState

class Player(object):

    ORDER_UP = True
    PASS = False

    def __init__(self, player_num: int, team_id: int, player_name: str):
        self.team_id = team_id
        self.hand = list()
        self.name = player_name
        self.player_num = player_num
        self.is_dealer = False

        self.going_alone = False
        self.sitting_out = False

    def make_move(self, game_state: GameState):
        raise Exception("Cannot have a player without a personality.")

    def receive_card(self, card_list: list):
        """
        Receive a list of cards.

        Must be a list
        :param card_list: a list of N cards to put into the hand
        :return: Nothing
        """
        self.hand += card_list

    def make_bid_rnd_1(self, game_state: GameState):
        raise Exception("Players without personalities cannot make bids")

    def make_bid_rnd_2(self, game_state: GameState):
        raise Exception("Players without personalities cannot pick trumps.")

    def discard(self, game_state: GameState):
        raise Exception("Players without personalities cannot decide what to discard.")

    def is_loaner(self, game_state: GameState) -> bool:
        raise Exception("Players without personalities are always loaners and that makes for a bad partner!")

    def set_dealer(self):
        self.is_dealer = True

    def set_not_dealer(self):
        self.is_dealer = False

    def get_is_dealer(self) -> bool:
        return self.is_dealer

    def clear_hand(self):
        self.hand = list()

    def sit_out(self):
        self.sitting_out = True
        self.going_alone = False

    def __repr__(self):
        return "Name: {} Team {} Hand: {}".format(self.name, self.team_id, self.hand)
