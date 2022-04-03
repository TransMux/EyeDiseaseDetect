<template>
  <div class="table-tree-container">
    <div class="list-tree-wrapper">
      <div class="list-tree-operator">
        <t-input v-model="filterText" clearable placeholder="请输入关键词" @change="onInput">
          <template #prefix-icon>
            <search-icon size="20px" />
          </template>
        </t-input>
        <t-tree
          :data="TREE_DATA"
          activable
          hover
          expand-on-click-node
          :expand-level="1"
          :loading="dataLoading"
          @active="handleTreeActive"
        />
      </div>
      <div class="list-tree-content">
        <Tabs />
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { SearchIcon } from 'tdesign-icons-vue-next';
import { TreeNodeValue } from 'tdesign-vue-next';
// import { TREE_DATA } from './constants';
import Tabs from '../components/tabs.vue';
import request from '@/utils/request';

function handleTreeActive(v: TreeNodeValue) {
  console.log('Tree Active', v);
}

const filterByText = ref();
const filterText = ref();

const dataLoading = ref(false);

const TREE_DATA = ref([]);

interface ResDataType {
  code: number;
  data: any;
  msg: string;
}

const fetchData = async () => {
  dataLoading.value = true;
  try {
    const res: ResDataType = await request.get('/api/tree-list');
    if (res.code === 0) {
      console.log(res);

      // const { list = [] } = res.data;
      TREE_DATA.value = res.data;
    }
  } catch (e) {
    console.log(e);
  } finally {
    dataLoading.value = false;
  }
};

onMounted(() => {
  fetchData();
});

const onInput = () => {
  console.log('OnSearchKeyChange');

  filterByText.value = (node) => {
    const rs = node.label.indexOf(filterText.value) >= 0;
    return rs;
  };
};
</script>
<style lang="less" scoped>
@import "@/style/variables.less";
.table-tree-container {
  background-color: @bg-color-container;
  border-radius: @border-radius;

  .t-tree {
    margin-top: 24px;
  }
}

.list-tree-wrapper {
  overflow-y: hidden;
}

.list-tree-operator {
  width: 200px;
  float: left;
  padding: 30px 32px;
}

.list-tree-content {
  border-left: 1px solid @border-level-1-color;
  overflow: auto;
}
</style>
