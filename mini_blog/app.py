from flask import Flask, render_template, request, redirect
import json


app = Flask(__name__)


@app.route('/')
def index():
    """ read article (file) name from article_name.txt """
    articles = []
    json_names = {}
    with open('articles.txt', 'r+') as f:
        json_names = json.load(f)
    articles = [x for x in json_names.keys()]
    return render_template('index.html', articles=articles)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create.html')
    else:  # post, find data and save
        articles = {}
        title = request.form['title']
        body = request.form['body']

        with open('articles.txt', 'r+') as f:
            articles = json.load(f)
            articles[title] = body
            f.seek(0)
            json.dump(articles, f)

        return render_template('view.html', title=title, body=body)


@app.route('/view/<string:title>', methods=['GET'])
def view(title):
    # open file with title and show content
    body = ''
    with open('articles.txt', 'r') as f:
        articles = json.load(f)
        body = articles[title].strip()
    return render_template('view.html', title=title, body=body)


@app.route('/edit/<string:title>', methods=['GET', 'POST'])
def edit(title):
    if request.method == 'GET':
        body = ''
        with open('articles.txt', 'r') as f:
            articles = json.load(f)
            body = articles[title]
        return render_template('edit.html', title=title, body=body)
    else:
        original_title = title
        title = request.form['title']
        body = request.form['body']

        # open file, find the original_title and pop
        with open('articles.txt', 'r+') as f:
            articles = json.load(f)
            articles.pop(original_title)
            articles[title] = body
            f.seek(0)
            json.dump(articles, f)

        return render_template('view.html', title=title, body=body)


@app.route('/delete/<string:title>', methods=['GET', 'POST'])
def delete(title):
    if request.method == 'GET':
        body = ''
        with open('articles.txt', 'r') as f:
            articles = json.load(f)
            body = articles[title]
        return render_template('delete.html', title=title, body=body)
    else:
        title = request.form['title']
        body = request.form['body']

        # open file, find the original_title and pop
        with open('articles.txt', 'r+') as f:
            articles = json.load(f)
            articles.pop(title)
            f.seek(0)
            f.truncate(0)
            json.dump(articles, f)

        return redirect('/')
