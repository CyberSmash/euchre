from sqlalchemy import Column, ForeignKey, Integer, String, Table, Boolean
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Player(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    player_name = Column(String(250))
    player_strategy = Column(Integer)


class Choices(Base):
    __tablename__ = 'choices_stats'
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('player.id'))
    was_lead = Column(Boolean)
    num_choices = Column(Integer)
    num_cards_left = Column(Integer)

engine = create_engine("sqlite:///euchre_data.db")

Base.metadata.create_all(engine)
