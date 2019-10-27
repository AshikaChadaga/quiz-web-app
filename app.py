import copy
import json
from flask import Flask, render_template, request
from flask_pymongo import PyMongo

CONFIG = {}
WRONG_ANS = []
COUNT = 0
DYNAMIC_HTML = "home.html"

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/test_database"
mongo = PyMongo(app)


@app.route("/")
def home_page():
    global WRONG_ANS, COUNT
    WRONG_ANS = []
    COUNT = 0
    return render_template(DYNAMIC_HTML)


@app.route("/", methods=['POST'])
def evaluate():
    for x in request.form.items():
        validate(x[0], x[1])
    print("count - ", COUNT)
    print("wrong ans - ", WRONG_ANS)
    return render_template('end.html', count=COUNT, wrong=WRONG_ANS)


def validate(key, value):
    global WRONG_ANS, COUNT
    keys = key.split("_")
    query = copy.deepcopy(CONFIG[keys[0]]["query"])
    var = CONFIG[keys[0]]["questions"][keys[1]]["variable"]
    req = CONFIG[keys[0]]["questions"][keys[1]]["required_field"]
    question = CONFIG[keys[0]]["questions"][keys[1]]["Q"]

    for field, val in query.items():
        if val == "var":
            query[field] = var
    db = mongo.db.posts.find(query)
    for x in db:
        if x[req] == value:
            COUNT = COUNT + 1
        else:
            wrong = (question, x[req], value)
            WRONG_ANS = WRONG_ANS + [wrong]


def generate_template(config):
    part_0 = '<html><head><style>h1{text-align:center;font-family: Orbitron;font-size: 300%;}</style></head><body><h1>QUIZ</h1>'
    part_1 = '<form method="post">'
    part_2 = '<h4 style="color:red" ;><b>'
    part_3 = '</b></h4><br><input type="text" name="'
    part_4 = '">'
    part_5 = '<br><br><button type="submit" value=Submit>Submit</button></form>'
    part_6 = '</body></html>'
    h_file = open("templates/" + DYNAMIC_HTML, "w")
    h_file.write(part_0)
    for type, values in config.items():
        h_file.write(part_1)
        for key, questions in values["questions"].items():
            html_str = part_2 + questions["Q"] + part_3 + type + "_" + key + part_4
            h_file.write(html_str)
    h_file.write(part_5)
    h_file.write(part_6)
    h_file.close()


if __name__ == '__main__':
    with open("config/config.json") as f:
        CONFIG = json.load(f)
    generate_template(CONFIG)
    app.run(debug=True)
