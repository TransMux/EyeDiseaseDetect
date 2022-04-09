from pathlib import Path

from flask import Flask, send_from_directory
from flask_cors import CORS

from EyeDiseaseDetect.Responses import code_0, internal_error
from EyeDiseaseDetect.utils import search_assets_structure

app = Flask(__name__)
cors = CORS(app, supports_credentials=True)

data_path: Path = Path()
Tree = None


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/api/tree-list")
def get_tree_data():
    if Tree is None:
        return internal_error("图片树未初始化")
    return code_0(Tree)


@app.route("/api/picture/<path:path>")
def send_report(path):
    return send_from_directory(str(data_path / "assets"), path)


def entry():
    # 读取配置文件
    global data_path
    data_path = Path(r"E:\competition\EyeDiseaseDetect\data")

    # 读取文件树
    global Tree
    Tree = search_assets_structure(data_path / "assets", data_path / "assets")
    print(Tree)

    # 启动后台服务器
    app.run(port=21335)


if __name__ == '__main__':
    entry()
