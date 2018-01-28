from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

association_table = Table(
    'association', Base.metadata,
    Column('left_id', Integer), ForeignKey('left.id'),
    Column('right_id', Integer), ForeignKey('right.id')
)



class Player(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    total_tricks_won = Column(Integer)
    strategy = Column(Integer)
    games = relationship("Game", secondary=association_table, back_populates="players")


class Game(Base):
    id = Column(Integer, primary_key=True)
    game_type = Column(Integer)
    team_a_tricks = Column(Integer)
    team_b_tricks = Column(Integer)
    players = relationship("Player", secondary=association_table, back_populates="games")


"""
class Hand(Base):
    id = Column(Integer, primary_key=True)
    player = relationship(Player)
    hand_data = Column(String(250))




class Game(Base):
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True)
    team_a_tricks = Column(Integer)
    team_b_tricks = Column(Integer)

    player_1 = relationship(Player)
    player_2 = relationship(Player)
    player_3 = relationship(Player)
    player_4 = relationship(Player)
"""



engine = create_engine("sqlite:///euchre_data.db")

Base.metadata.create_all(engine)