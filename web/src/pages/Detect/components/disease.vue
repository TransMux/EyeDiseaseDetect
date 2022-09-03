<template>
  <t-message v-if="isShowMsg" :close-btn="true" @close-btn-click="isShowMsg = false">
    {{ msg }}
  </t-message>
  <div class="list-common-table">
    <div class="table-container">
      <t-table :data="data" :columns="COLUMNS" :row-key="rowKey" :vertical-align="verticalAlign" :hover="hover"
               :expanded-row-keys="expandedRowKeys"
               expand-on-row-click
               :expand-icon="false"
               @expand-change="rehandleExpandChange"
      >
        <template #result="{ row }">
          <t-tag v-if="row.results === 'yes'" theme="warning" variant="light"> 患病</t-tag>
          <t-tag v-else-if="row.results === 'no'" theme="success" variant="light"> 健康</t-tag>
          <t-button v-else theme="default" @click="requestPredict(row)"> 预测</t-button>
        </template>
        <template #status="{ row }">
          <t-tag v-if="row.status === 'Waiting'" theme="warning" variant="light"> 排队中</t-tag>
          <t-tag v-if="row.status === 'Predict'" theme="warning" variant="light"> 预测中</t-tag>
          <t-tag v-if="row.status === 'Finish'" theme="success" variant="light"> 已完成</t-tag>
          <t-tag v-if="row.status === 'Unpredicted'" theme="danger" variant="light"> 未预测</t-tag>
        </template>
      </t-table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { inject, ref, watch, watchEffect } from 'vue';
import { MessagePlugin } from 'tdesign-vue-next';
import { ResDataType } from '@/interface';
import request from '@/utils/request';
import { SingleEyeImg, Predict, ListData, Model } from '../types';

const OpeningImg: { value: SingleEyeImg } = inject('OpeningImg');

const isShowMsg = ref(false);
const msg = ref('');

const props = defineProps<{
  models: Model[];
}>();

console.log(props);

const requestPredict = async (raw: ListData) => {
  console.log(raw);
  try {
    const res: ResDataType = await request.get(`http://localhost:21335/api/task/Pneumonia/${raw.path}`);
    if (res.code === 0) {
      MessagePlugin.info(res.msg);
      raw.status = 'Predict';
    } else {
      MessagePlugin.error(res.msg);
    }
  } catch (e) {
    console.log(e);
  }
};

const data = ref<ListData[]>([]);


const expandedRowKeys = ref([""]);
const rehandleExpandChange = (value, {expandedRowData}) => {
  expandedRowKeys.value = value;
  console.log('rehandleExpandChange', value, expandedRowData);
};

const rowKey = 'index';
const verticalAlign = 'top';
const hover = true;

const focus = inject<CallableFunction>('focus');


watchEffect(() => {
  console.log('Disease:开始映射数据');
  expandedRowKeys.value = [""]

  data.value = [];
  props.models.forEach((model) => {
    // console.log(model.model)
    if ("Pneumonia" in OpeningImg.value.meta.result) {
      data.value.push({
        name: "肺炎 Pneumonia",
        model: "ResNet",
        assay: "Deep Residual Learning for Image Recognition",
        confidence: OpeningImg.value.meta.result["Pneumonia"].overall_confident,
        status: OpeningImg.value.meta.result["Pneumonia"].status,
        path: OpeningImg.value.value,
        results: OpeningImg.value.meta.result["Pneumonia"].results.type,
      });
    } else {
      data.value.push({
        name: "肺炎 ResNet",
        model: "ResNet",
        assay: "Deep Residual Learning for Image Recognition",
        // confidence: 0,
        status: 'Unpredicted',
        path: OpeningImg.value.value,
      });
    }
  });
});

const COLUMNS = [
  {
    title: '检测项目',
    fixed: 'left',
    align: 'left',
    colKey: 'name',
  },
  {
    title: '理论支持',
    fixed: 'left',
    minWidth: '400',
    align: 'left',
    colKey: 'assay',
  },
  {
    title: '预测模型',
    colKey: 'model',
  },
  {title: '任务状态', colKey: 'status', width: 200, cell: {col: 'status'}},
  {title: '结果', colKey: 'result', width: 200, cell: {col: 'results'}},
  {
    title: '置信度',
    width: 200,
    ellipsis: true,
    colKey: 'confidence',
  },
];
</script>

<style lang="less">
@import './basic.less';
</style>
