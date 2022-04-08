from pet_shop.db import get_db


def get_all_pets():
    """ function to get all of the pets in database """
    error = ''
    db = get_db()
    cur = db.cursor()
    sql = """
        SELECT pet.id, pet.name, category.name
        FROM pets pet
        JOIN categories category ON category.id = pet.category_id
        ORDER BY pet.name
    """
    cur.execute(sql)
    pets = cur.fetchall()
    cur.close()

    if not pets:
        error = 'No Pet found'

    return pets, error


def get_pet_by_id(id):
    """ function to get pet by id """
    error = ''
    db = get_db()
    cur = db.cursor()
    sql = """
        SELECT id, name, category_id FROM pets WHERE id = %d
    """ % (int(id))
    cur.execute(sql)
    pet = cur.fetchone()
    cur.close()

    if not pet:
        error = 'Invalid pet with id: %d' % id

    return pet, error


def create_pet(data):
    """ function to create pet based on data dict """
    # trust that data is already complete
    error = ''
    db = get_db()
    cur = db.cursor()
    try:
        sql = """
            INSERT INTO pets (name, category_id) VALUES ('%s', %d)
        """ % (data.get('name'), data.get('category_id'))
        cur.execute(sql)
        db.commit()
    except db.IntegrityError as e:
        error = e
    cur.close()
    return None, error


def update_pet(data):
    """ function to update pet based on data dict """
    # trust that data is already complete
    error = ''
    db = get_db()
    cur = db.cursor()
    try:
        sql = """
            UPDATE pets
            SET name = '%s', category_id = %d
            WHERE id = %d
        """ % (data.get('name'), data.get('category_id'), data.get('id'))
        cur.execute(sql)
        db.commit()
    except db.IntegrityError as e:
        error = e
    cur.close()
    return None, error


def delete_pet(id):
    """ function to delete pet based on id """
    error = ''
    db = get_db()
    cur = db.cursor()
    try:
        sql = """
            DELETE FROM pets WHERE id = %d
        """ % (int(id))
        cur.execute(sql)
        db.commit()
    except db.IntegrityError as e:
        error = e
    except db.DatabaseError as e:
        error = e

    cur.close()
    return None, error
