import db
from enums import Teams
import pprint
game = dict()


def start_game(game_state: object, players: list, game_type: object):
    global game

    game = {
        'game_id': game_state.game_id,
        'game_type': game_type,
        'players': list(),
        'hands': list(),
        'scores': {
            'team_a': None,
            'team_b': None,
        },
        'winning_team': None
    }

    for player in players:
        game['players'].append({
            'name': player.name,
            'team': player.team_id,
            'id': player.player_num,
        })


def record_deal(game_state, players):
    """
    Called immediatly after a deal, before bidding.
    :param game_state:
    :param players:
    :return:
    """
    global game
    game['hands'].append(dict())
    game['hands'][-1]['player_hands'] = [None] * len(players)

    for player in players:
        game['hands'][-1]['player_hands'][player.player_num] = list()
        for card in player.hand:
            game['hands'][-1]['player_hands'][player.player_num].append(str(card))
        game['hands'][-1]['top_card'] = str(game_state.top_card)

    game['hands'][-1]['dealer'] = game_state.current_dealer


def record_trick_end(winning_team, trick_num):
    """
    Record the results of the trick as if it were a 6th trick

    This is admittedly a little strange, but I can't come up with a more straight forward
    way of being able to access this data.

    :param winning_team: The team who won the trick
    """
    global game
    game['hands'][-1]['tricks'][trick_num].append(
        {
            'winning_team': winning_team,
        }
    )


def record_hand_score(winning_team, points_scored, team_a_tricks, team_b_tricks):
    global game
    game['hands'][-1]['winner'] = {
        'winning_team': winning_team,
        'points_scored': points_scored,
        'tricks': [
            team_a_tricks,
            team_b_tricks
        ]

    }


def record_trick(card, player, trick_num):

    global game
    if 'tricks' not in game['hands'][-1]:
        game['hands'][-1]['tricks'] = [[] for _ in range(5)]  # Honestly, I need to make these magic numbers constants


    game['hands'][-1]['tricks'][trick_num].append({
        'card': str(card),
        'player_id': player.player_num,
        'team_id': player.team_id
    })


def record_redeal(is_redeal):
    """
    Called when a deal is considered dead, and the hand is redealt.

    :param is_redeal: True if this is aredeal. False otherwise.
    """
    global game
    game['hands'][-1]['redeal'] = is_redeal


def record_trump(game_state, suit, bid_round, player, card):
    global game
    game['hands'][-1]['bidding'] = {
            'suit': suit,
            'round': bid_round,
            'deciding_player': player.player_num,
            'card': str(card),
            'bidding_team': game_state.bidding_team,
            'defending_team': game_state.defending_team
    }
    record_redeal(False)


def end_game(game_state, team_a_score: int, team_b_score: int):
    pp = pprint.PrettyPrinter(indent=4)
    global game
    game['scores'] = [None]*2
    game['scores'][Teams.TEAM_A] = team_a_score
    game['scores'][Teams.TEAM_B] = team_b_score

    if team_a_score > team_b_score:
        game['winning_team'] = Teams.TEAM_A.value
    elif team_b_score > team_a_score:
        game['winning_team'] = Teams.TEAM_B.value
    else:
        game['winning_team'] = Teams.BOTH.value

    dbase = db.quick_setup()
    #pp.pprint(game)
    dbase.games.insert(game)
