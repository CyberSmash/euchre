import db


def main():
    dbase = db.quick_setup()
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

if __name__ == "__main__":
    main()