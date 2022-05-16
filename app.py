from flask_cors import CORS
from flask import request, Response
from flask import Flask, render_template, jsonify
import json
import base64
import urllib.request
import numpy as np
import cv2
import io

app = Flask(__name__, static_folder='./dist',
            template_folder='./dist')
CORS(app)

# array for saving pen history
pen_history = []


@app.route('/', defaults={'path': ''})
def index(path):
    return render_template('index.html')


@app.route('/save_history', methods=['post'])#デコレーター
def save_history():
    # global pen_history
    if request.json["request_type"] == "save_history":
        # json_pen_history = json.dumps(pen_history)#画像の形で保存する
        data = request.json["data"] # base64データ
        # file_json_pen_history = open("./data/pen_history.json", "w")
        # file_json_pen_history.write(json_pen_history)
        # file_json_pen_history.close() #

        data = data.split(',')#冒頭の不要なデータを消去.
        data = data[1]
        # data = data.replace("'", "")

        image_file=r"decode.jpg"#画像表示はできたが失敗
        img_binary = base64.b64decode(data)
        print(img_binary)
        jpg=np.frombuffer(img_binary,dtype=np.uint8)
        img = cv2.imdecode(jpg, cv2.IMREAD_COLOR)
        cv2.imwrite(image_file,img)

        # data2 = base64.b64decode(data)
        # print(data2)

        # img_binary = cv2.imdecode(data, cv2.IMREAD_COLOR)
        # with open('data2.txt',"wb") as f:
        #     f.write(img_binary)
            # f.write(img)

        return jsonify({"response_type": "save_confirmed"})
        # jpg=np.frombuffer(img_binary,dtype=np.uint8)
        # img = cv2.imdecode(jpg, cv2.IMREAD_UNCHANGED)
        # cv2.imwrite('data/sketch.jpg',img)
        

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
