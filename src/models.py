import datetime

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from src import constants


class BaseModel(object):
    id = sa.Column(sa.Integer, primary_key=True)
    time_created = sa.Column(
        sa.DateTime, default=datetime.datetime.now, nullable=False)
    time_updated = sa.Column(
        sa.DateTime, default=datetime.datetime.now,
        onupdate=datetime.datetime.now, nullable=False)


Base = declarative_base(cls=BaseModel)


class Trainer(Base):
    __tablename__ = 'trainer'
    # Trainers Username
    name = sa.Column(sa.String(250), nullable=False, unique=True)
    # Which team does he belong to
    # 0-None, 1-Mystic, 2-Valor, 3-Instinct
    team = sa.Column(sa.Enum(constants.Team), nullable=False)

    # All saved stats that belong to this trainer
    all_stats = relationship('TrainerStats')


class TrainerStats(Base):
    __tablename__ = 'trainer_stats'
    # Stats for which trainer
    trainer_id = sa.Column(sa.Integer, sa.ForeignKey('trainer.id'), nullable=False)
    trainer = relationship(Trainer)
    # When were the stats verified (None if never)
    verified = sa.Column(sa.DateTime, nullable=True, default=None)

    # Level of the trainer
    level = sa.Column(sa.Integer, nullable=True)
    # Total XP of the trainer
    xp = sa.Column(sa.Integer, nullable=True)

    # All badges that belong to this stat instance
    badges = relationship('Badge')


class Badge(Base):
    __tablename__ = 'badge'
    # To which stat instance does this badge belong
    stats_id = sa.Column(sa.Integer, sa.ForeignKey('trainer_stats.id'), nullable=False)
    stats = relationship(TrainerStats)
    # Name of the badge: e.g. Kanto
    badge_name = sa.Column(sa.String(250), nullable=False)
    # Integer value of the badge
    badge_value = sa.Column(sa.Integer, nullable=False)


class Gym(Base):
    __tablename__ = 'gym'
    # Gym in-game name
    name = sa.Column(sa.String(250), nullable=False)
    # Gym GPS coordinates
    gps_lat = sa.Column(sa.Float, nullable=False)
    gps_lon = sa.Column(sa.Float, nullable=False)
    # ID as fetched from GoMap
    gomap_id = sa.Column(sa.Integer, unique=True, nullable=False)
    # Which team currently occupies this gym
    team = sa.Column(sa.Enum(constants.Team), nullable=False)


class GymOccupation(Base):
    __tablename__ = 'gym_occupation'
    # Time span of occupation. If end_time=None it means ongoing
    start_time = sa.Column(sa.DateTime, nullable=False)
    end_time = sa.Column(sa.DateTime, nullable=True)

    # Which gym is occupied
    gym_id = sa.Column(sa.Integer, sa.ForeignKey('gym.id'), nullable=False)
    gym = relationship(Gym)

    # Which trainer is occupying the gym
    trainer_id = sa.Column(sa.Integer, sa.ForeignKey('trainer.id'), nullable=False)
    trainer = relationship(Trainer)
    # Which pokemon is in the gym
    pokemon_num = sa.Column(sa.Integer, nullable=False)


def test():
    from sqlalchemy.orm import sessionmaker
    engine = create_engine('sqlite:///sqlalchemy_example.db')

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    Base.metadata.create_all(engine)

    t = Trainer(name="Maks", team="instinct")
    session.add(t)
    session.commit()


if __name__ == "__main__":
    test()
