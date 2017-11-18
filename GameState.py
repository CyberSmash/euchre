from Deck import Deck
from Card import Card

class GameState(object):

    DEAL = 0
    BIDDING_RND_1 = 1
    BIDDING_RND_2 = 2
    TRICK_START = 3
    TRICK_END = 4
    HAND_END = 5
    END = 6


    def __init__(self):
        self.state = GameState.DEAL
        self.trick_cards = dict()

        # Used for bidding.
        self.top_card = None

        self.trumps = None
        self.defending_team = None
        self.bidding_team = None
        self.lead_card = None

    def calc_winnner(self):
        # First search for trump cards.
        pass


    def reset_trick(self):
        self.lead_card = None
        self.trick_cards = list()


    def set_state(self, new_state: int):
        self.state = new_state
        print("Game State Changed to {}".format(self.get_current_state_str()))

    def progress_state(self):
        self.state += 1 % (GameState.END + 1)

    def get_state(self) -> int:
        return self.state

    def is_bidding(self) -> bool:
        return self.state == GameState.BIDDING_RND_1 or self.state == GameState.BIDDING_RND_2

    def is_deal(self) -> bool:
        return self.state == GameState.DEAL

    def is_trick(self) -> bool:
        return self.state == GameState.TRICK_START

    def is_end(self):
        return self.state == GameState.END

    def is_loaners(self):
        return self.state == GameState.LOANERS

    def reset_trick(self):
        self.trick_cards = list()

    def add_card(self, card):
        self.trick_cards = card

    def set_top_card(self, card: Card):
        self.top_card = card

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
        if state == GameState.LOANERS:
            return "LOOKING FOR LOANERS"
        if state == GameState.TRICK_START:
            return "TRICK START"
        if state == GameState.TRICK_END:
            return "TRICK END"
        if state == GameState.END:
            return "END"

    def is_valid_play(self, played_card: Card, player_hand: list(Card)):
        """
        Determine if the card that's played is legal to play.

        :param played_card: The card the player chose to play
        :param player_hand: The rest of the players hand.
        :return: True if the card is a valid one. False otherwise.
        """
        if self.top_card is None:
            # Person who plays first can play anything...
            self.top_card = played_card
            return True

        lead_suit = self.top_card.suit
        if played_card.suit == lead_suit:
            # As long as we're following suit, it's always correct.
            return True

        # Determine if the player COULD have followed suit.
        for card in player_hand:
            if card.suit == lead_suit and card is not played_card:
                # Player could have lead with a different card of appropriate suit.
                return False

        return True