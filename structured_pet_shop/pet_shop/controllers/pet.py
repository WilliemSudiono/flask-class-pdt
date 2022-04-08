from flask import (
    Blueprint, render_template, jsonify, request, redirect, url_for, flash
)
import pet_shop.services.pet as svc_pet
import pet_shop.services.category as svc_category


bp = Blueprint('pet', __name__, url_prefix='/pet')


# HTML related routes
@bp.route('/', methods=['GET'])
def home():
    pets, error = svc_pet.get_all()
    flash(error)
    return render_template('pet/index.html', pets=pets)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    err = ''
    categories, _ = svc_category.get_all()
    if request.method == 'POST':
        name = request.form['name']
        category_id = request.form['category_id']
        data = {
            'name': name.strip(),
            'category_id': int(category_id),
        }
        _, error = svc_pet.save(data)
        if not error:
            return redirect(url_for('pet.home'))

        flash(err)

    return render_template('pet/create.html', categories=categories)


@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    err = ''
    pet, error = svc_pet.get_by_id(id)
    categories, _ = svc_category.get_all()

    if request.method == 'POST':
        name = request.form['name']
        category_id = request.form['category_id']
        data = {
            'id': int(id),
            'name': name.strip(),
            'category_id': int(category_id),
        }
        _, error = svc_pet.save(data)
        if not error:
            return redirect(url_for('pet.home'))

        flash(err)

    return render_template('pet/edit.html', pet=pet, categories=categories)


@bp.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    pet, error = svc_pet.get_by_id(id)
    if request.method == 'POST':
        _, error = svc_pet.delete(id)
        if not error:
            return redirect(url_for('pet.home'))

    flash(error)
    return render_template('pet/delete.html', pet=pet)
