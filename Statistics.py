class Statistics(object):

    num_games = 0

    def __init__(self):
        pass


class HandStatistics(Statistics):

    def __init__(self):
        self.num_choices = 0
        self.num_tricks = 0

    def add_num_choices(self, choices):
        self.num_choices += choices

    def calc_average_choices(self):
        return self.num_choices / self.num_tricks
