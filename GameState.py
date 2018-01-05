from Deck import Deck
from Card import Card
from typing import List
import logging
class GameState(object):

    DEAL = 0
    BIDDING_RND_1 = 1
    BIDDING_RND_2 = 2
    HAND_BEGIN = 3 # This is the beginning of a hand after bidding
    TRICK_START = 4 # This is a the beginning of a new trick, Leading player plays.
    TRICK_MIDDLE = 5 # All other tricks are played here
    TRICK_END = 6 # This is the end of a trick. Nothing is played
    HAND_END = 7 # This is the end of a hand before either GAME_END or DEAL
    GAME_END = 8

    def __init__(self):
        """
        Constructor. Nothing special.
        """
        self.state = GameState.DEAL
        self.trick_cards = dict()

        # Used for bidding.
        self.top_card = None

        self.trumps = None
        self.defending_team = None
        self.bidding_team = None
        self.lead_card = None
        self.lead_player = None
        self.played_cards = list()
        self.trick_num = 0

    def calc_winner(self):
        """
        Determine the winner at the end of a trick.

        :return: The player number of the winner.
        """
        # This isn't an efficient way to do this, but it works.
        best_card = 0
        best_player = -1
        for player_num, card in self.trick_cards.items():
            current_card_val = card.get_total_value(self.trumps, self.lead_card.suit)
            if best_card < current_card_val:
                best_card = current_card_val
                best_player = player_num

        return best_player

    def reset_trick(self):
        self.lead_card = None
        #self.played_cards += self.trick_cards
        self.trick_cards = dict()

    def set_state(self, new_state: int):
        self.state = new_state
        logging.info("Game State Changed to {}".format(self.get_current_state_str()))

    def progress_state(self):
        self.state += 1 % (GameState.GAME_END + 1)

    def get_state(self) -> int:
        return self.state

    def is_bidding(self) -> bool:
        return self.state == GameState.BIDDING_RND_1 or self.state == GameState.BIDDING_RND_2

    def is_deal(self) -> bool:
        return self.state == GameState.DEAL

    def is_trick_start(self) -> bool:
        return self.state == GameState.TRICK_START

    def is_trick_middle(self) -> bool:
        return self.state == GameState.TRICK_MIDDLE

    def is_trick_end(self) -> bool:
        return self.state == GameState.TRICK_END

    def is_end(self):
        return self.state == GameState.GAME_END

    def is_loaners(self):
        return self.state == GameState.LOANERS

    def is_hand_begin(self):
        return self.state == GameState.HAND_BEGIN

    def is_hand_end(self):
        return self.state == GameState.HAND_END

    def add_card(self, card):
        self.trick_cards = card

    def set_top_card(self, card: Card):
        self.top_card = card
        logging.info("Top Card: {}".format(self.top_card))

    def give_top_card(self):
        """
        Called when a player has ordered up / assisted
        :return:
        """
        card = self.top_card
        return card

    def set_trumps(self, suit: int):
        self.trumps = suit

    def reset_trumps(self):
        self.trumps = None

    def get_current_state_str(self) -> str:
        """
        Get the string of the current state
        :return: string of the state.
        """
        return self.get_state_str(self.state)

    def get_state_str(self, state: int) -> str:
        """
        Gett the state of a string
        :param state:
        :return:
        """
        if state == GameState.DEAL:
            return "DEAL"
        if state == GameState.BIDDING_RND_1:
            return "FIRST BIDDING ROUND"
        if state == GameState.BIDDING_RND_2:
            return "SECOND BIDDING ROUND"
        if state == GameState.HAND_BEGIN:
            return "HAND BEGIN"
        if state == GameState.TRICK_START:
            return "TRICK START"
        if state == GameState.TRICK_MIDDLE:
            return "TRICK MIDDLE"
        if state == GameState.TRICK_END:
            return "TRICK END"
        if state == GameState.HAND_END:
            return "HAND END"
        if state == GameState.TRICK_END:
            return "TRICK END"
        if state == GameState.GAME_END:
            return "END"

    def is_valid_play(self, played_card: Card, player_hand: list) -> bool:
        """
        Determine if the card that's played is legal to play.

        :param played_card: The card the player chose to play
        :param player_hand: The rest of the players hand.
        :return: True if the card is a valid one. False otherwise.
        """
        if self.lead_card is None:
            # Person who plays first can play anything...
            return True

        lead_suit = self.lead_card.get_suit(self.trumps)
        if played_card.get_suit(self.trumps) == lead_suit:
            # As long as we're following suit, it's always correct.
            return True

        # Determine if the player COULD have followed suit.
        for card in player_hand:
            if card.get_suit(self.trumps) == lead_suit and card is not played_card:
                # Player could have lead with a different card of appropriate suit.
                return False

        return True

    def get_valid_plays(self, hand: list) -> list:
        """
        Get all of the valid plays in a players hand.

        :param hand: A list of cards that make up the players hand.
        :return: A list of valid cards to play
        """
        valid_plays = list()

        for card in hand:
            if self.is_valid_play(card, hand):
                valid_plays.append(card)

        return valid_plays