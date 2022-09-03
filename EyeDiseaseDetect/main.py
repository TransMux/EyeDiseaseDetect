import json
import os
import sys

sys.path.append("..")
from EyeDiseaseDetect.Models.ResNet.ResNet import Pneumonia
from pathlib import Path
from typing import Dict

from flask import Flask, send_from_directory, request
from flask_cors import CORS
from service_streamer import ThreadedStreamer
from werkzeug.utils import secure_filename

from EyeDiseaseDetect.Models.ModelConstructor import ConstructModelPipe
from EyeDiseaseDetect.Responses import code_0, internal_error, NotAllowed
from EyeDiseaseDetect.utils import search_assets_structure

app = Flask(__name__)
cors = CORS(app, supports_credentials=True)

# 异步预测
Running_Tasks = []
glaucoma = Pneumonia()

# 每次添加模型都必须在这里配置！


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/api/tree/list")
def get_tree_data():
    if Tree is None:
        return internal_error("图片树未初始化")
    return code_0(Tree)


@app.route("/api/tree/update")
def resync():
    global Tree
    Tree = search_assets_structure(data_path / "assets", data_path / "assets")
    return code_0(Tree)


@app.route("/api/picture/<path:path>")
def send_report(path):
    return send_from_directory(str(data_path / "assets"), path)


@app.route("/api/meta/<path:path>")
def get_meta(path):
    try:
        with (data_path / "assets" / path).with_suffix(".json").open("r") as f:
            meta = json.load(f)
        return code_0(meta)
    except FileNotFoundError:
        return internal_error(f"不存在 {path} 对应的meta文件，请考虑Update Tree List")
    except Exception as e:
        return internal_error(e.__repr__())


@app.route("/api/models/list")
def model_list():
    return code_0(
        ModelInfo
    )


@app.route("/api/task/<model>/<path:path>")
def submit(path, model):
    img_path = data_path / "assets" / path
    try:
        # 判断是否预测过
        with img_path.with_suffix(".json").open("r") as f:
            meta = json.load(f)

        if meta["result"][model]["status"] in ["Waiting", "Predict", "Finish"]:
            return NotAllowed(f"{path} -> {model}模型已在队列中:{meta['result'][model]['status']}")
    except KeyError:
        pass
    except Exception as e:
        return internal_error(e.__repr__())
    finally:
        del meta  # 释放内存

    try:
        assert img_path.exists(), "FileNotFound"
        # Running_Tasks.append(
        #     StreamerMap[model].submit(
        #         [img_path]
        #     )
        # )
        glaucoma.predict([img_path])
        print(f"{path} to {model} 未被预测，添加到队列中...")
        # change_status([img_path], model, "Waiting")
        return code_0(None, msg="Successfully created prediction task")
    except Exception as e:
        return internal_error(e.__repr__())


@app.route('/api/upload', methods=['GET', 'POST'])
def uploader():
    f = request.files['file']
    print(request.files)
    if f.filename.rsplit(".", 1)[-1] in ["png", "jpg"]:
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        return code_0("文件成功上传")
    else:
        return {
            "code": 405,
            "data": None,
            "error": f"拓展名{f.filename.rsplit('.', 1)[-1]}似乎不是图片类型哦",
        }


if __name__ == '__main__':
    data_path = Path(r"../data")
    Tree = search_assets_structure(data_path / "assets", data_path / "assets")
    print(Tree)
    StreamerMap: Dict[str, ThreadedStreamer] = {
        # "Yolov5s": ConstructModelPipe(Yolov5s(data_path / "models")),
        "Pneumonia": ConstructModelPipe(Pneumonia())
    }
    ModelInfo: Dict[str, Dict[str, str]] = {
        # "Yolov5s": {"name": "Yolov5s", "model": "Yolov5s", "category": "disease"},
        "Pneumonia": {"name": "Pneumonia", "model": "ResNet152", "category": "disease"}
    }
    app.config['UPLOAD_FOLDER'] = str(data_path / "assets")
    # 启动后台服务器
    app.run(host="0.0.0.0", port=21335)
