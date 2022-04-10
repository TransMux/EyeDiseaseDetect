from abc import ABC
from pathlib import Path
from typing import List

from service_streamer import ThreadedStreamer, ManagedModel, Streamer


class BaseModel(ManagedModel, ABC):
    """Interface"""
    worker_num: int = 4
    batch: int = 1
    latency: float = 0.1

    def predict(self, data_paths: List[Path]) -> List:
        # 也可能不会有返回值
        self.change_status(data_paths, "Predict")
        predict = self._predict(data_paths)
        self.write_predict_result(data_paths, predict)
        self.change_status(data_paths, "Finish")

        pass

    def _predict(self, data_paths: List[Path]) -> List:
        # return self.model.predict(batch)
        raise NotImplementedError()

    def write_predict_result(self, result: List[Path], predicts: List):
        pass

    def change_status(self, data_paths: List[Path], status: str):
        pass


def ConstructModelPipe(model: BaseModel):
    pipe = Streamer(model, model.batch, model.latency, worker_num=model.worker_num)
    streamer = ThreadedStreamer(pipe.predict, model.batch, model.latency)
    return streamer
