from Player import Player
from GameState import GameState
from Card import Card
from secrets import randbelow, choice
import copy
import logging
from typing import List


class BasicPlayer(Player):

    CHANCE_OF_RND_1_BID = 4
    CHANCE_OF_RND_2_BID = 4
    CHANCE_OF_LOANER = 32

    def make_move(self, game_state: GameState):

        card = None

        if len(game_state.trick_cards) == 0:
            # It's my lead
            card = self.get_biggest_trump(game_state.trumps)
            if card is None:
                # lead biggest off suit
                card = self.get_biggest_non_trump(game_state.trumps)

        elif len(game_state.trick_cards) < 4:
            # I'm not at the end
            pass
        else:
            # I'm the last person. Determine if my partner is already winning
            current_winner = game_state.calc_winner()
            # @ todo, this should be fixed, its not always going to be that player id and team id are connected.
            current_winner_team_id = current_winner % 2

            # My partner has already won the trick, toss something stupid
            if current_winner_team_id == self.team_id:

                card = self.find_lowest_card(game_state.trumps)

            # The other team is winning the trick. Determine if I can win
            card = self.winning_card(game_state.trumps, game_state.trick_cards)
            if card is None:
                # No way to win, toss something stupid
                card = self.find_lowest_card(game_state.trumps)

        self.hand.remove(card)
        return card

    def make_bid_rnd_1(self, game_state: GameState) -> int:
        """
        Determine if we should order up.

        :return: True if the player orders it up / assists False if they pass
        """

        hand_strength = self.calc_hand_strength(game_state.top_card)
        if hand_strength >= 7:
            return Player.ORDER_UP

        return Player.PASS

    def is_loaner(self, game_state: GameState) -> bool:
        """
        Determine if the player wants to go alone or not.

        In this basic strategy the player always relies on their partner, and never goes alone.

        :param game_state: The GameState object
        :return: True of he player will go alone. False otherwise.
        """
        return False

    def make_bid_rnd_2(self, game_state: GameState) -> int:
        suits = copy.copy(Card.SUITS) # a little slow, but readable. Necessary so we don't all modify the same list.
        invalid_suit = game_state.top_card.get_suit()
        suits.remove(invalid_suit)

        strongest_suit = 0
        best_suit = Card.SUIT_NOSUIT
        for suit in suits:
            hand_strength = self.calc_hand_strength(Card(suit, 10)) # The value doesn't matter.
            if hand_strength > strongest_suit:
                best_suit = suit
                strongest_suit = hand_strength

        if strongest_suit >= 7:
            return best_suit
        else:
            return Card.SUIT_NOSUIT

    def discard(self, game_state: GameState) -> Card:
        """
        The dealer will be required to discard if he has a card ordered up.
        This function decides what to discard.

        :param game_state: The game state object
        :return: The discarded card.
        """
        idx = None
        voidable_suits = self.find_voidable_suits(game_state.trumps)
        if len(voidable_suits) > 0:
            for index, card in enumerate(self.hand):
                if card.get_suit() == voidable_suits[0]:
                    idx = index
                    break

        else:

            lowest_card = self.find_lowest_card(game_state.trumps)
            for index, card in self.hand:
                if card == lowest_card:
                    idx = index

        discard = self.hand[idx]
        del self.hand[idx] # @TODO: I'm not iterating...does this have consequences?
        return discard

    def count_suit(self, suit):
        count = 0
        for card in self.hand:
            if card.suit == suit:
                count += 1
        return count

    def would_have_right_bower(self, top_card: Card):
        for card in self.hand:
            if card.value == Card.JACK and top_card.suit == card.suit:
                return True
        return False

    def would_have_left_bower(self, top_card: Card):
        for card in self.hand:
            if card.value == Card.JACK and top_card.get_matching(card.suit) == card.suit:
                return True
        return False

    def has_card(self, value, suit):
        for card in self.hand:
            if card.value == value and card.suit == suit:
                return True
        return False

    def num_offsuit_aces(self, avoid_suit):
        count = 0
        for card in self.hand:
            if card.value == Card.ACE and card.get_raw_suit() != avoid_suit:
                count += 1

        return count

    def calc_hand_strength(self, potential_trump: Card):
        """
        Hand strength system found at: https://www.thespruce.com/how-to-bid-in-euchre-411487
        Other systems exist that I may implement in the future.

        :param potential_trump: The potential trump card.
        :return:
        """
        hand_strength = 0

        if self.would_have_right_bower(potential_trump):
            hand_strength += 3
        if self.would_have_left_bower(potential_trump):
            hand_strength += 3

        top_card_suit = potential_trump.get_raw_suit()
        if self.has_card(Card.ACE, top_card_suit):
            hand_strength += 2
        if self.has_card(Card.KING, top_card_suit):
            hand_strength += 2
        if self.has_card(Card.QUEEN, top_card_suit):
            hand_strength += 2
        if self.has_card(Card.JACK, top_card_suit):
            hand_strength += 2
        if self.has_card(10, top_card_suit):
            hand_strength += 1
        if self.has_card(9, top_card_suit):
            hand_strength += 1

        offsuit_aces = self.num_offsuit_aces(top_card_suit)
        hand_strength += (offsuit_aces)
        return hand_strength

    def find_voidable_suits(self, avoid_suit: int):
        suit_count = [0 for _ in range(4)]
        for card in self.hand:
            suit_count[card.get_suit()] += 1

        voidable_suits = list()
        for num, count in enumerate(suit_count):
            if count == 1 and num != avoid_suit:
                voidable_suits.append(num)

        return voidable_suits

    def find_lowest_card(self, avoid_suit):

        lowest_card = None

        for card in self.hand:
            if lowest_card is None and card.suit != avoid_suit:
                lowest_card = card
                continue

            if card.value < lowest_card.value and card.suit != avoid_suit:
                lowest_card = card

        return lowest_card

    def get_biggest_trump(self, trump_suit):
        trump_cards = self.get_trump_cards(trump_suit)
        if len(trump_cards) == 0:
            # I have no trumps
            return None

        if len(trump_cards) == 1:
            return trump_cards[0]

        biggest_card = None
        for card in self.hand:
            if biggest_card is None and card.suit == trump_suit:
                biggest_card = card
                continue

            if biggest_card.value < card.value and card.suit == trump_suit:
                biggest_card = card

        return biggest_card

    def get_trump_cards(self, trump_suit) -> List(Card):
        """
        Return all of the card sin my hand that are trumps.

        :param trump_suit: The suit of trump.
        :return: A list of cards.
        """
        cards = [card for card in self.hand if card.get_suit(trump_suit) == trump_suit]
        return cards

    def get_biggest_non_trump(self, trump_suit):
        card = max(card.value for card in self.hand if card.get_suit(trump_suit) != trump_suit)
        return card

    def find_lowest_card(self, trump_suit) -> Card:
        """
        Get the worst possible card in my hand and get rid of it.
        :param trump_suit: The suit of trump, don't pick this card.

        :return: A card that is the lowest card in my hand
        """
        lowest_card = None

        for card in self.hand:
            if lowest_card is None and card.get_suit(trump_suit) != trump_suit:
                lowest_card = card
                continue
            if lowest_card > card.value and card.get_suit(trump_suit) != trump_suit:
                lowest_card = card

        # We found no non-trump cards.
        if lowest_card is None:
            for card in self.hand:
                if lowest_card is None:
                    lowest_card = card
                    continue
                if lowest_card.value > card.value:
                    lowest_card = card

        return lowest_card

    def winning_card(self, trump_suit, tricks_played):
        """

        :param trump_suit:
        :param tricks_played:
        :return:
        """