from unittest import TestCase
from Card import Card
from GameState import GameState
class TestGameState(TestCase):

    def setUp(self):
        self.game_state = GameState()
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