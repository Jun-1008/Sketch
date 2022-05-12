from flask_cors import CORS
from flask import request, Response
from flask import Flask, render_template, jsonify
import json

app = Flask(__name__, static_folder='./dist',
            template_folder='./dist')
CORS(app)

# array for saving pen history
pen_history = []


@app.route('/', defaults={'path': ''})
def index(path):
    return render_template('index.html')


@app.route('/save_history', methods=['post'])
def save_history():
    global pen_history
    if request.json["request_type"] == "save_history":
        json_pen_history = json.dumps(pen_history)

        file_json_pen_history = open("./data/pen_history.json", "w")
        file_json_pen_history.write(json_pen_history)
        file_json_pen_history.close()
        return jsonify({"response_type": "save_confirmed"})


@app.route('/save_line', methods=['post'])
def save_line():
    if request.json["request_type"] == "save_line":
        pen_history = request.json["pen_history"]
        on_save_history(pen_history)
        return jsonify({"response_type": "save_confirmed"})


def on_save_history(pen):
    global pen_history
    pen_move = pen

    pen_history.append(pen_move)


if __name__ == '__main__':
    app.run()
