from datetime import datetime, timedelta

from src import models
from src import constants


def add_new_gyms(gym_data):
    """ Find all gyms that are not yet in the database and save them to the
    database
    params:
        gym_data (list): a list of objects representing Gyms
    reutrns:
        (int): number of new gyms found
    """
    session = models.get_session()
    num_new = 0
    for gym in gym_data:
        gym_model = session.query(models.Gym).filter(
            models.Gym.gomap_id == gym['gym_id']).first()
        if gym_model is None:
            print('New gym found!', gym['name'])
            start_timetamp = min(m['time_deploy'] for m in gym['memb'])
            num_new += 1
            gym_model = models.Gym(
                name=gym['name'],
                gps_lat=gym['latitude'],
                gps_lon=gym['longitude'],
                gomap_id=gym['gym_id'],
                team=constants.Team(gym['team_id']),
                last_team_change=datetime.fromtimestamp(start_timetamp),
            )
    session.commit()
    return num_new


def add_new_trainers(gym_data):
    """ Find all trainers that are not yet in the database and save them to the
    database
    params:
        gym_data (list): a list of objects representing Gyms
    reutrns:
        (int): number of new trainers found
    """
    # First find a list of all trainers
    trainer_data = dict()
    for gym in gym_data:
        for trainer in gym['memb']:
            trainer_data[trainer['tn']] = trainer

    num_new = 0
    # Query and save them if they are not already in the database
    session = models.get_session()
    for mem in trainer_data.values():
        trainer = session.query(models.Trainer).filter(
            models.Trainer.name == mem['tn']).first()
        if trainer is None:
            print('New trainer found!', mem['tn'])
            num_new += 1
            trainer = models.Trainer(
                name=mem['tn'], team=constants.Team(gym['team_id']))
            session.add(trainer)
            stats = models.TrainerStats(trainer=trainer, verified=datetime.now())
            session.add(stats)
            level_badge = models.Badge(
                stats=stats, name='Level', description='Trainer level',
                value=mem["tl"])
            session.add(level_badge)
    session.commit()
    return num_new


def find_criminals(gym_data):
    """ Find all trainers that knocked down gyms younger than 500 minutes
    params:
        gym_data (list): a list of objects representing Gyms
    reutrns:
        (int): number of crimes commited
    """
    num_crimes = 0
    session = models.get_session()
    for gym in gym_data:
        gym_model = session.query(models.Gym).get(gomap_id=gym['gym_id'])
        new_team = constants.Team(gym['team_id'])
        if new_team != constants.Team.none and gym_model.team != new_team:
            # We found a team change!
            timetamp, name = min((m['time_deploy'], m['tn']) for m in gym['memb'])
            new_time = datetime.fromtimestamp(timetamp)
            standing = new_time - gym_model.last_team_change
            if standing < timedelta(minutes=500):
                # We found a bad boy!
                num_crimes += 1
                trainer = session.query(models.Trainer).get(name=name)
                crime = models.GymCrime(
                    gym_id=gym_model.id,
                    trainer_id=trainer.id,
                    standing_minutes=standing.total_seconds()//60,
                    beaten_time=new_time,
                )
                session.add(crime)
    session.commit()
    return num_crimes


def update_gyms(gym_data):
    """ Update all gym so they have correct color, occupations, and last change
    time
    params:
        gym_data (list): a list of objects representing Gyms
    reutrns:
        None
    """
    session = models.get_session()
    for gym in gym_data:
        gym_model = session.query(models.Gym).get(gomap_id=gym['gym_id'])
        new_team = constants.Team(gym['team_id'])
        if new_team != constants.Team.none and gym_model.team != new_team:
            # We found a team change!
            timetamp, name = min(m['time_deploy'] for m in gym['memb'])

            gym_model.team = new_team
            gym_model.last_team_change = datetime.fromtimestamp(timetamp)
            session.add(gym_model)

        # Check who is the gym and who is not
        # Previous occupations
        occupations = session.query(models.GymOccupation)\
            .filter(models.GymOccupation.end_time == None) \
            .filter(models.GymOccupation.gym_id == gym_model.id)
        now = datetime.now()
        accounted = []
        # Remove previous occupators
        for occupation in occupations:
            trainer = occupation.trainer
            for member in gym['memb']:
                if trainer.name == member['tn']:
                    accounted.append(member['tn'])
                    break
            else:
                occupation.end_time = now
                session.add(occupation)

        # Add new members
        for member in gym['memb']:
            if member['tn'] not in accounted:
                trainer = session.query(models.Trainer).get(name=member['tn'])
                new_occupation = models.GymOccupation(
                    start_time=datetime.fromtimestamp(member['time_deploy']),
                    gym_id=gym_model.id,
                    trainer_id=trainer.id,
                    pokemon_num=member['p']
                )
                session.add(new_occupation)

    session.commit()

def update_database(gym_data):

    add_new_gyms(gym_data)
    add_new_trainers(gym_data)
    find_criminals(gym_data)
    update_gyms(gym_data)
    update_trainers(gym_data)
