<template>
  <div class="list-common-table">
    <div class="table-container">
      <t-table :data="data" :columns="COLUMNS" :row-key="rowKey" :vertical-align="verticalAlign" :hover="hover">
        <template #status="{ row }">
          <t-tag v-if="row.status === 'Waiting'" theme="warning" variant="light"> 排队中 </t-tag>
          <t-tag v-if="row.status === 'Predict'" theme="danger" variant="light"> 预测中 </t-tag>
          <t-tag v-if="row.status === 'Finish'" theme="success" variant="light"> 已完成 </t-tag>
          <t-tag v-if="row.status === 'Unpredicted'" theme="danger" variant="light"> 未预测 </t-tag>
        </template>
        <template #op="{ row }">
          <t-button v-if="row.status === 'Unpredicted'" theme="default"> 预测 </t-button>
          <t-button v-if="row.status === 'Finish'" theme="success"> 聚焦 </t-button>
        </template>
      </t-table>
    </div>
  </div>
</template>
<script setup lang="ts">
import { inject, ref, watch, watchEffect } from 'vue';
import { SingleEyeImg, Predict, ListData, Model } from '../types';

const OpeningImg: { value: SingleEyeImg } = inject('OpeningImg');

const props = defineProps<{
  models: Model[];
}>();

console.log(props);

const data = ref<ListData[]>([]);

watchEffect(() => {
  console.log('Disease:开始映射数据');

  data.value = [];
  props.models.forEach((model) => {
    if (model.model in OpeningImg.value.meta.result) {
      data.value.push({
        name: model.name,
        confidence: OpeningImg.value.meta.result[model.model].confidence,
        status: OpeningImg.value.meta.result[model.model].status,
      });
    } else {
      data.value.push({
        name: model.name,
        // confidence: 0,
        status: 'Unpredicted',
      });
    }
  });
});

const COLUMNS = [
  {
    title: '检测项目',
    fixed: 'left',
    minWidth: '200',
    align: 'left',
    colKey: 'name',
  },
  { title: '任务状态', colKey: 'status', width: 200, cell: { col: 'status' } },
  {
    title: '预测结果',
    width: 200,
    ellipsis: true,
    colKey: 'label',
  },
  {
    title: '置信度',
    width: 200,
    ellipsis: true,
    colKey: 'confidence',
  },
  { title: '操作', colKey: 'op', width: 200, cell: { col: 'status' } },
];

const rowKey = 'index';
const verticalAlign = 'top';
const hover = true;
</script>

<style lang="less">
@import './basic.less';
</style>
