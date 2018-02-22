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


        cards = self.player.get_trump_cards(Card.SUIT_HEARTS)
        self.assertEqual(len(cards), 3)

        cards = self.player.get_trump_cards(Card.SUIT_CLUBS)
        self.assertEqual(len(cards), 1)

    def test_find_lowest_card(self):
        self.player.hand = [
            Card(Card.SUIT_CLUBS, 10),
            Card(Card.SUIT_SPADES, Card.KING),
            Card(Card.SUIT_HEARTS, Card.ACE),
            Card(Card.SUIT_DIAMONDS, Card.JACK),
            Card(Card.SUIT_HEARTS, 9)
        ]

        lowest_card = self.player.find_lowest_card(Card.SUIT_CLUBS)
        self.assertEqual(lowest_card.value, 9)
        self.assertEqual(lowest_card.suit, Card.SUIT_HEARTS)

    def test_get_biggest_trump(self):
        self.player.hand = [
            Card(Card.SUIT_CLUBS, 10),
            Card(Card.SUIT_SPADES, Card.KING),
            Card(Card.SUIT_HEARTS, Card.ACE),
            Card(Card.SUIT_DIAMONDS, Card.JACK),
            Card(Card.SUIT_HEARTS, 9)
        ]

        biggest_trump = self.player.get_biggest_trump(Card.SUIT_HEARTS, Card.SUIT_NOSUIT)
        self.assertEqual(biggest_trump.get_total_value(Card.SUIT_HEARTS, Card.SUIT_NOSUIT), Card.JACK + Card.LEFT_BOWER_BONUS)
        self.assertEqual(biggest_trump.get_suit(Card.SUIT_HEARTS), Card.SUIT_HEARTS)

    def test_find_voidable_suits(self):
        self.player.hand = [
            Card(Card.SUIT_CLUBS, 10),
            Card(Card.SUIT_SPADES, Card.KING),
            Card(Card.SUIT_HEARTS, Card.ACE),
            Card(Card.SUIT_DIAMONDS, Card.JACK),
            Card(Card.SUIT_HEARTS, 9)
        ]

        voidable_suits = self.player.find_voidable_suits(Card.SUIT_DIAMONDS)
        self.assertEqual(2, len(voidable_suits))
        self.assertTrue(Card.SUIT_CLUBS in voidable_suits)
        self.assertTrue(Card.SUIT_SPADES in voidable_suits)

        voidable_suits = self.player.find_voidable_suits(Card.SUIT_HEARTS)
        self.assertEqual(2, len(voidable_suits))
        self.assertTrue(Card.SUIT_SPADES in voidable_suits)
        self.assertTrue(Card.SUIT_CLUBS in voidable_suits)

        voidable_suits = self.player.find_voidable_suits(Card.SUIT_NOSUIT)
        self.assertEqual(3, len(voidable_suits))
        self.assertTrue(Card.SUIT_SPADES in voidable_suits)
        self.assertTrue(Card.SUIT_CLUBS in voidable_suits)
        self.assertTrue(Card.SUIT_DIAMONDS in voidable_suits)

    def test_num_offsuit_aces(self):
        self.player.hand = [
            Card(Card.SUIT_CLUBS, 10),
            Card(Card.SUIT_SPADES, Card.KING),
            Card(Card.SUIT_HEARTS, Card.ACE),
            Card(Card.SUIT_DIAMONDS, Card.JACK),
            Card(Card.SUIT_HEARTS, 9)
        ]

        num_offsuit_aces = self.player.num_offsuit_aces(Card.SUIT_DIAMONDS)
        self.assertEqual(1, num_offsuit_aces)
