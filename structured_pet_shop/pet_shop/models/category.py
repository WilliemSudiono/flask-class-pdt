from pet_shop.db import get_db  # notice we import the get_db function to use g


# every function here will return result and error to show that something
# happened in database transaction
def get_all_categories():
    """ function to get all of the categories in database """
    error = ''
    db = get_db()
    cur = db.cursor()
    sql = """
        SELECT id, name FROM categories
    """
    cur.execute(sql)
    categories = cur.fetchall()
    cur.close()

    if not categories:
        error = 'No Category found'

    return categories, error


def get_category_by_id(id):
    """ function to get category by id """
    error = ''
    db = get_db()
    cur = db.cursor()
    sql = """
        SELECT id, name FROM categories WHERE id = %d
    """ % (int(id))
    cur.execute(sql)
    category = cur.fetchone()
    cur.close()

    if not category:
        error = 'Invalid category with id: %d' % id

    return category, error


def create_category(data):
    """ function to create category based on data dict """
    # trust that data is already complete
    error = ''
    db = get_db()
    cur = db.cursor()
    try:
        sql = """
            INSERT INTO categories (name) VALUES ('%s')
        """ % data.get('name')
        cur.execute(sql)
        db.commit()
    except db.IntegrityError as e:
        error = e
    cur.close()
    return None, error


def update_category(data):
    """ function to update category based on data dict """
    # trust that data is already complete
    error = ''
    db = get_db()
    cur = db.cursor()
    try:
        sql = """
            UPDATE categories SET name = '%s' WHERE id = %d
        """ % (data.get('name'), data.get('id'))
        cur.execute(sql)
        db.commit()
    except db.IntegrityError as e:
        error = e
    cur.close()
    return None, error


def delete_category(id):
    """ function to delete category based on id """
    error = ''
    db = get_db()
    cur = db.cursor()
    try:
        sql = """
            DELETE FROM categories WHERE id = %d
        """ % (int(id))
        cur.execute(sql)
        db.commit()
    except db.IntegrityError as e:
        error = 'Category is related to a pet'
    except db.DatabaseError as e:
        error = e

    cur.close()
    return None, error
