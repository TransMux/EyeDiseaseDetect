from pathlib import Path
from typing import List

import torch

from EyeDiseaseDetect.Models.ModelConstructor import BaseModel
from EyeDiseaseDetect.Models.utils import change_status, update_meta, predict_result_template


class Yolov5s(BaseModel):
    def __init__(self, model_path):
        self.model_path: Path = model_path
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=self.model_path / 'hub/yolov5s.pt')

    def predict(self, data_paths: List[Path]) -> List:
        change_status(data_paths, self.__class__.__name__, "Predict")
        result = self.model(data_paths)
        # TODO: 这里只能是临时展示 batch * count * result
        # 1 * 1 * 6 需要把前面两个1 flatten 一下
        for i, r in enumerate(result.xyxyn[0]):
            update_meta(
                data_paths[i],
                self.__class__.__name__,
                predict_result_template(
                    status="Finish",
                    x1=float(r[0]),
                    y1=float(r[1]),
                    x2=float(r[2]),
                    y2=float(r[3]),
                    confidence=float(r[4]),
                    label=result.names[int(r[5])]
                )
            )
        return result.xyxyn
