from pathlib import Path

from flask import Flask
from flask_cors import CORS

from EyeDiseaseDetect.Responses import code_0, internal_error
from EyeDiseaseDetect.utils import search_assets_structure

app = Flask(__name__)
cors = CORS(app, supports_credentials=True)

Tree = None


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/api/tree-list")
def get_tree_data():
    if Tree is None:
        return internal_error("图片树未初始化")
    return code_0(Tree)


def entry():
    global Tree
    data_path = Path(r"E:\competition\EyeDiseaseDetect\data")
    Tree = search_assets_structure(data_path / "assets")
    print(Tree)
    # app.run(port=21335)


if __name__ == '__main__':
    entry()
