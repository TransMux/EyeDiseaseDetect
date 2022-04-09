<template>
  <div>
    <div>debug: {{ OpeingImg }}</div>

    <div id="label-img" ref="img" class="disease_pic" v-show="OpeingImg"></div>

    <t-tabs v-model="value" v-if="OpeingImg">
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
  </div>
</template>

<script setup lang="ts">
import { inject, onMounted, provide, ref, watch, watchEffect } from 'vue';
import LabelImg from 'label-img';
import diseaseVue from './disease.vue';
import featureVue from './feature.vue';
import { SingleEyeImg } from '../types';

const { Shape } = LabelImg;

// 挂载
let labeler: LabelImg
const img = ref<HTMLDivElement>(null);

// TODO: 解决ref响应式ReplImp的类型问题 ref<SingleEyeImg> 会报 “ref”表示值，但在此处用作类型。是否指“类型 ref”?
const OpeingImg: { value: SingleEyeImg } = inject('OpeningImg');
onMounted(() => {
  // https://github.com/hold-baby/label-img
  labeler = new LabelImg(<HTMLDivElement>img.value, {
    //@ts-ignore
    width: 800,
    height: 600,
    bgColor: `#000`, // 背景色
    //@ts-ignore
    imagePlacement: 'default', // default | center
  });

  // 加载图片
  watch(OpeingImg, () => {
    const url = `http://localhost:21335/api/picture/${OpeingImg.value.value}`
    console.log("<Tabs> Load url:", url);
    labeler.load(url);
  })
})



// // 注册图形
// labeler.value.register('polygon', {
//   name: 'Hello',
//   type: 'Polygon',
//   tag: '多边形',
// });
// 加载图片
// 选择标注多边形
// labeler.label('polygon');


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
