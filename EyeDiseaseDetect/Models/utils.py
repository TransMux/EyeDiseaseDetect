import json
from pathlib import Path
from typing import List


def change_status(data_path: List[Path], model_name: str, status: str) -> None:
    assert status in ["Waiting", "Predict", "Finish"]

    for file in data_path:
        with file.with_suffix(".json").open("r") as f:
            data = json.load(f)
        data["result"][model_name] = status
        with file.with_suffix(".json").open("w") as f:
            json.dump(data, f)
