class Card(object):

    SUIT_NOSUIT = -1
    SUIT_SPADES = 0
    SUIT_HEARTS = 1
    SUIT_CLUBS = 2
    SUIT_DIAMONDS = 3

    COLOR_BLACK = 0 # Detrmined as SUIT_SPADES % 2 == 0 and SUIT_CLUBS % 2 == 0
    COLOR_RED = 1 # Determined as SUIT_SPADES % 2 == 1 and SUIT_CLUBS % 2 == 1

    ACE = 14
    KING = 13
    QUEEN = 12
    JACK = 11

    SUITS = [SUIT_SPADES, SUIT_HEARTS, SUIT_CLUBS, SUIT_DIAMONDS]
    VALUES = [9, 10, JACK, QUEEN, KING, ACE]

    def __init__(self, suit=None, value=None):
        if value < 9 or value > Card.ACE:
            raise ValueError("Card value cannot be larger than and ACE (9-13 Inclusive).")
        if suit < Card.SUIT_SPADES or suit > Card.SUIT_DIAMONDS:
            raise ValueError("Card Suit must be between 0 and 3 (inclusive)")

        self.suit = suit
        self.value = value

    def get_value(self) -> int:
        return self.value

    def get_total_value(self, trump_suit: int, lead_suit: int):
        color = self.get_color(self.suit)
        trump_color = self.get_color(trump_suit)

        ret_val = 0
        if self.suit == lead_suit and trump_suit != lead_suit:
            ret_val += self.value

        if color == trump_color:
            # We at least have the same color as trump. Lets determine if it's a jack
            if self.suit == trump_suit:
                if self.value == Card.JACK:
                    # We have the right bower
                    ret_val += 2000 + self.value
                else:
                    # We have a trump, but not the right bower
                    ret_val += 100 + self.value

            elif self.suit != trump_suit and self.value == Card.JACK:
                # We don't have the same suit, but the same color, and we have the Jack, This is the left bower.
                ret_val += 1000 + self.value


        return ret_val


    def get_color(self, suit: int) -> int:
        """
        Determine the color of the suit.

        This will also appropriately assign the trump suit to the left bower if this card
        is the left bower.

        The return values map to the constants Card.COLOR_BLACK and Card.COLOR_RED
        :param: trump_suit If set we will check against the trump suit to determine if our card is the left bower
        :return: 0 if the suit is black 1 if the suit is red.
        """
        return suit % 2

    def get_suit(self, trump_suit=None) -> int:
        if trump_suit is not None and self.value == Card.JACK:
            matching_suit = self.get_matching(trump_suit)
            if self.suit == matching_suit:
                return trump_suit
        return self.suit

    def get_raw_suit(self):
        return self.suit

    def set_value(self, new_val: int):
        self.value = new_val

    def set_suit(self, new_suit: int):
        self.suit = new_suit

    def get_value_str(self) -> str:
        if self.value == None:
            return "None"

        elif self.value == 9:
            return "9"

        elif self.value == 10:
            return "10"

        elif self.value == Card.JACK:
            return "J"

        elif self.value == Card.QUEEN:
            return "Q"

        elif self.value == Card.KING:
            return "K"

        elif self.value == Card.ACE:
            return "A"

        return "Unk"

    def get_matching(self, suit):
        if suit == Card.SUIT_CLUBS:
            return Card.SUIT_SPADES

        if suit == Card.SUIT_SPADES:
            return Card.SUIT_CLUBS

        if suit == Card.SUIT_HEARTS:
            return Card.SUIT_DIAMONDS

        if suit == Card.SUIT_DIAMONDS:
            return Card.SUIT_HEARTS

    def get_suit_str(self, short: bool=False) -> str:
        if (short):
            return self.suit_str(self.suit)
        else:
            return self.suit_str_long(self.suit)


    @staticmethod
    def suit_str(suit: int) -> str:
        if suit == Card.SUIT_SPADES:
            return "S"
        elif suit == Card.SUIT_DIAMONDS:
            return "D"
        elif suit == Card.SUIT_CLUBS:
            return "C"
        elif suit == Card.SUIT_HEARTS:
            return "H"

        return "Unk"

    @staticmethod
    def suit_str_long(suit: int) -> str:
        if suit == Card.SUIT_SPADES:
            return "SPADES"
        elif suit == Card.SUIT_DIAMONDS:
            return "DIAMONDS"
        elif suit == Card.SUIT_CLUBS:
            return "CLUBS"
        elif suit == Card.SUIT_HEARTS:
            return "HEARTS"


    def __repr__(self):
        return "{}{}".format(self.get_value_str(), self.get_suit_str(short=True))