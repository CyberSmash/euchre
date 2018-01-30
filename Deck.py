from Card import Card
from secrets import randbelow, choice

class Deck(object):

    def __init__(self):
        self.deck = list()
        self.init_deck()

    def init_deck(self):
        for suit in Card.SUITS:
            for val in Card.VALUES:
                self.deck.append(Card(suit=suit, value=val))

    def shuffle_deck(self):
        self.deck = list()
        self.init_deck()

    def deal(self, num: int=1) -> list:
        """
        Returns a list of requested cards.
        Cards are then removed from the deck.
        :param num: The number of cards to return
        :return: A list containing the requested number of cards on success. None if the deck is empty.
        """
        if num == 0:
            raise ValueError("Cannot deal zero cards.")

        cards = list()
        if self.deck_is_empty(num):
            return list()

        for x in range(0, num):
            card = None

            # Loop until we have a valid card.
            idx = 0
            card = None
            while card is None:
                card = choice(self.deck)

            self.deck[idx] = None
            cards.append(card)

        return cards

    def deal_one(self) -> Card:
        return self.deal(1)[0]

    def deck_is_empty(self, minimum: int=1) -> bool:
        """
        Determine if the deck is empty or has at least minimum cards.

        :param minimum: The minimum number of cards that the deck must have.
        :return: True if the deck is empty, or doesn't have the required cards. False otherwise.
        """

        if minimum == 0:
            raise ValueError("There will always be at least zero cards available.")

        count = 0
        for card in self.deck:
            if card is not None:
                count += 1
            if count >= minimum:
                return False

        return True