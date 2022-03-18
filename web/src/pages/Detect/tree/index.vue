<template>
  <div class="table-tree-container">
    <div class="list-tree-wrapper">
      <div class="list-tree-operator">
        <t-input v-model="filterText" clearable placeholder="请输入关键词" @change="onInput">
          <template #prefix-icon>
            <search-icon size="20px" />
          </template>
        </t-input>
        <t-tree :data="TREE_DATA" activable hover expand-on-click-node :expand-level="1" @active="handleTreeActive" />
      </div>
      <div class="list-tree-content">
        <common-table />
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref } from 'vue';
import { SearchIcon } from 'tdesign-icons-vue-next';
import { TreeNodeValue } from 'tdesign-vue-next';
import { TREE_DATA } from './constants';
import CommonTable from '../components/CommonTable.vue';

function handleTreeActive(v: TreeNodeValue) {
  console.log('Tree Active', v);
}

const filterByText = ref();
const filterText = ref();

const onInput = () => {
  console.log('OnSearchKeyChange');

  filterByText.value = (node) => {
    const rs = node.label.indexOf(filterText.value) >= 0;
    return rs;
  };
};
</script>
<style lang="less" scoped>
@import '@/style/variables.less';
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
