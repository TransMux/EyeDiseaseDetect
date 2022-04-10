from pathlib import Path
from typing import List

from service_streamer import ThreadedStreamer


class BaseModel:
    """Interface"""
    worker_num: int = 4
    batch: int = 10
    latency: float = 1

    def predict(self, data_paths: List[Path]) -> List:
        # 也可能不会有返回值
        # self.change_status(data_paths, "Predict")
        # predict = self._predict(data_paths)
        # self.write_predict_result(data_paths, predict)
        # self.change_status(data_paths, "Finish")
        # gc.collect()
        # return predict
        raise NotImplementedError()


def ConstructModelPipe(model: BaseModel):
    streamer = ThreadedStreamer(model.predict, model.batch, model.latency)
    return streamer
