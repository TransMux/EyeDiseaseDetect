<template>
  <div class="list-common-table">
    <div class="table-container">
      <t-table :data="props.disease" :columns="COLUMNS" :row-key="rowKey" :vertical-align="verticalAlign"
        :hover="hover">
        <template #status="{ row }">
          <t-tag v-if="row.status === 'Waiting'" theme="warning" variant="light"> 排队中 </t-tag>
          <t-tag v-if="row.status === 'Predict'" theme="danger" variant="light"> 预测中 </t-tag>
          <t-tag v-if="row.status === 'Finish'" theme="success" variant="light"> 已完成 </t-tag>
        </template>
      </t-table>
    </div>
  </div>
</template>
<script setup lang="ts">
import { inject, ref, watch } from 'vue';
import { SingleEyeImg, Predict } from '../types';

const OpeingImg: { value: SingleEyeImg } = inject('OpeningImg');

const props = defineProps<{
  disease: Predict[];
}>();

console.log(props);

watch(OpeingImg, () => {
  console.log(OpeingImg);
});

const COLUMNS = [
  {
    title: '检测项目',
    fixed: 'left',
    minWidth: '200',
    align: 'left',
    colKey: 'name',
  },
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
  { title: '任务状态', colKey: 'status', width: 200, cell: { col: 'status' } },

  // {
  //   title: '合同收付类型',
  //   width: 200,
  //   ellipsis: true,
  //   colKey: 'paymentType',
  // },
  // {
  //   title: '合同金额 (元)',
  //   width: 200,
  //   ellipsis: true,
  //   colKey: 'amount',
  // },
  // {
  //   align: 'left',
  //   fixed: 'right',
  //   width: 200,
  //   colKey: 'op',
  //   title: '操作',
  // },
];

const rowKey = 'index';
const verticalAlign = 'top';
const hover = true;
// const confirmVisible = ref(false);

const data = ref([]);

const dataLoading = ref(false);
</script>

<style lang="less">
@import './basic.less';
</style>
