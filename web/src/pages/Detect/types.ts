export interface SingleEyeImg {
  label: string;
  value: string; // 图片对应地址
  children: SingleEyeImg | null; // 如果是null则说明是图片
  meta: any; // meta data
}
