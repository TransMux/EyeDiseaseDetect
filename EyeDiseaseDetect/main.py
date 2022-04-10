from pathlib import Path
from typing import Dict

from flask import Flask, send_from_directory
from flask_cors import CORS
from service_streamer import ThreadedStreamer

from EyeDiseaseDetect.Models.ModelConstructor import ConstructModelPipe
from EyeDiseaseDetect.Models.yolov5s import Yolov5s
from EyeDiseaseDetect.Responses import code_0, internal_error
from EyeDiseaseDetect.utils import search_assets_structure

app = Flask(__name__)
cors = CORS(app, supports_credentials=True)

# 异步预测
Running_Tasks = []


# 每次添加模型都必须在这里配置！


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


@app.route("/api/models/list")
def model_list():
    return code_0(
        list(StreamerMap.keys())
    )


@app.route("/api/task/<model>/<path:path>")
def submit(path, model):
    try:
        img_path = data_path / "assets" / path
        assert img_path.exists(), "FileNotFound"
        Running_Tasks.append(
            StreamerMap[model].submit(
                [img_path]
            )
        )
        return code_0(None, msg="成功新建异步预测任务")
    except Exception as e:
        return internal_error(e.__repr__())


if __name__ == '__main__':
    data_path = Path(r"E:\competition\EyeDiseaseDetect\data")
    Tree = search_assets_structure(data_path / "assets", data_path / "assets")
    print(Tree)
    StreamerMap: Dict[str, ThreadedStreamer] = {
        "Yolov5s": ConstructModelPipe(Yolov5s(data_path / "models"))
    }

    # 启动后台服务器
    app.run(port=21335)
