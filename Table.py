from Player import Player
from Deck import Deck
from GameState import GameState
from random import randrange
from Card import Card

from RandomPlayer import RandomPlayer
class Table(object):

    TEAM_A = 0
    TEAM_B = 1

    def __init__(self, player_type: type(Player)):

        self.players = [player_type(0, Table.TEAM_A, "Player-0"),
                        player_type(1, Table.TEAM_B, "Player-1"),
                        player_type(2, Table.TEAM_A, "Player-2"),
                        player_type(3, Table.TEAM_B, "Player-3")]

        self.scores = [0, 0] # Indexed using TEAM_A and TEAM_B

        self.deck = Deck()
        self.game_state = GameState()

        self.current_dealer = randrange(0, 3)
        self.players[self.current_dealer].set_dealer()

        self.current_player_turn = (self.current_dealer + 1) % len(self.players)

        self.game_state.set_state(GameState.DEAL)

        # This is set when the first card of the trick is being played. It's false when it's not the first card.
        self.tick_begin = True

    def next_player(self):
        """
        Increment the current player by one spot.
        :return: Nothing.
        """
        self.current_player_turn = (self.current_player_turn + 1) % len(self.players)

    def step_game(self):
        """
        Progress the game state by one step.
        Dealing is one step complete step
        Bidding goes in separate steps

        :return:
        """

        if self.game_state.is_deal():
            self.deal_cards()
            self.game_state.set_top_card(self.deck.deal_one())
            self.game_state.set_state(GameState.BIDDING_RND_1)
            return GameState.DEAL

        elif self.game_state.is_bidding():
            self.bid_step()

        elif self.game_state.is_trick():
            self.trick_step()

        elif self.game_state.is_end():
            raise Exception("Game State not yet implemented.")
        else:
            raise Exception("Step into an unknown game state {}".format(self.game_state.get_state()))


    def trick_step(self):
        current_player = self.get_current_player()
        dealer = self.get_dealer()

        if self.game_state.state == GameState.TRICK_START:
            # TODO: How can we enforce that this player actually has this card?
            card = current_player.make_move(self.game_state)
            if not self.game_state.is_valid_play(card, current_player.hand):
                raise Exception("{} attempted to play {} However this is an "
                                "invalid card to play.".format(current_player.name, card))

            self.game_state.trick_cards[current_player.player_num] = card

            if current_player == dealer:
                self.game_state.set_state(GameState.TRICK_END)

            self.next_player()

        if self.game_state.state == GameState.TRICK_END:
            winner_id = self.game_state.calc_winner()
            self.game_state.reset_trick()

    def bid_step(self):
        if self.game_state.get_state() == GameState.BIDDING_RND_1:
            self.handle_bidding_rnd_1()
        elif self.game_state.get_state() == GameState.BIDDING_RND_2:
            self.handle_bidding_rnd_2()


    def handle_bidding_rnd_1(self):
        current_player = self.get_current_player()
        dealer = self.get_dealer()

        bid = current_player.make_bid_rnd_1(self.game_state)

        if bid == Player.ORDER_UP:
            self.handle_bid(current_player, dealer)
            self.game_state.set_state(GameState.TRICK_START)
            self.reset_current_player()

        elif bid == Player.PASS:
            print("Player {}: Passed.".format(current_player.name))
            if current_player == dealer:
                self.game_state.set_state(GameState.BIDDING_RND_2)
            self.next_player()
        else:
            raise ValueError("Invalid bid from {}".format(current_player.name))


    def handle_bid(self, current_player: Player, dealer: Player):
        """
        The current player has decided to order up a card. This function handles that logic.

        :param current_player: The current player object
        :param dealer: The dealer.
        :return: Nothing.
        """
        dealer.discard(self.game_state)
        top_card = self.game_state.give_top_card()
        dealer.receive_card([top_card])

        self.game_state.set_trumps(top_card.get_suit())
        print("Player {}: Ordered up the {}. Trumps is now {}".format(self.current_player_turn,
                                                                      top_card, top_card.get_suit_str()))
        self.handle_loaner(current_player)




    def handle_bidding_rnd_2(self):
        """
        In this bidding round each player has the option to announce trumps as long
        as it's not the card that was already optioned to be trumps. If all players decline to call
        trumps, then this round is dead, and we start again from a new deal with the same dealer.
        :return:
        """
        current_player = self.get_current_player()
        dealer = self.get_dealer()

        bid = current_player.make_bid_rnd_2(self.game_state)
        if bid != Card.SUIT_NOSUIT:
            self.handle_make(current_player, bid)
            self.game_state.set_state(GameState.TRICK_START)
            self.game_state.bidding_team = current_player.team_id
            self.reset_current_player()

        if bid == Card.SUIT_NOSUIT:
            print("{} has decided not to announce a Trumps".format(current_player.name))
            if current_player == dealer:
                print("The deal has been called Dead. It will be re-dealt.")
                self.dead_deal()
            else:
                self.next_player()

    def handle_make(self, current_player: Player, selected_suit: int):
        """
        Handle the player wanting to make the suit.

        :param current_player: The current player object that wanted to make.
        :param selected_suit: The suit that is the selected by the current player.
        :return:
        """
        if selected_suit == self.game_state.top_card.suit:
            raise ValueError("The player {} attempted to make a suit that is no longer legal in the second round"
                             "of bidding. NOTE: This error needs to be passed back to the "
                             "player somehow.".format(current_player.name))

        if selected_suit not in Card.SUITS:
            raise ValueError("{} tried to make a suit that doesn't exist {}. NOTE: This needs to be passed back"
                             "to the player somehow.".format(current_player.name, selected_suit))

        print("{} has set {} as Trumps.".format(current_player.name, selected_suit))
        self.handle_loaner(current_player)


    def handle_loaner(self, current_player: Player) -> bool:
        """
        Determine if a player is going alone and if so, set up the player and teammate thusly.

        :param current_player: The current player
        :return: True if the player is going to go alone. False otherwise.
        """
        # Determine if the player wants to go alone.
        is_loaner = current_player.is_loaner(self.game_state)
        if not is_loaner:
            return False

        # The player wants to go alone.
        teammate = self.get_player_teammate(current_player)
        teammate.sit_out()

        current_player.is_loaner(self.game_state)
        print("{} has decided to go alone. {} will sit out of this round.".format(current_player.name, teammate.name))
        return True


    def dead_deal(self):
        """
        In this case, all players passed on the face up card, and no one
        wanted to call trumps. This calls for a reshuffle, and re-deal.
        :return:
        """
        for player in self.players:
            player.clear_hand()
            self.deck.init_deck()
        self.game_state.set_state(GameState.DEAL)
        self.current_player_turn = (self.current_dealer + 1) % len(self.players)


    def reset_current_player(self):
        """
        Helper function that sets the current player to the player to the left of the dealer.
        :return: Nothing
        """
        self.current_player_turn = (self.current_dealer + 1) % len(self.players)


    def get_dealer(self) -> Player:
        """
        Get the current Dealer player object.
        :return: A player object.
        """
        return self.players[self.current_dealer]


    def get_current_player(self) -> Player:
        """
        Get the player who's turn it is.
        :return: The current player Player object.
        """
        return self.players[self.current_player_turn]


    def get_player_teammate(self, current_player: Player) -> Player:
        """
        Get the teammate object of the current player.

        :param current_player: The player who's teammate you want to retrieve
        :return: The teammate Player object.
        """

        for player in self.players:
            if current_player.team_id == player.team_id and current_player.player_num != player.player_num:
                return player

        raise Exception("Cannot find second player with the Team ID {} and without the player number of {}".format(
            current_player.team_id, current_player.player_num
        ))


    def move_dealer(self):
        """
        Pass the deal to the next dealer.
        :return:
        """
        self.current_dealer = (self.current_dealer + 1) % len(self.players)


    def deal_cards(self):
        two_cards = True
        # Deal two rounds
        for x in range(0, 2):
            two_cards = not two_cards
            for idx in range(0, len(self.players)):
                p = ((self.current_dealer + 1) + idx) % len(self.players)
                cards = None
                if two_cards:
                    cards = self.deck.deal(2)
                elif not two_cards:
                    cards = self.deck.deal(3)

                if cards == None:
                    raise Exception("While dealing I ran out of cards...")

                two_cards = not two_cards

                self.players[p].receive_card(cards)


