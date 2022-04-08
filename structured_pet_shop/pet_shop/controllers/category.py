from flask import (
    Blueprint, render_template, jsonify, request, redirect, url_for, flash
)
import pet_shop.services.category as svc_category


bp = Blueprint('category', __name__, url_prefix='/category')


# HTML related routes
@bp.route('/', methods=['GET'])
def home():
    categories, error = svc_category.get_all()
    flash(error)
    return render_template('category/index.html', categories=categories)


@bp.route('/detail/<int:id>', methods=['GET'])
def get_by_id(id):
    category, error = svc_category.get_by_id(id)
    flash(error)
    return render_template('category/detail.html', category=category)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    err = ''
    if request.method == 'POST':
        name = request.form['name']
        data = {
            'name': name.strip(),
        }
        _, error = svc_category.save(data)
        if not error:
            return redirect(url_for('category.home'))

        flash(err)

    return render_template('category/create.html')


@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    err = ''
    category, error = svc_category.get_by_id(id)

    if request.method == 'POST':
        name = request.form['name']
        data = {
            'id': int(id),
            'name': name.strip(),
        }
        _, error = svc_category.save(data)
        if not error:
            return redirect(url_for('category.home'))

        flash(err)

    return render_template('category/edit.html', category=category)


@bp.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    category, error = svc_category.get_by_id(id)
    if request.method == 'POST':
        _, error = svc_category.delete(id)
        if not error:
            return redirect(url_for('category.home'))

    flash(error)
    return render_template('category/delete.html', category=category)
