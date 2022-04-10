from sqlalchemy import exc, select, update
from petshop.models.category import Category
from petshop.db import session


def get_all():
    """ function to get all data """
    error = ''
    try:
        # scalars() is needed to make sure the result is put in a list
        statement = select(Category).order_by(Category.name)
        categorys = session.execute(statement).scalars().all()
    except exc.NoResultFound as e:
        error = e
    return categorys, error


def get_by_id(id):
    """ function to get data by id """
    error = ''
    try:
        category = session.get(Category, id)
    except exc.NoResultFound as e:
        error = e
    return category, error


def create(data):
    """ function to create from data dict, returning error if any """
    error = ''
    if data and data.get('name'):
        try:
            category = Category(data['name'])
            session.add(category)
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
            statement = update(Category)\
                .where(Category.id == data['id'])\
                .values(name=data['name'])\
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
        category = session.get(Category, id)
        session.delete(category)
        session.commit()
    except exc.IntegrityError as e:
        session.rollback()
        error = e
    return None, error
