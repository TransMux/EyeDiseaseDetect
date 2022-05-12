import os
from pathlib import Path
from typing import Sequence

from PIL import Image
from flask import Flask, send_from_directory, request
from flask_cors import CORS
from werkzeug.utils import secure_filename

# from EyeDiseaseDetect.Models.ModelConstructor import ConstructModelPipe
# from EyeDiseaseDetect.Models.utils import change_status
# from EyeDiseaseDetect.Models.yolov5s import Yolov5s
from EyeDiseaseDetect.Responses import code_0, internal_error
from EyeDiseaseDetect.utils import search_assets_structure
from EyeNew.FileScan import get_meta_info

app = Flask(__name__)
cors = CORS(app, supports_credentials=True)

# 异步预测
Running_Tasks = []
HOME = Path(r"E:\competition\EyeDiseaseDetect\data")
ASSETS = HOME / "assets"
Tree = search_assets_structure(ASSETS, ASSETS)


@app.route("/api/tree/list")
def get_tree_data():
    if Tree is None:
        return internal_error("图片树未初始化")
    return code_0(Tree)


@app.route("/api/tree/update")
def resync():
    global Tree
    Tree = search_assets_structure(ASSETS, ASSETS)
    return code_0(Tree)


@app.route("/api/picture/<path:path>")
def send_pic(path):
    return send_from_directory(ASSETS, path)


@app.route("/api/meta/<path:path>")
def get_meta(path):
    return get_meta_info(path, ASSETS)


@app.route("/api/crop/<path:path>")
def add_new_crop(path):
    pos: Sequence[Sequence[int]] = request.args.get("positions")
    label: str = request.args.get("label")

    img_path = ASSETS / path
    save_folder = img_path.with_suffix(".crop")
    positions = [str(pos[0][0]),
                 str(pos[0][1]),
                 str(pos[2][0]),
                 str(pos[2][1])]
    save_path = save_folder / f"血管瘤_{label}_原图_{'_'.join(positions)}.jpg"

    img = Image.open(img_path)
    print("裁剪：", img.size)
    cropped = img.crop((*pos[0], *pos[2]))
    cropped.save(save_path)
    return save_path.relative_to(ASSETS)


# @app.route("/api/models/list")
# def model_list():
#     return code_0(
#         ModelInfo
#     )


# @app.route("/api/task/<model>/<path:path>")
# def submit(path, model):
#     img_path = data_path / "assets" / path
#     try:
#         # 判断是否预测过
#         with img_path.with_suffix(".json").open("r") as f:
#             meta = json.load(f)
#
#         if meta["result"][model]["status"] in ["Waiting", "Predict", "Finish"]:
#             return NotAllowed(f"{path} -> {model}模型已在队列中:{meta['result'][model]['status']}")
#     except KeyError:
#         pass
#     except Exception as e:
#         return internal_error(e.__repr__())
#     finally:
#         del meta  # 释放内存
#
#     try:
#         assert img_path.exists(), "FileNotFound"
#         Running_Tasks.append(
#             StreamerMap[model].submit(
#                 [img_path]
#             )
#         )
#         print(f"{path} to {model} 未被预测，添加到队列中...")
#         change_status([img_path], model, "Waiting")
#         return code_0(None, msg="成功新建异步预测任务")
#     except Exception as e:
#         return internal_error(e.__repr__())


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
    app.config['UPLOAD_FOLDER'] = str(data_path / "assets")
    app.run(port=21335)
