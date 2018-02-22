from Player import Player
from GameState import GameState
from Card import Card
from secrets import randbelow, choice
import copy
import logging
from typing import List, Optional
import operator


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

    def num_offsuit_aces(self, avoid_suit: int) -> int:
        """
        Calculate the number of offsuit aces that exist in our hand.

        :param avoid_suit: The suit we wish to not count. Typically trump or something.
        :return: The number of offsuit aces in our hand.
        """
        count = sum(1 for c in filter(lambda c: c.get_raw_suit() != avoid_suit and c.value == Card.ACE, self.hand))

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

    def find_voidable_suits(self, trump_suit: int) -> List[int]:
        """
        Find any suits which could be voided (only one card remains)

        @attention tests written

        :param trump_suit: The current trump suit, this suit will not be reported.
        :return: A list of integers containing the suits which can be voided
        """
        suit_count = [0 for _ in range(4)]
        for card in self.hand:
            suit_count[card.get_suit(trump_suit)] += 1

        voidable_suits = list()
        for num, count in enumerate(suit_count):
            if count == 1 and num != trump_suit:
                voidable_suits.append(num)

        return voidable_suits

    def find_lowest_card(self, avoid_suit: int, lead_suit: int=Card.SUIT_NOSUIT) -> Optional[Card]:
        """
        Get the lowest card possible.

        @attention tests written

        :param avoid_suit: The suit to not pick from (usually because it's trump).
        :param lead_suit: The suit that was lead. Card.SUIT_NOSUIT if it hasn't been set.
        :return: A card that is the lowest in my hand. None if a non-avoid suit card can be found.
        """
        try:
            card = min(filter(lambda a: a.suit != avoid_suit, self.hand), key=lambda c: c.get_total_value(avoid_suit, lead_suit))
        except ValueError as ex:
            return None

        return card

    def get_biggest_trump(self, trump_suit: int, lead_card_suit: int=Card.SUIT_NOSUIT) -> Optional[Card]:
        """
        Get the biggest trump-suited card in my hand.

        @attention tests written

        :param trump_suit: The trumpian suit.
        :param lead_card_suit: The lead card's suit.
        :return: None if there are no trump cards. The biggest trump card if one exists.
        """
        try:
            card = max(filter(lambda a: a.get_suit(trump_suit) == trump_suit, self.hand),
                       key=lambda c: c.get_total_value(trump_suit, lead_card_suit))
        except ValueError as ex:
            return None

        return card

    def get_trump_cards(self, trump_suit):
        """
        Return all of the card sin my hand that are trumps.

        @attention tests written

        :param trump_suit: The suit of trump.
        :return: A list of cards.
        """
        cards = [card for card in self.hand if card.get_suit(trump_suit) == trump_suit]
        return cards

    def get_biggest_non_trump(self, trump_suit, lead_card_suit=Card.SUIT_NOSUIT) -> Optional[Card]:
        """
        Get the biggest non-trump card.

        @attention tests written

        :param trump_suit: The suit to be avoided as trump.
        :return: The biggest non-trump suit. In case of a tie, the first one encountered is returned.
        """
        try:
            card = max(filter(lambda a: a.get_suit(trump_suit) != trump_suit, self.hand),
                       key=lambda c: c.get_total_value(trump_suit, lead_card_suit))
        except ValueError as ex:
            return None

        return card

    def winning_card(self, trump_suit, tricks_played):
        """

        :param trump_suit:
        :param tricks_played:
        :return:
        """
        pass
