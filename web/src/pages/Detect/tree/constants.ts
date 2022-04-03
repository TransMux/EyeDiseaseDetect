// TODO：后端返回
export const TREE_DATA = [
  {
    label: '3月17日患者',
    value: 0,
    children: [
      {
        label: '本科室',
        value: '0-0',
      },
      {
        label: '其他科室',
        value: '0-1',
        children: [
          {
            label: '患者A',
            value: '0-1-0',
          },
          {
            label: '患者B',
            value: '患者B',
          },
        ],
      },
    ],
  },
  {
    label: '3月16日患者',
    value: 1,
    children: [
      {
        label: '本科室',
        value: '1-0',
      },
      {
        label: '其他科室',
        value: '1-1',
      },
    ],
  },
  {
    label: '数据集',
    value: 2,
    children: [
      {
        label: 'OIA-ODIR',
        value: '2-0',
      },
      {
        label: 'kaggle',
        value: '2-1',
        children: [
          {
            label: '1.jpg',
            value: '2-1-0',
          },
          {
            label: '2.jpg',
            value: '2-1-1',
          },
        ],
      },
    ],
  },
];
