import db

def get_player_team_id(players, player_id):
    """
    Given a player ID return their team ID

    :param players: A list of players from the database game['players']
    :param player_id: The id to find the team id of
    :return: The team id matching player_id, None if not found.
    """
    for player in players:
        if player['id'] == player_id:
            return player['team']

    return None

def find_dealer_winners_rnd1(dbase):
    """
    Determine if being the dealer helps with win percentage of a hand.

    :param dbase: Database object
    :return:
    """
    games = dbase.games.find({})
    dealer_team_won = 0
    total_hands = 0
    for game in games:
        for hand in game['hands']:
            if hand['redeal'] is True:  # ignore redealt hands
                continue
            if hand['bidding']['round'] == 2:  # ignore times where we go to the second bidding round
                continue
            if hand['winner']['winning_team'] == get_player_team_id(game['players'], hand['dealer']):
                dealer_team_won += 1
            total_hands += 1

    print("Times a dealer's team won {}".format(dealer_team_won))
    print("Total Hands: {}".format(total_hands))
    print("Percentage win of dealer's team: {}".format((dealer_team_won / total_hands) * 100))

def find_lead_winners(dbase):
    games = dbase.games.find({})

    lead_won_count = 0
    num_tricks = 0

    for game in games:
        for hand_num, hand in enumerate(game['hands']):
            if hand['redeal'] is True:
                continue
            for trick_num, trick in enumerate(hand['tricks']):
                try:

                    if trick[0]['team_id'] == trick[-1]['winning_team']:
                        lead_won_count += 1
                    num_tricks += 1
                except IndexError as ex:
                    print(
                        "Could not find index in game {} hand {} trick {}".format(game['game_id'], hand_num, trick_num))

    print("Number of tricks {}".format(num_tricks))
    print("Number of tricks where the lead won {}".format(lead_won_count))
    print("Percentage: {}".format((lead_won_count / num_tricks) * 100))


def calc_raw_winners(dbase):

    b_wins = dbase.games.find({'winning_team': 1}).count()
    a_wins = dbase.games.find({'winning_team': 0}).count()
    ties = dbase.games.find({'winning_team': 2}).count()

    total_games = b_wins + a_wins + ties

    a_win_percent = (a_wins / total_games) * 100
    b_win_percent = (b_wins / total_games) * 100
    ties_percent = (ties / total_games) * 100

    print("Team A won: {}% of the time.".format(a_win_percent))
    print("Team B won: {}% of the time.".format(b_win_percent))
    print("Ties: {}% of the time.".format(ties_percent))


def main():

    dbase = db.quick_setup()
    calc_raw_winners(dbase)
    find_lead_winners(dbase)
    find_dealer_winners_rnd1(dbase)

if __name__ == "__main__":
    main()