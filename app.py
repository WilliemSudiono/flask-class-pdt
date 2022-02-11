from flask import Flask, render_template, request, jsonify


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/square', methods=['POST'])
def square():
    response = {}
    data = request.get_json()
    if data.get('number'):
        number = int(data['number'])
        response = {'status': 200, 'result': number * number, 'message': 'Success'}
    else:
        response = {'status': 500, 'result': 0, 'message': 'Error'}
    return jsonify(response)
