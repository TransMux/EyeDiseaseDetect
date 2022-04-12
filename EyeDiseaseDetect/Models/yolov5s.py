from pathlib import Path
from typing import List

import torch
from PIL import Image

from EyeDiseaseDetect.Models.ModelConstructor import BaseModel
from EyeDiseaseDetect.Models.utils import change_status, update_meta, predict_result_template, label_template


class Yolov5s(BaseModel):
    def __init__(self, model_path):
        self.model_path: Path = model_path
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=self.model_path / 'hub/yolov5s.pt')

    def predict(self, data_paths: List[Path]) -> List:
        change_status(data_paths, self.__class__.__name__, "Predict")
        result = self.model(data_paths)
        names = result.names
        cors = result.xyxyn
        # TODO: 这里只能是临时展示 batch * count * result
        # 1 * 1 * 6 需要把前面两个1 flatten 一下
        labels = []
        for i, batch in enumerate(cors):
            with Image.open(data_paths[i]) as img:
                width, height = img.size
            overall_confident = 0
            for label in batch:
                overall_confident += float(label[4])

                x1 = float(label[0]) * width
                y1 = float(label[1]) * height
                x2 = float(label[2]) * width
                y2 = float(label[3]) * height
                labels.append(
                    label_template(
                        shape="Ract",
                        positions=[
                            [x1, y1, ], [x2, y1], [x2, y2], [x1, y2]
                        ],
                        confidence=float(label[4]),
                        label=names[int(label[5])]
                    )
                )
            overall_confident = overall_confident / len(batch)
            update_meta(
                data_paths[i],
                self.__class__.__name__,
                predict_result_template(
                    status="Finish",
                    results=labels,
                    overall_confident=overall_confident
                )
            )
        return result.xyxyn
