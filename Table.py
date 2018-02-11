from Player import Player
from Deck import Deck
from GameState import GameState
from Card import Card
import logging
from enum import Enum
import EuchreDatabase
from enums import GameType
from enums import Teams

class Table(object):

    def __init__(self, player_type: type(Player), game_id: int, game_type: GameType=GameType.PROGRESSIVE):

        self.players = [player_type(0, Teams.TEAM_A, "Player-0"),
                        player_type(1, Teams.TEAM_B, "Player-1"),
                        player_type(2, Teams.TEAM_A, "Player-2"),
                        player_type(3, Teams.TEAM_B, "Player-3")]

        self.game_type = game_type

        self.scores = [0, 0]        # Indexed using TEAM_A and TEAM_B
        self.tricks_won = [0, 0]    # Indexed using TEAM_A and TEAM_B

        self.deck = Deck()
        self.game_state = GameState(game_id)

        self.players[self.game_state.current_dealer].set_dealer()

        self.current_player_turn = (self.game_state.current_dealer + 1) % len(self.players)

        self.game_state.set_state(GameState.GAME_START)

        self.loaner_team = None
        self.loaner_player = None

        self.trick_obj = None

    def step_game(self):
        """
        Progress the game state by one step.
        Dealing is one step complete step
        Bidding goes in separate steps

        :return:
        """

        if self.game_state.is_game_start():
            self.handle_game_start()

        elif self.game_state.is_deal():
            self.handle_deal()

        elif self.game_state.is_bidding():
            self.bid_step()

        elif self.game_state.is_hand_begin():
            self.hand_begin()

        elif self.game_state.is_trick_start():
            self.handle_trick_start()

        elif self.game_state.is_trick_middle():
            self.trick_middle()

        elif self.game_state.is_trick_end():
            self.handle_trick_end()

        elif self.game_state.is_hand_end():
            self.handle_hand_end()

        elif self.game_state.is_end():
            self.handle_game_end()

    def handle_game_start(self):
        """
        This is a placeholder for the beginning of a game. The entire state machine starts here.

        :return:
        """

        self.game_state.num_hands = 0
        self.game_state.set_state(GameState.DEAL)
        EuchreDatabase.start_game(self.game_state, self.players, self.game_type)

    def handle_deal(self):
        """
        This function handles the dealing of the cards. It is where
        all play of a hand begins.

        :return:
        """

        logging.info("Dealer is player {}".format(self.game_state.current_dealer))
        self.deck.shuffle_deck()
        self.deal_cards()
        self.game_state.set_top_card(self.deck.deal_one())
        self.reset_current_player() # ensure the first player is to the left of the dealer.
        EuchreDatabase.record_deal(self.game_state, self.players)
        self.game_state.set_state(GameState.BIDDING_RND_1)

    def hand_begin(self):
        """
        This is the logic that controls what happens at the beginning of a new hand.
        :return:
        """
        self.reset_current_player() # Set up so that we play with the next player being to the left of the dealer.
        self.deck.shuffle_deck()
        self.game_state.set_state(GameState.TRICK_START)

    def handle_trick_start(self):
        """
        Played when the trick starts

        :return:
        """
        logging.info("Starting trick #{}".format(self.game_state.trick_num))
        # In this case, this would be the first trick of the hand. Get the player to the left of the dealer.
        current_player = self.get_current_player()
        while current_player.is_sitting_out():
            self.next_player()
            current_player = self.get_current_player()

        # reset the lead player.
        self.game_state.lead_player = current_player

        card = current_player.make_move(self.game_state)
        if not self.game_state.is_valid_play(card, current_player.hand):
            raise ValueError("{} chose an invalid card to play. {}".format(current_player.name, card))

        self.game_state.lead_player = current_player
        self.game_state.lead_card = card

        EuchreDatabase.record_trick(card, current_player, self.game_state.trick_num)
        self.game_state.set_state(GameState.TRICK_MIDDLE)
        self.next_player()  # Set up the next state so that it will have a valid player.

    def trick_middle(self):
        """
        Perform all tricks other than the lead trick.

        :return: Nothing.
        """
        current_player = self.get_current_player()

        if current_player == self.game_state.lead_player:
            self.game_state.set_state(GameState.TRICK_END)
        else:
            self.player_move(current_player)
            self.next_player()

    def handle_trick_end(self):
        """
        The end of the trick, after all players have played.

        We need to decide who the winner is, assign them as the next lead
        add their score to their hand score, then setup for the next trick.

        :return:
        """
        winner_id = self.game_state.calc_winner()

        # Find the winner ID in the array. They aren't necessarally the same.
        for num, player in enumerate(self.players):
            if player.player_num == winner_id:
                logging.info("{} Won this trick".format(player.name))
                self.game_state.lead_player = player
                self.current_player_turn = num
                player.hand_score += 1
                self.tricks_won[player.team_id] += 1
                EuchreDatabase.record_trick_end(player.team_id, self.game_state.trick_num)
                break

        self.game_state.reset_trick()
        self.game_state.trick_num += 1

        if self.game_state.trick_num >= 5:
            self.game_state.trick_num = 0
            self.game_state.set_state(GameState.HAND_END)
        else:
            self.game_state.set_state(GameState.TRICK_START)

    def handle_hand_end(self):
        # Determine the winner
        defending_team = self.game_state.defending_team
        bidding_team = self.game_state.bidding_team

        if self.tricks_won[bidding_team] == 3 or self.tricks_won[bidding_team] == 4:
            # Whether the bidding team goes alone or not, if they get 3 or 4 tricks they only get a point.
            self.scores[bidding_team] += 1
            EuchreDatabase.record_hand_score(bidding_team, 1, self.tricks_won[Teams.TEAM_A],
                                             self.tricks_won[Teams.TEAM_B])

        elif self.tricks_won[bidding_team] == 5: # bidding team gets 5 points
            if self.loaner_team is not None and bidding_team == self.loaner_team: # 5 points, plus loaner
                self.scores[bidding_team] += 4
                EuchreDatabase.record_hand_score(bidding_team, 4, self.tricks_won[Teams.TEAM_A],
                                                 self.tricks_won[Teams.TEAM_B])
            else:  # 5 points, no loaner
                self.scores[bidding_team] += 2
                EuchreDatabase.record_hand_score(bidding_team, 2, self.tricks_won[Teams.TEAM_A],
                                                 self.tricks_won[Teams.TEAM_B])

        elif self.tricks_won[defending_team] >= 3:
            self.scores[defending_team] += 2
            EuchreDatabase.record_hand_score(defending_team, 2, self.tricks_won[Teams.TEAM_A],
                                             self.tricks_won[Teams.TEAM_B])

        logging.info("The defending(team {}) team won {} tricks.".format(defending_team, self.tricks_won[defending_team]))
        logging.info("The bidding team(team {}) won {} tricks.".format(bidding_team, self.tricks_won[bidding_team]))
        logging.info("The Score is now: TEAM A: {} to TEAM B: {}".format(self.scores[Teams.TEAM_A],
                                                                         self.scores[Teams.TEAM_B]))

        # Reset the trick scores
        self.tricks_won = [0, 0]

        # This must happen before move_dealer or the correct dealer will not get set.
        for player in self.players:
            player.reset()

        self.game_state.num_hands += 1
        self.loaner_team = None
        self.loaner_player = None
        self.move_dealer()
        self.game_state.trick_num = 0 # @todo: This should be handled by a reset function in game state, not here.

        if self.game_type == GameType.TRADITIONAL and (self.scores[Teams.TEAM_A] >= 10 or
                                                       self.scores[Teams.TEAM_B] >= 10):
            self.game_state.set_state(GameState.GAME_END)

        elif self.game_type == GameType.PROGRESSIVE and self.game_state.num_hands >= 8:
            self.game_state.set_state(GameState.GAME_END)

        else:
            self.game_state.set_state(GameState.DEAL)

    def player_move(self, current_player: Player):
        """
        Helper function to get a move from a player.

        Provides validation of the move.

        :param current_player: The player to make a move.
        :return: Nothing
        :raises: Exception if the played card is invalid.
        """
        # TODO: How can we enforce that this player actually has this card?
        card = current_player.make_move(self.game_state)
        if not self.game_state.is_valid_play(card, current_player.hand):
            raise Exception("{} attempted to play {} However this is an "
                            "invalid card to play.".format(current_player.name, card))

        self.game_state.trick_cards[current_player.player_num] = card
        EuchreDatabase.record_trick(card, current_player, self.game_state.trick_num)

    def bid_step(self):
        """
        Step Through the bidding state.

        This is the main router function between BIDDING_RND_1 and BIDDING_RND 2.

        :return: Nothing.
        """
        if self.game_state.get_state() == GameState.BIDDING_RND_1:
            self.handle_bidding_rnd_1()
        elif self.game_state.get_state() == GameState.BIDDING_RND_2:
            self.handle_bidding_rnd_2()

    def handle_bidding_rnd_1(self):
        """
        Perform all logic necessary for bidding round one.

        :return: Nothing.
        :raises: ValueError if a player attempts to bid something other than ORDER_UP or PASS.
        """
        current_player = self.get_current_player()
        dealer = self.get_dealer()

        bid = current_player.make_bid_rnd_1(self.game_state)

        if bid == Player.ORDER_UP:
            self.handle_bid(current_player, dealer)
            self.reset_current_player()
            self.game_state.bidding_team = current_player.team_id
            self.game_state.defending_team = (current_player.team_id + 1) % 2
            self.game_state.set_state(GameState.TRICK_START)
            EuchreDatabase.record_trump(self.game_state, self.game_state.top_card.get_suit(), 1, current_player,
                                        self.game_state.top_card)
        elif bid == Player.PASS:
            logging.info("Player {}: Passed.".format(current_player.name))
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
        self.game_state.top_card = self.game_state.give_top_card()
        dealer.receive_card([self.game_state.top_card])

        logging.info("Player {}: Ordered up the {}. Trumps is now {}".format(self.current_player_turn,
                                                                             self.game_state.top_card,
                                                                             self.game_state.top_card.get_suit_str()))
        self.game_state.set_trumps(self.game_state.top_card.get_suit())

        is_loaner = self.handle_loaner(current_player)
        if is_loaner:
            self.loaner_team = current_player.team_id
            self.loaner_player = current_player

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
            self.game_state.set_trumps(bid)
            self.game_state.set_state(GameState.TRICK_START)
            self.game_state.bidding_team = current_player.team_id
            self.game_state.defending_team = (current_player.team_id + 1) % 2

            is_loaner = self.handle_loaner(current_player)
            if is_loaner:
                self.loaner_team = current_player.team_id
                self.loaner_player = current_player

            EuchreDatabase.record_trump(self.game_state, bid, 2, current_player, None)
            self.reset_current_player()

        if bid == Card.SUIT_NOSUIT:
            logging.info("{} has decided not to announce a Trumps".format(current_player.name))
            if current_player == dealer:
                logging.info("The deal has been called Dead. It will be re-dealt.")
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

        logging.info("{} has set {} as Trumps.".format(current_player.name, Card.suit_str(selected_suit)))
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
        logging.info("{} has decided to go alone. {} will sit out of this round.".format(current_player.name, teammate.name))
        return True

    def handle_game_end(self):
        """
        This handle all the cleanup of the end of the game
        :return:
        """

        logging.info("Scores: TEAM A: {}, TEAM B: {}".format(self.scores[Teams.TEAM_A], self.scores[Teams.TEAM_B]))
        EuchreDatabase.end_game(self.game_state, self.scores[Teams.TEAM_A], self.scores[Teams.TEAM_B])
        self.tricks_won = [0, 0]
        self.scores = [0, 0]
        self.deck.shuffle_deck()
        self.game_state.set_state(GameState.GAME_START)

    def dead_deal(self):
        """
        In this case, all players passed on the face up card, and no one
        wanted to call trumps. This calls for a reshuffle, and re-deal.
        :return:
        """
        for player in self.players:
            player.clear_hand()
        self.deck.shuffle_deck()
        self.game_state.set_state(GameState.DEAL)
        self.current_player_turn = (self.game_state.current_dealer + 1) % len(self.players)
        EuchreDatabase.record_redeal(True)

    def reset_current_player(self):
        """
        Helper function that sets the current player to the player to the left of the dealer.
        :return: Nothing
        """
        self.current_player_turn = (self.game_state.current_dealer + 1) % len(self.players)
        self.game_state.lead_player = self.players[self.current_player_turn]

    def get_dealer(self) -> Player:
        """
        Get the current Dealer player object.
        :return: A player object.
        """
        return self.players[self.game_state.current_dealer]

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
        self.players[self.game_state.current_dealer].set_not_dealer()
        self.game_state.current_dealer = (self.game_state.current_dealer + 1) % len(self.players)
        self.players[self.game_state.current_dealer].set_dealer()

    def deal_cards(self):
        two_cards = True
        # Deal two rounds
        for x in range(0, 2):
            two_cards = not two_cards
            for idx in range(0, len(self.players)):
                p = ((self.game_state.current_dealer + 1) + idx) % len(self.players)
                cards = None
                if two_cards:
                    cards = self.deck.deal(2)
                elif not two_cards:
                    cards = self.deck.deal(3)

                if cards == None:
                    raise Exception("While dealing I ran out of cards...")

                two_cards = not two_cards

                self.players[p].receive_card(cards)

    def next_player(self):
        """
        Increment the current player by one spot.
        :return: Nothing.
        """
        self.current_player_turn = (self.current_player_turn + 1) % len(self.players)
        while self.players[self.current_player_turn].is_sitting_out():
            self.current_player_turn = (self.current_player_turn + 1) % len(self.players)

    def print_player_hands(self):
        for player in self.players:
            logging.info(player)


