from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
import petshop.services.pet as svc_pet
import petshop.services.category as svc_category


bp = Blueprint('pet', __name__, url_prefix='/pet')


@bp.route('/')
def home():
    pets, error = svc_pet.get_all()
    if error:
        flash(error)
    return render_template('pet/index.html', pets=pets)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    error = ''
    categories, _ = svc_category.get_all()
    if request.method == 'POST':
        name = request.form['name']
        category_id = request.form['category_id']
        name = name.strip()

        data = {
            'name': name,
            'category_id': category_id,
        }
        _, error = svc_pet.create(data)
        if not error:
            return redirect(url_for('pet.home'))

    if error:
        flash(error)

    return render_template('pet/create.html', categories=categories)


@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    error = ''
    pet, error = svc_pet.get_by_id(id)
    categories, _ = svc_category.get_all()
    if request.method == 'POST':
        name = request.form['name']
        category_id = request.form['category_id']
        name = name.strip()

        data = {
            'id': int(id),
            'name': name,
            'category_id': category_id,
        }
        _, error = svc_pet.edit(data)
        if not error:
            return redirect(url_for('pet.home'))

    if error:
        flash(error)

    return render_template('pet/edit.html', pet=pet, categories=categories)


@bp.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    error = ''
    pet, error = svc_pet.get_by_id(id)
    if request.method == 'POST':
        _, error = svc_pet.delete(id)
        if not error:
            return redirect(url_for('pet.home'))

    if error:
        flash(error)

    return render_template('pet/delete.html', pet=pet)
