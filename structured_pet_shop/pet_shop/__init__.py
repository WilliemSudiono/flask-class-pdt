from flask import Flask


def create_app():
    """ special function in Flask to use the Factory pattern """
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='THISISASECRETKEY'
    )

    from . import db
    db.init_app(app)  # connect the db to app to use teardown_appcontext

    from pet_shop.controllers import category, pet, home
    app.register_blueprint(home.bp)
    app.register_blueprint(category.bp)
    app.register_blueprint(pet.bp)

    return app
