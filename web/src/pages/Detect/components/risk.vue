<template>
  <div class="list-common-table">
    <div class="table-container">
      <t-table
        :data="data"
        :columns="COLUMNS"
        :row-key="rowKey"
        :vertical-align="verticalAlign"
        :hover="hover"
        :pagination="pagination"
        :loading="dataLoading"
        @page-change="rehandlePageChange"
        @change="rehandleChange"
      >
        <template #status="{ row }">
          <t-tag v-if="row.status === '失败'" theme="danger" variant="light"> 审核失败 </t-tag>
          <t-tag v-if="row.status === CONTRACT_STATUS.AUDIT_PENDING" theme="warning" variant="light"> 待审核 </t-tag>
          <t-tag v-if="row.status === CONTRACT_STATUS.EXEC_PENDING" theme="warning" variant="light"> 待履行 </t-tag>
          <t-tag v-if="row.status === CONTRACT_STATUS.EXECUTING" theme="success" variant="light"> 履行中 </t-tag>
          <t-tag v-if="row.status === CONTRACT_STATUS.FINISH" theme="success" variant="light"> 已完成 </t-tag>
        </template>
        <template #contractType="{ row }">
          <p v-if="row.contractType === CONTRACT_TYPES.MAIN">审核失败</p>
          <p v-if="row.contractType === CONTRACT_TYPES.SUB">待审核</p>
          <p v-if="row.contractType === CONTRACT_TYPES.SUPPLEMENT">待履行</p>
        </template>
        <template #paymentType="{ row }">
          <p v-if="row.paymentType === CONTRACT_PAYMENT_TYPES.PAYMENT" class="payment-col">
            付款<trend class="dashboard-item-trend" type="up" />
          </p>
          <p v-if="row.paymentType === CONTRACT_PAYMENT_TYPES.RECIPT" class="payment-col">
            收款<trend class="dashboard-item-trend" type="down" />
          </p>
        </template>
        <!-- <template #op="slotProps">
          <a class="t-button-link" @click="rehandleClickOp(slotProps)">管理</a>
          <a class="t-button-link" @click="handleClickDelete(slotProps)">删除</a>
        </template> -->
      </t-table>
      <!-- <t-dialog
        v-model:visible="confirmVisible"
        header="确认删除当前所选合同？"
        :body="confirmBody"
        :on-cancel="onCancel"
        @confirm="onConfirmDelete"
      /> -->
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { MessagePlugin } from 'tdesign-vue-next';
import Trend from '@/components/trend/index.vue';
import request from '@/utils/request';
import { ResDataType } from '@/interface';

import { CONTRACT_STATUS, CONTRACT_TYPES, CONTRACT_PAYMENT_TYPES } from '@/constants';

const COLUMNS = [
  {
    title: '疾病名称',
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

const pagination = ref({
  defaultPageSize: 20,
  total: 100,
  defaultCurrent: 1,
});
// const confirmVisible = ref(false);

const data = ref([]);

const dataLoading = ref(false);
const fetchData = async () => {
  dataLoading.value = true;
  try {
    const res: ResDataType = await request.get('http://43.138.152.86:21335/api/get-list');
    if (res.code === 0) {
      const { list = [] } = res.data;
      data.value = list;
      pagination.value = {
        ...pagination.value,
        total: list.length,
      };
    }
  } catch (e) {
    console.log(e);
  } finally {
    dataLoading.value = false;
  }
};

// const deleteIdx = ref(-1);
// const confirmBody = computed(() => {
//   if (deleteIdx.value > -1) {
//     const { name } = data.value[deleteIdx.value];
//     return `删除后，${name}的所有合同信息将被清空，且无法恢复`;
//   }
//   return '';
// });

// const resetIdx = () => {
//   deleteIdx.value = -1;
// };

// const onConfirmDelete = () => {
//   // 真实业务请发起请求
//   data.value.splice(deleteIdx.value, 1);
//   pagination.value.total = data.value.length;
//   confirmVisible.value = false;
//   MessagePlugin.success('删除成功');
//   resetIdx();
// };

// const onCancel = () => {
//   resetIdx();
// };

onMounted(() => {
  fetchData();
});

const rehandlePageChange = (curr, pageInfo) => {
  console.log('分页变化', curr, pageInfo);
};
const rehandleChange = (changeParams, triggerAndData) => {
  console.log('统一Change', changeParams, triggerAndData);
};
</script>

<style lang="less">
@import './basic.less';
</style>
