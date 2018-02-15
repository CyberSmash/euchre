from unittest import TestCase
from BasicPlayer import BasicPlayer
from enums import Teams
from Card import Card

class TestBasicPlayer(TestCase):

    def setUp(self):
        self.player = BasicPlayer(0, 0, "player-0")

    def tearDown(self):
        pass

    def test_get_biggest_non_trump(self):
        self.player.hand = [
            Card(Card.SUIT_CLUBS, 10),
            Card(Card.SUIT_SPADES, Card.KING),
            Card(Card.SUIT_HEARTS, Card.ACE),
            Card(Card.SUIT_DIAMONDS, Card.JACK),
            Card(Card.SUIT_HEARTS, 9)
        ]

        card = self.player.get_biggest_non_trump(Card.SUIT_HEARTS)
        self.assertEqual(card.value, self.player.hand[1].value)
        self.assertEqual(card.suit, self.player.hand[1].suit)

        card = self.player.get_biggest_non_trump(Card.SUIT_SPADES)
        self.assertEqual(card.value, Card.ACE)
        self.assertEqual(card.suit, Card.SUIT_HEARTS)

    def test_get_trump_cards(self):
        self.player.hand = [
            Card(Card.SUIT_CLUBS, 10),
            Card(Card.SUIT_SPADES, Card.KING),
            Card(Card.SUIT_HEARTS, Card.ACE),
            Card(Card.SUIT_DIAMONDS, Card.JACK),
            Card(Card.SUIT_HEARTS, 9)
        ]

        cards = self.player.get_trump_cards(Card.SUIT_HEARTS)
        self.assertEqual(len(cards), 3)

        self.assertEqual(cards[0], self.player.hand[2])
        self.assertEqual(cards[1], self.player.hand[3])
        self.assertEqual(cards[2], self.player.hand[4])