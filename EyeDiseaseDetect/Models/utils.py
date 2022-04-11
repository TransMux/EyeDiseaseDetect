import json
from pathlib import Path
from typing import List


def predict_result_template(
        name=None,
        model=None,
        status=None,
        x1=None,
        y1=None,
        x2=None,
        y2=None,
        disease=None,
        confidence=None
):
    return {
        "name": name,
        "model": model,
        "status": status,
        "x1": x1,
        "y1": y1,
        "x2": x2,
        "y2": y2,
        "disease": disease,
        "confidence": confidence
    }


def change_status(data_path: List[Path], model_name: str, status: str) -> None:
    assert status in ["Waiting", "Predict", "Finish"]

    for file in data_path:
        with file.with_suffix(".json").open("r") as f:
            data = json.load(f)
        try:
            data["result"][model_name]["status"] = status
        except KeyError:
            data["result"][model_name] = predict_result_template(status=status)
        with file.with_suffix(".json").open("w") as f:
            json.dump(data, f)


def update_meta(data_path: List[Path], model_name: str, data: dict):
    for file in data_path:
        with file.with_suffix(".json").open("r") as f:
            origin = json.load(f)
        for key, value in data.items():
            if value is not None:
                # 更新值
                origin[key] = value
        with file.with_suffix(".json").open("w") as f:
            json.dump(data, f)
