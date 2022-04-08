from flask import (
    Blueprint, render_template
)


bp = Blueprint('', __name__)


@bp.route('/', methods=['GET'])
def home():
    return render_template('index.html')
