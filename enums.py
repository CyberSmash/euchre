from enum import IntEnum

class GameType(IntEnum):
    # Progressive plays for 8 hands. For X rounds, regardless of score
    PROGRESSIVE = 0

    # Traditional is played first to 10 points.
    TRADITIONAL = 1

class Teams(IntEnum):
    TEAM_A = 0
    TEAM_B = 1
    BOTH = 2  # Technically it's possible for both to win in a progressive game. This helps solve that issue.