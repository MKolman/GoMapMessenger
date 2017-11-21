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

    @classmethod
    def query(cls):
        session = get_session()
        return session.query(cls)


Base = declarative_base(cls=BaseModel)


class Trainer(Base):
    __tablename__ = 'trainer'
    # Trainers Username
    name = sa.Column(sa.String(250), nullable=False, unique=True)
    # Which team does he belong to
    # 0-None, 1-Mystic, 2-Valor, 3-Instinct
    team = sa.Column(sa.Enum(constants.Team), nullable=False)

    # All saved stats that belong to this trainer
    all_stats = relationship('TrainerStats', order_by='TrainerStats.time_created')

    def get_latest_stats(self, only_verified=False):
        result = dict()
        for stat in self.all_stats:
            if only_verified and stat.verified is None:
                continue
            for badge in stat.badges:
                result[badge.name] = badge
        return result

    def get_latest_stat(self, stat_name, only_verified=False):
        query = Badge.query() \
            .filter(Badge.name == stat_name) \
            .join(Badge.stats) \
            .filter(TrainerStats.trainer_id == self.id) \
            .order_by(TrainerStats.time_created)
        if only_verified:
            query = query.filter(TrainerStats.verified.isnot(None)) \
                         .filter(TrainerStats.verified != '')
        return query.first()


class TrainerStats(Base):
    __tablename__ = 'trainer_stats'
    # Stats for which trainer
    trainer_id = sa.Column(sa.Integer, sa.ForeignKey('trainer.id'), nullable=False)
    trainer = relationship(Trainer)
    # When were the stats verified (None if never)
    verified = sa.Column(sa.DateTime, nullable=True, default=None)

    # All badges that belong to this stat instance
    badges = relationship('Badge')


class Badge(Base):
    __tablename__ = 'badge'
    # To which stat instance does this badge belong
    stats_id = sa.Column(sa.Integer, sa.ForeignKey('trainer_stats.id'), nullable=False)
    stats = relationship(TrainerStats)
    # Name of the badge: e.g. Kanto
    name = sa.Column(sa.String(250), nullable=False)
    # E-g Catch bug-type pokemon
    description = sa.Column(sa.String(500), nullable=False)
    # Integer value of the badge
    value = sa.Column(sa.Integer, nullable=False)
    # Each stat can only have one badge per type
    __table_args__ = (
        sa.UniqueConstraint("stats_id", "name"),
    )


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
    # When was the last change of team color (for wall of shame)
    last_team_change = sa.Column(
        sa.DateTime, default=datetime.datetime.now, nullable=False)


class GymOccupation(Base):
    __tablename__ = 'gym_occupation'
    # Time span of occupation. If end_time=None it means ongoing
    start_time = sa.Column(sa.DateTime, nullable=False)
    end_time = sa.Column(sa.DateTime, nullable=True, default=None)

    # Which gym is occupied
    gym_id = sa.Column(sa.Integer, sa.ForeignKey('gym.id'), nullable=False)
    gym = relationship(Gym)

    # Which trainer is occupying the gym
    trainer_id = sa.Column(sa.Integer, sa.ForeignKey('trainer.id'), nullable=False)
    trainer = relationship(Trainer)
    # Which pokemon is in the gym
    pokemon_num = sa.Column(sa.Integer, nullable=False)


class GymCrime(Base):
    __tablename__ = 'gym_crime'
    # Where was the crime commited
    gym_id = sa.Column(sa.Integer, sa.ForeignKey('gym.id'), nullable=False)
    # Who commited the crime
    trainer_id = sa.Column(sa.Integer, sa.ForeignKey('trainer.id'), nullable=False)
    # Duration in minutes that the gym was standing before it was torn down
    standing_minutes = sa.Column(sa.Integer, nullable=False)
    # Time at which the gym was wrongfully beaten
    beaten_time = sa.Column(sa.DateTime, nullable=True)


def get_session():
    from sqlalchemy.orm import sessionmaker
    sql_engine = create_engine("sqlite:///gym_status.sqlite")
    DBSession = sessionmaker(bind=sql_engine)
    return DBSession()

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
