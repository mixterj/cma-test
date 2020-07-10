# importing modules
from flask import Flask, render_template, json, request, send_from_directory
from flask_bootstrap import Bootstrap
import re, os

# declaring app name
app = Flask(__name__)

# set variables for app
bootstrap = Bootstrap(app)
image_list = []
creators_dict = {}
department_dict = {}
title_list = []
title_id_lookup = {}


with open('./static/data/image-data.json') as f:
    images = json.load(f)

for key, value in images.items():
    image_obj = {}
    image_obj['id'] = key
    image_obj['image'] = value['image']
    image_obj['title'] = value['title']
    image_obj['description'] = value['tombstone']
    image_list.append(image_obj)
    title_list.append(value['title'].lower())
    title_id_lookup[value['title'].lower()] = key

for key, value in images.items():
    if len(value['creator']) > 0:
        for item in value['creator']:
            if item['id'] not in creators_dict:
                creators_dict[item['id']] = {}
                creators_dict[item['id']]['artworks'] = []
                creators_dict[item['id']]['artworks'].append(key)
                creators_dict[item['id']]['role'] = item['role']
                creators_dict[item['id']]['description'] = item['description']
            else:
                creators_dict[item['id']]['artworks'].append(key)

for key, value in images.items():
    if value['department']['id'] not in department_dict:
        department_dict[value['department']['id']] = {}
        department_dict[value['department']['id']]['artworks'] = []
        department_dict[value['department']['id']]['artworks'].append(key)
        department_dict[value['department']['id']]['name'] = value['department']['name']
    else:
        department_dict[value['department']['id']]['artworks'].append(key)

# defining home page
@app.route('/')
def homepage():
    return render_template("index.html", len = len(image_list), image_list = image_list, departments = department_dict, creators = creators_dict)

@app.route('/details/<id>')
def profile(id):
    image = images[id]

    return render_template("details.html", image = images[id])

@app.route('/creator/<id>')
def creator(id):
    creator = creators_dict[id]
    return render_template("creator.html", creator = creators_dict[id], images = images)

@app.route('/department/<id>')
def departmen(id):
    department = department_dict[id]
    print(id)
    return render_template("department.html", department = department_dict[id], images = images)

@app.route('/search', methods=['POST'])
def search():
    search = request.form['inputSearch']
    substr = []
    match_ids = []
    substr.append(search)
    matches = Filter(title_list, substr)
    for match in matches:
        match_id = title_id_lookup[match]
        match_ids.append(match_id)
    return render_template('search.html', match_list=match_ids, images = images)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

def Filter(string, substr):
    return [str for str in string if
             any(sub in str for sub in substr)]


app.run(host='0.0.0.0', port=5001)