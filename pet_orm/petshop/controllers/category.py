from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
import petshop.services.category as svc_category


bp = Blueprint('category', __name__, url_prefix='/category')


@bp.route('/')
def home():
    categories, error = svc_category.get_all()

    if error:
        flash(error)

    return render_template('category/index.html', categories=categories)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    error = ''
    if request.method == 'POST':
        name = request.form['name']
        name = name.strip()

        data = {
            'name': name,
        }
        _, error = svc_category.create(data)
        if not error:
            return redirect(url_for('category.home'))

    if error:
        flash(error)

    return render_template('category/create.html')


@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    error = ''
    category, error = svc_category.get_by_id(id)
    if request.method == 'POST':
        name = request.form['name']
        name = name.strip()

        data = {
            'id': int(id),
            'name': name,
        }
        _, error = svc_category.edit(data)
        if not error:
            return redirect(url_for('category.home'))

    if error:
        flash(error)

    return render_template('category/edit.html', category=category)


@bp.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    error = ''
    category, error = svc_category.get_by_id(id)
    if request.method == 'POST':
        _, error = svc_category.delete(id)
        if not error:
            return redirect(url_for('category.home'))

    if error:
        flash(error)

    return render_template('category/delete.html', category=category)
