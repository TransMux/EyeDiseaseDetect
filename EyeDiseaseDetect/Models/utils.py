import json
from pathlib import Path
from typing import List


def label_template(
        shape=None,
        positions: List = None,
        label=None,
        confidence=None
):
    return {
        "shape": shape,
        "positions": positions,
        "label": label,
        "confidence": confidence
    }


def predict_result_template(
        model=None,
        status=None,
        results=None,
        overall_confident=None,
):
    return {
        "model": model,
        "status": status,
        "results": results,
        "overall_confident": overall_confident
    }


def change_status(data_path: List[Path], model_name: str, status: str) -> None:
    assert status in ["Waiting", "Predict", "Finish"]

    for file in data_path:
        with file.with_suffix(".json").open("r") as f:
            data = json.load(f)
        try:
            data["result"][model_name]["status"] = status
        except KeyError:
            data["result"][model_name] = predict_result_template(status=status, model=model_name)
        with file.with_suffix(".json").open("w") as f:
            json.dump(data, f)


def update_meta(file: Path, model_name: str, data: dict):
    with file.with_suffix(".json").open("r") as f:
        origin = json.load(f)
    for key, value in data.items():
        if value is not None:
            # 更新值
            origin["result"][model_name][key] = value
    with file.with_suffix(".json").open("w") as f:
        json.dump(origin, f)
