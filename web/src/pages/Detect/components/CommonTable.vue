<template>
  <t-tabs v-model="value">
    <t-tab-panel :value="1">
      <template #label> <t-icon name="scan" class="tabs-icon-margin" /> 病变特征检测 </template>
      <featureVue />
    </t-tab-panel>
    <t-tab-panel :value="2">
      <template #label> <t-icon name="chart-bubble" class="tabs-icon-margin" /> 疾病风险评估 </template>
      <diseaseVue />
    </t-tab-panel>
  </t-tabs>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import diseaseVue from './disease.vue';
import featureVue from './feature.vue';

const value = ref(1);
</script>

<style>
.t-tabs__nav-item {
  padding-right: 120px;
  padding-left: 120px;
}

.tabs-icon-margin {
  margin-right: 4px;
}

.t-tabs__nav-wrap {
  margin: auto;
}
</style>
