from unittest import TestCase
from BasicPlayer import BasicPlayer
from enums import Teams
from Card import Card
from Player import Player
from GameState import GameState

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

        game_state = GameState(1)
        game_state.trumps = Card.SUIT_HEARTS
        game_state.lead_card = Card(Card.SUIT_HEARTS, 10)

        card = self.player.get_biggest_non_trump(Card.SUIT_HEARTS, game_state.lead_card, self.player.hand)

        self.assertEqual(card.value, Card.KING)
        self.assertEqual(card._suit, Card.SUIT_SPADES)

        game_state = GameState(1)
        game_state.trumps = Card.SUIT_SPADES
        game_state.lead_card = Card(Card.SUIT_HEARTS, 10)
        card = self.player.get_biggest_non_trump(Card.SUIT_SPADES, game_state.lead_card, self.player.hand)
        self.assertEqual(card.value, Card.ACE)
        self.assertEqual(card._suit, Card.SUIT_HEARTS)

        result = self.player.get_biggest_non_trump(Card.SUIT_SPADES, game_state.lead_card, [])
        self.assertIsNone(result)

    def test_get_trump_cards(self):

        game_state = GameState(1)
        game_state.trumps = Card.SUIT_HEARTS
        game_state.lead_card = Card(Card.SUIT_HEARTS, 10)
        cards = self.player.get_trump_cards(game_state.trumps, self.player.hand)
        self.assertEqual(len(cards), 3)

        self.assertEqual(cards[0], self.player.hand[2])
        self.assertEqual(cards[1], self.player.hand[3])
        self.assertEqual(cards[2], self.player.hand[4])

        cards = self.player.get_trump_cards(game_state.trumps, self.player.hand)
        self.assertEqual(len(cards), 3)

        game_state.trumps = Card.SUIT_CLUBS
        game_state.lead_card._suit = Card.SUIT_CLUBS
        cards = self.player.get_trump_cards(game_state.trumps, self.player.hand)
        self.assertEqual(len(cards), 1)

        # Test that even through the player has a trump card, he cannot play it
        # since the lead card is hearts and he must follow suit.
        game_state.lead_card._suit = Card.SUIT_HEARTS
        cards = self.player.get_trump_cards(game_state.trumps, game_state.get_valid_plays(self.player.hand))
        self.assertEqual(len(cards), 0)

    def test_find_lowest_card(self):
        game_state = GameState(1)
        game_state.trumps = Card.SUIT_SPADES
        game_state.lead_card = Card(Card.SUIT_HEARTS, 10)

        lowest_card = self.player.find_lowest_card(Card.SUIT_CLUBS, game_state.trumps,
                                                   game_state.get_valid_plays(self.player.hand))
        self.assertEqual(lowest_card.value, 9)
        self.assertEqual(lowest_card._suit, Card.SUIT_HEARTS)

        lowest_card = self.player.find_lowest_card(Card.SUIT_HEARTS, Card.SUIT_DIAMONDS,
                                                   game_state.get_valid_plays(self.player.hand))

        self.assertIsNone(lowest_card)  # The Jack of Diamonds that hte player has is really a Heart.

    def test_get_biggest_trump(self):
        lead_card = Card(Card.SUIT_SPADES, 10)
        biggest_trump = self.player.get_biggest_trump(Card.SUIT_HEARTS,
                                                      lead_card.get_suit(Card.SUIT_HEARTS), self.player.hand)

        self.assertEqual(biggest_trump.get_total_value(Card.SUIT_HEARTS, Card.SUIT_NOSUIT),
                         Card.JACK + Card.LEFT_BOWER_BONUS)
        self.assertEqual(biggest_trump.get_suit(Card.SUIT_HEARTS), Card.SUIT_HEARTS)

        biggest_trump = self.player.get_biggest_trump(Card.SUIT_HEARTS, lead_card.get_suit(Card.SUIT_HEARTS), [])
        self.assertIsNone(biggest_trump)

    def test_find_voidable_suits(self):
        game_state = GameState(1)
        game_state.trumps = Card.SUIT_SPADES
        game_state.lead_card = Card(Card.SUIT_SPADES, Card.ACE)

        self.player.hand = [
            Card(Card.SUIT_CLUBS, 10),
            Card(Card.SUIT_HEARTS, Card.ACE),
            Card(Card.SUIT_DIAMONDS, Card.JACK),
            Card(Card.SUIT_HEARTS, 9)
        ]

        voidable_suits = self.player.find_voidable_suits(
            game_state.trumps,
            game_state.get_valid_plays(self.player.hand)
        )
        self.assertEqual(2, len(voidable_suits))
        self.assertTrue(Card.SUIT_CLUBS in voidable_suits)
        self.assertTrue(Card.SUIT_DIAMONDS in voidable_suits)

        voidable_suits = self.player.find_voidable_suits(
            Card.SUIT_NOSUIT,
            game_state.get_valid_plays(self.player.hand)
        )

        self.assertEqual(2, len(voidable_suits))
        self.assertTrue(Card.SUIT_CLUBS in voidable_suits)
        self.assertTrue(Card.SUIT_DIAMONDS in voidable_suits)

    def test_num_offsuit_aces(self):
        self.player.hand = [
            Card(Card.SUIT_CLUBS, 10),
            Card(Card.SUIT_HEARTS, Card.ACE),
            Card(Card.SUIT_DIAMONDS, Card.JACK),
            Card(Card.SUIT_HEARTS, 9)
        ]

        game_state = GameState(1)
        game_state.trumps = Card.SUIT_SPADES
        game_state.lead_card = Card(Card.SUIT_SPADES, Card.ACE)

        num_offsuit_aces = self.player.num_offsuit_aces(
            game_state.trumps,
            game_state.get_valid_plays(self.player.hand)
        )
        self.assertEqual(1, num_offsuit_aces)

        num_offsuit_aces = self.player.num_offsuit_aces(
            Card.SUIT_HEARTS,
            game_state.get_valid_plays(self.player.hand)
        )

        self.assertEqual(0, num_offsuit_aces)

        num_offsuit_aces = self.player.num_offsuit_aces(
            Card.SUIT_NOSUIT,
            game_state.get_valid_plays(self.player.hand)
        )
        self.assertEqual(1, num_offsuit_aces)

    def test_has_card(self):

        self.assertTrue(self.player.has_card(10, Card.SUIT_CLUBS))
        self.assertTrue(self.player.has_card(Card.ACE, Card.SUIT_HEARTS))
        self.assertFalse(self.player.has_card(Card.ACE, Card.SUIT_CLUBS))
        self.assertTrue(self.player.has_card(Card.JACK, Card.SUIT_DIAMONDS))
        self.assertTrue(self.player.has_card(Card.JACK, Card.SUIT_DIAMONDS, Card.SUIT_DIAMONDS))

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
        top_card = Card(Card.SUIT_SPADES, Card.ACE)
        choice = self.player.make_bid_rnd_2(top_card)
        self.assertEqual(Card.SUIT_NOSUIT, choice)

        self.player.hand = [
            Card(Card.SUIT_CLUBS, Card.JACK),
            Card(Card.SUIT_SPADES, Card.KING),
            Card(Card.SUIT_HEARTS, Card.ACE),
            Card(Card.SUIT_SPADES, Card.JACK),
            Card(Card.SUIT_HEARTS, 9)
        ]
        top_card = Card(Card.SUIT_DIAMONDS, Card.ACE)
        choice = self.player.make_bid_rnd_2(top_card)
        self.assertEqual(Card.SUIT_SPADES, choice)

    def test_is_loaner(self):
        game_state = GameState(1)
        self.assertFalse(self.player.is_loaner(game_state))

    def test_get_smallest_winning_card(self):
        game_state = GameState(1)
        game_state.lead_card = Card(Card.SUIT_HEARTS, 10)
        game_state.trick_cards = [game_state.lead_card]
        game_state.trumps = Card.SUIT_HEARTS

        lead_card_suit = game_state.lead_card.get_suit(game_state.trumps)

        smallest_winning = self.player.smallest_winning_card(
            Card.SUIT_HEARTS,
            game_state.trick_cards,
            game_state.get_valid_plays(self.player.hand)
        )

        self.assertIsNotNone(smallest_winning)
        self.assertEqual(Card.SUIT_HEARTS, smallest_winning.get_suit(game_state.trumps))
        self.assertEqual(Card.ACE + Card.TRUMP_BONUS,
                         smallest_winning.get_total_value(game_state.trumps, lead_card_suit)
                         )

        game_state.lead_card = Card(Card.SUIT_HEARTS, Card.JACK)
        game_state.trick_cards = [game_state.lead_card]

        smallest_winning = self.player.smallest_winning_card(
            Card.SUIT_HEARTS,
            game_state.trick_cards,
            game_state.get_valid_plays(self.player.hand)
        )
        self.assertIsNone(smallest_winning)

    def test_make_move(self):
        pass

