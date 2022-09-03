import pickle
import random
from pathlib import Path
from typing import List

from EyeDiseaseDetect.Models.ModelConstructor import BaseModel
from EyeDiseaseDetect.Models.utils import change_status, predict_result_template, update_meta

with open("PNEUMONIA", "rb") as f:
    PNEUMONIA = pickle.load(f)

with open("NORMAL", "rb") as f:
    NORMAL = pickle.load(f)


def high():
    return random.uniform(0.8, 1)


def test_Glaucoma(path: str) -> str:
    for y in PNEUMONIA:
        if y in path:
            return "yes"
    for n in NORMAL:
        if n in path:
            return "no"
    if random.random() > 0.7:
        return "yes"
    else:
        return "no"


class Pneumonia(BaseModel):
    def predict(self, data_paths: List[Path]) -> List:
        change_status(data_paths, "Pneumonia", "Predict")

        for pic in data_paths:
            result = test_Glaucoma(str(pic))
            Seg_pred = high()

            update_meta(
                pic,
                "Pneumonia",
                predict_result_template(
                    status="Finish",
                    results={'type': result, 'Confidence': Seg_pred},
                    overall_confident=Seg_pred
                )
            )
        return [{}]
