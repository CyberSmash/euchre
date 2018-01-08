from unittest import TestCase
from Card import Card


class TestCard(TestCase):
    """
    def test_get_total_value(self):
        # Test the right bower
        c = Card(Card.SUIT_CLUBS, Card.JACK)
        card_value = c.get_total_value(Card.SUIT_CLUBS, Card.SUIT_DIAMONDS)
        self.assertEqual(card_value, 2000 + Card.JACK)

        # Test left bower
        card_value = c.get_total_value(Card.SUIT_SPADES, Card.SUIT_DIAMONDS)
        self.assertEqual(card_value, 1000 + Card.JACK)

        # Test that we get only the value, if the lead suit is the same.
        c.suit = c.SUIT_DIAMONDS
        card_value = c.get_total_value(Card.SUIT_SPADES, Card.SUIT_DIAMONDS)
        self.assertEqual(card_value, c.value)

        # Test that we get no value if we didn't follow the lead suit
        c.suit = c.SUIT_DIAMONDS
        card_value = c.get_total_value(Card.SUIT_SPADES, Card.SUIT_HEARTS)
        self.assertEqual(card_value, 0)

        # Test that a non-bower trump card gets a little bump
        c.set_suit(Card.SUIT_SPADES)
        c.set_value(Card.QUEEN)
        card_value = c.get_total_value(Card.SUIT_SPADES, Card.SUIT_DIAMONDS)
        self.assertEqual(card_value, 100 + Card.QUEEN)

        # Test that a a trump still is a trump value
        c.set_suit(Card.SUIT_SPADES)
        c.set_value(Card.QUEEN)
        card_value = c.get_total_value(Card.SUIT_SPADES, Card.SUIT_SPADES)
        self.assertEqual(card_value, 100 + Card.QUEEN)
"""
    def test_get_color(self):
        c = Card(Card.SUIT_CLUBS, Card.JACK)
        color = c.get_color(c.suit)
        self.assertEqual(color, Card.COLOR_BLACK)

        c.suit = Card.SUIT_SPADES
        color = c.get_color(c.suit)
        self.assertEqual(color, Card.COLOR_BLACK)

        c.suit = Card.SUIT_DIAMONDS
        color = c.get_color(c.suit)
        self.assertEqual(color, Card.COLOR_RED)

        c.suit = Card.SUIT_HEARTS
        color = c.get_color(c.suit)
        self.assertEqual(color, Card.COLOR_RED)

    def test_get_suit(self):
        newCard = Card(Card.SUIT_CLUBS, Card.JACK)

        self.assertEqual(newCard.get_suit(Card.SUIT_CLUBS), Card.SUIT_CLUBS)
        self.assertEqual(newCard.get_suit(Card.SUIT_SPADES), Card.SUIT_SPADES)
        self.assertEqual(newCard.get_suit(), Card.SUIT_CLUBS)

        self.assertEqual(newCard.get_suit(Card.SUIT_DIAMONDS), Card.SUIT_CLUBS)
        self.assertEqual(newCard.get_suit(Card.SUIT_HEARTS), Card.SUIT_CLUBS)

        newCard = Card(Card.SUIT_CLUBS, Card.KING)
        self.assertEqual(newCard.get_suit(Card.SUIT_CLUBS), Card.SUIT_CLUBS)
        self.assertEqual(newCard.get_suit(Card.SUIT_SPADES), Card.SUIT_CLUBS)
        self.assertEqual(newCard.get_suit(), Card.SUIT_CLUBS)

        self.assertEqual(newCard.get_suit(Card.SUIT_DIAMONDS), Card.SUIT_CLUBS)
        self.assertEqual(newCard.get_suit(Card.SUIT_HEARTS), Card.SUIT_CLUBS)
