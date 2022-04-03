from flask import (
    Flask, render_template, request, redirect, url_for
)
from db import db_connection

app = Flask(__name__)


@app.route('/')
def index():
    """ function to show home page """
    return render_template('index.html')


@app.route('/categories', methods=['GET'])
def list_categories():
    categories = get_all_categories()
    return render_template('category/index.html', categories=categories)


@app.route('/category/create', methods=['GET', 'POST'])
def create_category():
    if request.method == 'POST':
        name = request.form['name']
        data = {
            'name': name,
        }
        save_category(data)
        return redirect(url_for('list_categories'))

    return render_template('category/create.html')


@app.route('/category/edit/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    category = get_category_by_id(category_id)

    if request.method == 'POST':
        name = request.form['name']
        data = {
            'id': category_id,
            'name': name,
        }
        save_category(data)
        return redirect(url_for('list_categories'))

    return render_template('category/edit.html', category=category)


@app.route('/category/delete/<int:category_id>', methods=['GET', 'POST'])
def delete_category(category_id):
    category = get_category_by_id(category_id)

    if request.method == 'POST':
        remove_category_by_id(category_id)
        return redirect(url_for('list_categories'))

    return render_template('category/delete.html', category=category)


def get_all_categories():
    """ function to get all of the categories """
    db = db_connection()
    cur = db.cursor()
    sql = """
        SELECT id, name
        FROM categories
        ORDER BY name
    """
    cur.execute(sql)
    categories = cur.fetchall()
    cur.close()
    db.close()
    return categories


def get_category_by_id(category_id):
    """ function to get category by certain ID """
    db = db_connection()
    cur = db.cursor()
    sql = """
        SELECT id, name
        FROM categories
        WHERE id = %d
    """ % (int(category_id))
    cur.execute(sql)
    category = cur.fetchone()
    cur.close()
    db.close()
    return category


def save_category(data):
    # data is a dict
    # notice by checking the existence of 'id', we could do update and insert
    if data:
        name = data.get('name')

        sql = """
            INSERT INTO categories (name) VALUES ('%s')
        """ % (name)

        if data.get('id'):  # if there is id in the data dict, UPDATE
            category_id = data.get('id')
            sql = """
                UPDATE categories SET name = '%s' WHERE id = %d
            """ % (name, category_id)

        db = db_connection()
        cur = db.cursor()
        cur.execute(sql)
        db.commit()
        cur.close()
        db.close()


def remove_category_by_id(category_id):
    db = db_connection()
    cur = db.cursor()
    sql = """
        DELETE FROM categories WHERE id = %d
    """ % (int(category_id))
    cur.execute(sql)
    db.commit()
    cur.close()
    db.close()


@app.route('/pets')
def list_pets():
    pets = get_all_pets()
    return render_template('pet/index.html', pets=pets)


@app.route('/pet/create', methods=['GET', 'POST'])
def create_pet():
    # in creating pet, we need information about the categories
    categories = get_all_categories()

    if request.method == 'POST':
        name = request.form['name']
        category_id = request.form['category_id']
        data = {
            'name': name,
            'category_id': int(category_id),
        }
        save_pet(data)
        return redirect(url_for('list_pets'))

    return render_template('pet/create.html', categories=categories)


@app.route('/pet/edit/<int:pet_id>', methods=['GET', 'POST'])
def edit_pet(pet_id):
    pet = get_pet_by_id(pet_id)
    categories = get_all_categories()

    if request.method == 'POST':
        name = request.form['name']
        category_id = request.form['category_id']
        data = {
            'id': pet_id,
            'name': name,
            'category_id': int(category_id),
        }
        save_pet(data)
        return redirect(url_for('list_pets'))

    return render_template('pet/edit.html', pet=pet, categories=categories)


@app.route('/pet/delete/<int:pet_id>', methods=['GET', 'POST'])
def delete_pet(pet_id):
    pet = get_pet_by_id(pet_id)

    if request.method == 'POST':
        remove_pet_by_id(pet_id)
        return redirect(url_for('list_pets'))

    return render_template('pet/delete.html', pet=pet)


def get_all_pets():
    """ function to get all of the pets """
    db = db_connection()
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
    db.close()
    return pets


def get_pet_by_id(pet_id):
    """ function to get pet by certain ID """
    db = db_connection()
    cur = db.cursor()
    sql = """
        SELECT pet.id, pet.name, pet.category_id
        FROM pets pet
        WHERE pet.id = %d
    """ % (int(pet_id))
    cur.execute(sql)
    pet = cur.fetchone()
    cur.close()
    db.close()
    return pet


def save_pet(data):
    if data:
        name = data.get('name')
        category_id = data.get('category_id')

        sql = """
            INSERT INTO pets (name, category_id) VALUES ('%s', %d)
        """ % (name, category_id)

        if data.get('id'):  # if there is id in the data dict, UPDATE
            pet_id = data.get('id')
            sql = """
                UPDATE pets SET name = '%s', category_id = %d WHERE id = %d
            """ % (name, category_id, pet_id)

        db = db_connection()
        cur = db.cursor()
        cur.execute(sql)
        db.commit()
        cur.close()
        db.close()


def remove_pet_by_id(pet_id):
    db = db_connection()
    cur = db.cursor()
    sql = """
        DELETE FROM pets WHERE id = %d
    """ % (int(pet_id))
    cur.execute(sql)
    db.commit()
    cur.close()
    db.close()
