export interface Predict {
  model: string;
  status: 'Waiting' | 'Predict' | 'Finish';
  x1: number;
  y1: number;
  x2: number;
  y2: number;
  label: string;
  confidence: number;
}

interface PicData {
  // eslint-disable-next-line camelcase
  create_time: number;
  result: Predict[]; // meta data
}

export interface SingleEyeImg {
  label: string;
  value: string; // 图片对应地址
  children: SingleEyeImg | null; // 如果是null则说明是图片
  meta: PicData;
}
