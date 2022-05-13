export interface Predict {
  model: string;
  status: 'Waiting' | 'Predict' | 'Finish';
  confidence: number;
  results: {
    shape: 'Polygon' | 'Ract';
    label: string;
    confidence: number;
    positions: [[number, number], [number, number]];
  }[];
  // name?: string; // 模型外显名称 传到表格中的数据务必保证
}

export interface ListData {
  name: string;
  model: string;
  assay: string;
  confidence?: number;
  status: string;
  path: string;
  results?: {
    shape: 'Polygon' | 'Ract';
    label: string;
    confidence: number;
    positions: [[number, number], [number, number]];
  }[];
}

interface PicData {
  // eslint-disable-next-line camelcase
  create_time: number;
  result: { Any: Predict }; // meta data
}

export interface Model {
  name: string; // 模型外显名称
  model: string;
  category: 'disease' | 'risk'; // 类别
}

export interface SingleEyeImg {
  label: string;
  value: string; // 图片对应地址
  children: SingleEyeImg | null; // 如果是null则说明是图片
  meta: PicData;
}
