import db
from enums import Teams
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
        })


def record_deal(game_state, players):
    global game
    game['hands'].append(dict())
    for player in players:
        game['hands'][-1][player.name] = str(player.hand)

        game['hands'][-1]['top_card'] = str(game_state.top_card)


def record_redeal(is_redeal):
    game['hands'][-1]['redeal'] = is_redeal


def record_trump(suit, bid_round, player_name, card):
    game['hands'][-1]['bidding'] = {
            'suit': suit,
            'round': bid_round,
            'player': player_name,
            'card': str(card)
    }
    record_redeal(False)


def end_game(game_state, team_a_score: int, team_b_score: int):
    global game

    game['scores']['team_a'] = team_a_score
    game['scores']['team_b'] = team_b_score

    if team_a_score > team_b_score:
        game['winning_team'] = Teams.TEAM_A.value
    elif team_b_score > team_a_score:
        game['winning_team'] = Teams.TEAM_B.value
    else:
        game['winning_team'] = Teams.BOTH.value

    dbase = db.quick_setup()
    dbase.games.insert(game)
