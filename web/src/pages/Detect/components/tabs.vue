<template>
  <!-- <img src="@/assets/17_right.jpeg" class="disease_pic" /> -->

  <div id="label-img" class="disease_pic"></div>

  <t-tabs v-model="value">
    <t-tab-panel :value="1">
      <template #label>
        <t-icon name="scan" class="tabs-icon-margin" />病变特征检测
      </template>
      <featureVue />
    </t-tab-panel>
    <t-tab-panel :value="2">
      <template #label>
        <t-icon name="chart-bubble" class="tabs-icon-margin" />疾病风险评估
      </template>
      <diseaseVue />
    </t-tab-panel>
  </t-tabs>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import LabelImg from 'label-img';
import diseaseVue from './disease.vue';
import featureVue from './feature.vue';
const Shape = LabelImg.Shape

onMounted(() => {
  const labelImgElement = document.getElementById('label-img');

  const labeler = new LabelImg(<HTMLDivElement>labelImgElement, {
    width: 800,
    height: 600,
    bgColor: `#000`, // 背景色
    imagePlacement: 'default', // default | center
  });
  // https://github.com/hold-baby/label-img
  labeler.load('./src/assets/17_right.jpeg');

  // 注册图形
  labeler.register('polygon', {
    name: 'Hello',
    type: 'Polygon',
    tag: '多边形',
  });
  // 加载图片
  // 选择标注多边形 
  // labeler.label('polygon');
});



const value = ref(1);
</script>

<style>
.disease_pic {
  margin: auto;
  left: 25%;
  margin-top: 30px;
  margin-bottom: 30px;
}

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
