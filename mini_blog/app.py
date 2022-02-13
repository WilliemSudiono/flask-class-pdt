from flask import Flask, render_template, request, redirect
import json


app = Flask(__name__)


@app.route('/')
def index():
    """ read article (file) name from articles.txt """
    articles = []
    json_names = {}  # initiate empty dict
    with open('articles.txt', 'r+') as f:  # open file
        json_names = json.load(f)  # load the json inside text file
    articles = [x for x in json_names.keys()]  # get keys (title) inside list
    return render_template('index.html', articles=articles)  # pass to template


@app.route('/create', methods=['GET', 'POST'])
def create():
    # GET method, render the html to prepare form
    if request.method == 'GET':
        return render_template('create.html')
    else:  # post, find data and save
        articles = {}
        # form takes from tag "name" value
        title = request.form['title']
        body = request.form['body']

        # open the file and write, thus r+
        with open('articles.txt', 'r+') as f:
            articles = json.load(f)
            # strip contents to remove unused whitespaces
            articles[title] = body.strip()  # add new title as key, body as value
            f.seek(0)  # put it at the beginning to replace the whole file
            json.dump(articles, f)  # re-insert the data

        # then show the view page with title and body
        return render_template('view.html', title=title, body=body)


@app.route('/view/<string:title>', methods=['GET'])
def view(title):
    # NOTE: this function accepts parameter (title) and so does the URL route
    # open file with title and show content
    body = ''
    with open('articles.txt', 'r') as f:
        articles = json.load(f)
        body = articles[title].strip()  # find value of certain title
    return render_template('view.html', title=title, body=body)


@app.route('/edit/<string:title>', methods=['GET', 'POST'])
def edit(title):
    # GET, show the content of files and the title
    if request.method == 'GET':
        body = ''
        with open('articles.txt', 'r') as f:
            articles = json.load(f)
            body = articles[title]  # find value of certain title
        return render_template('edit.html', title=title, body=body)
    else:  # POST
        original_title = title  # used as key
        title = request.form['title']
        body = request.form['body']

        # open file, find the original_title and pop
        with open('articles.txt', 'r+') as f:
            articles = json.load(f)
            articles.pop(original_title)  # remove the old title
            articles[title] = body  # insert a new one
            f.seek(0)  # put at beginning
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
            articles.pop(title)  # remove data with key "title"
            f.seek(0)  # put at beginning
            f.truncate(0)  # remove the whole content of file
            json.dump(articles, f)  # add the new one

        return redirect('/')  # go back to home
