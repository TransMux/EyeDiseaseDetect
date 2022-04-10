from pathlib import Path
from typing import List

import torch

from EyeDiseaseDetect.Models.ModelConstructor import BaseModel
from EyeDiseaseDetect.Models.utils import change_status


class Yolov5s(BaseModel):
    def __init__(self, model_path):
        self.model_path: Path = model_path
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=self.model_path / 'hub/yolov5s.pt')

    def predict(self, data_paths: List[Path]) -> List:
        change_status(data_paths, self.__class__.__name__, "Predict")
        result = self.model(data_paths).xyxy
        change_status(data_paths, self.__class__.__name__, "Finish")
        return result
