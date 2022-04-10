from pathlib import Path
from typing import List

import torch

from EyeDiseaseDetect.Models.ModelConstructor import BaseModel


class Yolov5s(BaseModel):

    def _predict(self, data_paths: List[Path]) -> List:
        return self.model(data_paths)

    def init_model(self, *args, **kwargs):
        # model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True, verbose=True)
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path='data/models/hub/yolov5s.pt')
