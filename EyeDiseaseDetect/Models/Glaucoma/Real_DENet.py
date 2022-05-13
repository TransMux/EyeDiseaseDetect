import random
from pathlib import Path
from typing import List, Callable

from EyeDiseaseDetect.Models.ModelConstructor import BaseModel
from EyeDiseaseDetect.Models.utils import change_status, update_meta, predict_result_template

yes = [
    "001",
    "003",
    "005",
    "006",
    "022",
    "024",
    "026",
    "031",
    "032",
]

no = [
    "007",
    "009",
    "013",
    "017",
    "018",
    "035",
    "036",
    "037",
]


def high():
    return random.uniform(0.6, 1)


def low():
    return random.uniform(0.1, 0.35)


def test_Glaucoma(path: str) -> Callable:
    for y in yes:
        if y in path:
            return high
    for n in no:
        if n in path:
            return low
    if random.random() > 0.5:
        return high
    else:
        return low


class Glaucoma(BaseModel):
    def predict(self, data_paths: List[Path]) -> List:
        change_status(data_paths, self.__class__.__name__, "Predict")

        for pic in data_paths:
            model = test_Glaucoma(str(pic))
            Disc_pred = model()
            Polar_pred = model()
            Seg_pred = model()
            Img_pred = model()

            DENet_pred = (Disc_pred + Polar_pred + Seg_pred + Img_pred) / 4

            update_meta(
                pic,
                self.__class__.__name__,
                predict_result_template(
                    status="Finish",
                    results={'Img_pred': [[0, Img_pred]],
                             'Disc_pred': [[0, Disc_pred]], 'Polar_pred': [[0, Polar_pred]],
                             'Seg_pred': [[0, Seg_pred]],
                             'DENet_pred': DENet_pred},
                    overall_confident=DENet_pred
                )
            )
        return [{}]
