from sqlalchemy import exc, insert, select, update
from petshop.models.pet import Pet
from petshop.db import session


def get_all():
    """ function to get all data """
    error = ''
    try:
        # scalars() is needed to make sure the result is put in a list
        statement = select(Pet).order_by(Pet.name)
        pets = session.execute(statement).scalars().all()
    except exc.NoResultFound as e:
        error = e
    return pets, error


def get_by_id(id):
    """ function to get data by id """
    error = ''
    try:
        pet = session.get(Pet, id)
    except exc.NoResultFound as e:
        error = e
    return pet, error


def create(data):
    """ function to create from data dict, returning error if any """
    error = ''
    if data:
        try:
            statement = insert(Pet).values(data)
            session.execute(statement)
            session.commit()
        except exc.IntegrityError as e:
            session.rollback()
            error = e

    return None, error


def edit(data):
    """ function to edit from data dict, returning error if any """
    error = ''
    if data and data.get('name') and data.get('id'):
        try:
            update_data = data.copy()
            update_data.pop('id')
            statement = update(Pet)\
                .where(Pet.id == data['id'])\
                .values(update_data)\
                .execution_options(synchronize_session='fetch')
            session.execute(statement)
            session.commit()
        except exc.IntegrityError as e:
            session.rollback()
            error = e

    return None, error


def delete(id):
    """ function to delete based on id, returning error if any """
    error = ''
    try:
        pet = session.get(Pet, id)
        session.delete(pet)
        session.commit()
    except exc.IntegrityError as e:
        session.rollback()
        error = e
    return None, error
