from flask import Flask
from flask_cors import CORS

from EyeDiseaseDetect.Responses import code_0
from EyeDiseaseDetect.consts import TREE_DATA

app = Flask(__name__)
cors = CORS(app, supports_credentials=True)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/api/tree-list")
def get_tree_data():
    return code_0(TREE_DATA)


if __name__ == '__main__':
    app.run(port=21335)
