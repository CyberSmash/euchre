from unittest import TestCase
from BasicPlayer import BasicPlayer
from enums import Teams
from Card import Card
from Player import Player


class TestBasicPlayer(TestCase):

    def setUp(self):
        self.player = BasicPlayer(0, 0, "player-0")
        self.player.hand = [
            Card(Card.SUIT_CLUBS, 10),
            Card(Card.SUIT_SPADES, Card.KING),
            Card(Card.SUIT_HEARTS, Card.ACE),
            Card(Card.SUIT_DIAMONDS, Card.JACK),
            Card(Card.SUIT_HEARTS, 9)
        ]

    def tearDown(self):
        pass

    def test_get_biggest_non_trump(self):

        card = self.player.get_biggest_non_trump(Card.SUIT_HEARTS)
        self.assertEqual(card.value, self.player.hand[1].value)
        self.assertEqual(card._suit, self.player.hand[1]._suit)

        card = self.player.get_biggest_non_trump(Card.SUIT_SPADES)
        self.assertEqual(card.value, Card.ACE)
        self.assertEqual(card._suit, Card.SUIT_HEARTS)

    def test_get_trump_cards(self):

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

        lowest_card = self.player.find_lowest_card(Card.SUIT_CLUBS)
        self.assertEqual(lowest_card.value, 9)
        self.assertEqual(lowest_card._suit, Card.SUIT_HEARTS)

    def test_get_biggest_trump(self):

        biggest_trump = self.player.get_biggest_trump(Card.SUIT_HEARTS, Card.SUIT_NOSUIT)
        self.assertEqual(biggest_trump.get_total_value(Card.SUIT_HEARTS, Card.SUIT_NOSUIT), Card.JACK + Card.LEFT_BOWER_BONUS)
        self.assertEqual(biggest_trump.get_suit(Card.SUIT_HEARTS), Card.SUIT_HEARTS)

    def test_find_voidable_suits(self):

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

        num_offsuit_aces = self.player.num_offsuit_aces(Card.SUIT_DIAMONDS)
        self.assertEqual(1, num_offsuit_aces)

        num_offsuit_aces = self.player.num_offsuit_aces(Card.SUIT_HEARTS)
        self.assertEqual(0, num_offsuit_aces)

        num_offsuit_aces = self.player.num_offsuit_aces(Card.SUIT_NOSUIT)
        self.assertEqual(1, num_offsuit_aces)

    def test_has_card(self):

        self.assertEqual(True, self.player.has_card(10, Card.SUIT_CLUBS))
        self.assertEqual(True, self.player.has_card(Card.ACE, Card.SUIT_HEARTS))
        self.assertEqual(False, self.player.has_card(Card.ACE, Card.SUIT_CLUBS))
        self.assertEqual(True, self.player.has_card(Card.JACK, Card.SUIT_DIAMONDS))
        self.assertEqual(True, self.player.has_card(Card.JACK, Card.SUIT_DIAMONDS, Card.SUIT_DIAMONDS))

    def test_would_have_left_bower(self):

        top_card = Card(Card.SUIT_CLUBS, Card.ACE)
        self.assertEqual(False, self.player.would_have_left_bower(top_card))

        top_card = Card(Card.SUIT_HEARTS, Card.ACE)
        self.assertEqual(True, self.player.would_have_left_bower(top_card))

        top_card = Card(Card.SUIT_DIAMONDS, Card.ACE)
        self.assertEqual(False, self.player.would_have_left_bower(top_card))

    def test_would_have_right_bower(self):

        top_card = Card(Card.SUIT_CLUBS, Card.ACE)
        self.assertEqual(False, self.player.would_have_right_bower(top_card))

        top_card = Card(Card.SUIT_DIAMONDS, 10)
        self.assertEqual(True, self.player.would_have_right_bower(top_card))

        top_card = Card(Card.SUIT_HEARTS, 10)
        self.assertEqual(False, self.player.would_have_right_bower(top_card))

    def test_count_suit(self):
        num = self.player.count_suit(Card.SUIT_HEARTS)
        self.assertEqual(2, num)

        num = self.player.count_suit(Card.SUIT_SPADES)
        self.assertEqual(1, num)

    def test_calc_hand_strength(self):
        top_card = Card(Card.SUIT_SPADES, 10)
        strength = self.player.calc_hand_strength(top_card)
        self.assertEqual(3, strength)

        top_card = Card(Card.SUIT_HEARTS, 10)
        strength = self.player.calc_hand_strength(top_card)
        self.assertEqual(6, strength)

    def test_make_bid_rnd_1(self):
        top_card = Card(Card.SUIT_SPADES, 10)
        result = self.player.make_bid_rnd_1(top_card)
        self.assertEqual(Player.PASS, result)

        top_card = Card(Card.SUIT_HEARTS, 10)
        result = self.player.make_bid_rnd_1(top_card)
        self.assertEqual(Player.PASS, result)

        self.player.hand[-1] = Card(Card.SUIT_HEARTS, Card.JACK)
        result = self.player.make_bid_rnd_1(top_card)
        self.assertEqual(Player.ORDER_UP, result)

    def test_discard(self):
        discard = self.player.discard(Card.SUIT_SPADES)
        self.assertEqual(Card.SUIT_CLUBS, discard.get_suit(Card.SUIT_SPADES))
        self.assertEqual(10, discard.get_value())

        # put the discard card back into the players hand.
        self.player.hand.append(discard)

        discard = self.player.discard(Card.SUIT_CLUBS)
        self.assertEqual(Card.SUIT_DIAMONDS, discard.get_suit(Card.SUIT_CLUBS))
        self.assertFalse(discard in self.player.hand)
        self.assertEqual(4, len(self.player.hand))

        # Test that the player cannot void a suit.
        self.player.hand = [
            Card(Card.SUIT_SPADES, 10),
            Card(Card.SUIT_SPADES, Card.KING),
            Card(Card.SUIT_HEARTS, Card.ACE),
            Card(Card.SUIT_SPADES, Card.JACK),
            Card(Card.SUIT_HEARTS, 9)
        ]

        discard = self.player.discard(Card.SUIT_DIAMONDS)
        self.assertEqual(Card.SUIT_HEARTS, discard.get_suit(Card.SUIT_DIAMONDS))
        self.assertEqual(9, discard.value)

    def test_make_bid_rnd_2(self):
        pass
