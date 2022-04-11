<template>
  <div class="list-common-table">
    <div class="table-container">
      <t-table :data="data" :columns="COLUMNS" :row-key="rowKey" :vertical-align="verticalAlign" :hover="hover">
        <template #status="{ row }">
          <t-tag v-if="row.status === '失败'" theme="danger" variant="light"> 审核失败 </t-tag>
          <t-tag v-if="row.status === CONTRACT_STATUS.AUDIT_PENDING" theme="warning" variant="light"> 待审核 </t-tag>
          <t-tag v-if="row.status === CONTRACT_STATUS.EXEC_PENDING" theme="warning" variant="light"> 待履行 </t-tag>
          <t-tag v-if="row.status === CONTRACT_STATUS.EXECUTING" theme="success" variant="light"> 履行中 </t-tag>
          <t-tag v-if="row.status === CONTRACT_STATUS.FINISH" theme="success" variant="light"> 已完成 </t-tag>
        </template>
        <template #paymentType="{ row }">
          <p v-if="row.paymentType === CONTRACT_PAYMENT_TYPES.PAYMENT" class="payment-col">
            付款
            <trend class="dashboard-item-trend" type="up" />
          </p>
          <p v-if="row.paymentType === CONTRACT_PAYMENT_TYPES.RECIPT" class="payment-col">
            收款
            <trend class="dashboard-item-trend" type="down" />
          </p>
        </template>
      </t-table>
    </div>
  </div>
</template>
<script setup lang="ts">
import { inject, ref, watch } from 'vue';
import Trend from '@/components/trend/index.vue';
import { CONTRACT_STATUS, CONTRACT_PAYMENT_TYPES } from '@/constants';
import { SingleEyeImg, Predict, Model } from '../types';

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
    title: '理论支持',
    width: 400,
    ellipsis: true,
    colKey: 'theory',
  },
  {
    title: '置信度',
    width: 200,
    ellipsis: true,
    colKey: 'confidence',
  },
  { title: '检测状态', colKey: 'status', width: 200, cell: { col: 'status' } },

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
