from Player import Player
from random import randrange, choice
from GameState import GameState
from Card import Card
import copy

class RandomPlayer(Player):

    CHANCE_OF_RND_1_BID = 8
    CHANCE_OF_RND_2_BID = 8
    CHANCE_OF_LOANER = 32

    def make_move(self, game_state: GameState):
        # Randomly pick a card.
        card = choice(self.hand)
        while not game_state.is_valid_play(card, self.hand):
            card = choice(self.hand)
        print("{} plays {}".format(self.name, card))
        self.hand.remove(card)
        return card

    def make_bid_rnd_1(self, game_state: GameState) -> int:
        """
        Determine at a 1/4 way if the player will order up / assist.

        :return: True if the player orders it up / assists False if they pass
        """
        val = randrange(0, RandomPlayer.CHANCE_OF_RND_1_BID)
        if val == 0:
            # Order up
            return Player.ORDER_UP

        return Player.PASS

    def is_loaner(self, game_state: GameState) -> bool:
        """
        Determine if the player wants to go alone or not.

        In this simple implementation, te player will randomly choose to go alone.

        :param game_state: The GameState object
        :return: True of he player will go alone. False otherwise.
        """
        val = randrange(0, RandomPlayer.CHANCE_OF_LOANER)
        if val == 0:
            self.going_alone = True
            self.is_out = False
            return True

    def make_bid_rnd_2(self, game_state: GameState) -> int:

        pick_suit = randrange(0, RandomPlayer.CHANCE_OF_RND_2_BID)
        if pick_suit != 0:
            return Card.SUIT_NOSUIT

        suits = copy.copy(Card.SUITS) # a little slow, but readable. Necessary so we don't all modify the same list.
        invalid_suit = game_state.top_card.get_suit()
        print("Removing Suit: {}".format(invalid_suit))
        print("Suits: {}".format(suits))
        suits.remove(invalid_suit)

        picked_suit = choice(suits)
        return picked_suit

    def discard(self, game_state: GameState) -> Card:
        idx = randrange(0, len(self.hand))
        discard = self.hand[idx]
        del self.hand[idx] # @TODO: I'm not iterating...does this have consequences?
        return discard