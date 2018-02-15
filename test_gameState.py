from unittest import TestCase
from Card import Card
from GameState import GameState
class TestGameState(TestCase):

    def setUp(self):
        self.game_state = GameState(0)
        self.game_state.state = GameState.TRICK_END
        self.game_state.trumps = Card.SUIT_DIAMONDS


    def test_calc_winnner(self):

        # No trumps
        self.game_state.lead_card = Card(Card.SUIT_HEARTS, Card.ACE)
        self.game_state.trick_cards = {
            0: Card(Card.SUIT_CLUBS, 10),
            1: Card(Card.SUIT_SPADES, Card.KING),
            2: Card(Card.SUIT_HEARTS, Card.ACE),
            3: Card(Card.SUIT_HEARTS, 9)
        }

        winner = self.game_state.calc_winner()
        self.assertEqual(winner, 2)

        # Right bower
        self.game_state.trick_cards = {
            0: Card(Card.SUIT_DIAMONDS, Card.JACK),
            1: Card(Card.SUIT_SPADES, Card.KING),
            2: Card(Card.SUIT_HEARTS, Card.ACE),
            3: Card(Card.SUIT_HEARTS, 9)
        }
        winner = self.game_state.calc_winner()
        self.assertEqual(winner, 0)

        # Left Bower winning
        self.game_state.trick_cards = {
            0: Card(Card.SUIT_HEARTS, Card.JACK),
            1: Card(Card.SUIT_SPADES, Card.KING),
            2: Card(Card.SUIT_HEARTS, Card.ACE),
            3: Card(Card.SUIT_HEARTS, 9)
        }
        winner = self.game_state.calc_winner()
        self.assertEqual(winner, 0)

        # Left Bower losing
        self.game_state.trick_cards = {
            0: Card(Card.SUIT_HEARTS, Card.JACK),
            1: Card(Card.SUIT_SPADES, Card.KING),
            2: Card(Card.SUIT_DIAMONDS, Card.JACK),
            3: Card(Card.SUIT_HEARTS, 9)
        }
        winner = self.game_state.calc_winner()
        self.assertEqual(winner, 2)

        # One trump no bowers
        self.game_state.trick_cards = {
            0: Card(Card.SUIT_HEARTS, Card.ACE),
            1: Card(Card.SUIT_SPADES, Card.KING),
            2: Card(Card.SUIT_DIAMONDS, 10),
            3: Card(Card.SUIT_HEARTS, 9)
        }

        winner = self.game_state.calc_winner()
        self.assertEqual(winner, 2)

        # Trump Battle
        self.game_state.trick_cards = {
            0: Card(Card.SUIT_DIAMONDS, Card.ACE),
            1: Card(Card.SUIT_DIAMONDS, Card.KING),
            2: Card(Card.SUIT_DIAMONDS, Card.JACK),
            3: Card(Card.SUIT_HEARTS, Card.JACK)
        }

        winner = self.game_state.calc_winner()
        self.assertEqual(winner, 2)

        self.game_state.lead_card = Card(Card.SUIT_DIAMONDS, Card.JACK)
        # failed test case
        self.game_state.trick_cards = {
            2: Card(Card.SUIT_DIAMONDS, Card.JACK),
            3: Card(Card.SUIT_DIAMONDS, Card.KING),
            0: Card(Card.SUIT_CLUBS, Card.ACE),
            1: Card(Card.SUIT_HEARTS, Card.KING)
        }
        self.game_state.trumps = Card.SUIT_HEARTS

        winner = self.game_state.calc_winner()
        self.assertEqual(winner, 2)

        self.game_state.lead_card = Card(Card.SUIT_DIAMONDS, Card.JACK)

        self.game_state.trumps = Card.SUIT_DIAMONDS
        self.game_state.trick_cards = {
            1: Card(Card.SUIT_DIAMONDS, Card.JACK),
            2: Card(Card.SUIT_DIAMONDS, 10),
            3: Card(Card.SUIT_HEARTS, Card.JACK),
            0: Card(Card.SUIT_DIAMONDS, 9)
        }

        winner = self.game_state.calc_winner()
        self.assertEqual(winner, 1)

        self.game_state.lead_card = Card(Card.SUIT_CLUBS, Card.QUEEN)
        self.game_state.trumps = Card.SUIT_HEARTS
        self.game_state.trick_cards = {
            3: Card(Card.SUIT_CLUBS, Card.QUEEN),
            0: Card(Card.SUIT_CLUBS, Card.JACK),
            1: Card(Card.SUIT_CLUBS, 9),
            2: Card(Card.SUIT_CLUBS, 10),
        }

        res = self.game_state.trick_cards[0].get_total_value(self.game_state.trumps, Card.SUIT_CLUBS)
        self.assertEqual(res, 11)
        winner = self.game_state.calc_winner()
        self.assertEqual(winner, 3)


        self.game_state.lead_card = Card(Card.SUIT_SPADES, Card.ACE)
        self.game_state.trumps = Card.SUIT_HEARTS
        self.game_state.trick_cards = {
            1: Card(Card.SUIT_SPADES, Card.ACE),
            2: Card(Card.SUIT_SPADES, Card.KING),
            3: Card(Card.SUIT_SPADES, 9),
            0: Card(Card.SUIT_SPADES, Card.JACK)
        }

        winner = self.game_state.calc_winner()
        self.assertEqual(winner, 1)