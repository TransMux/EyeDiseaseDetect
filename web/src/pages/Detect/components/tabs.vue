<template>
  <div>
    <!-- <div class="controls">
      <t-button theme="default" variant="outline" @click="props.update"> 刷新数据 </t-button>
      <t-button theme="default" variant="outline" @click="LabelerResize"> 重置图片 </t-button>
    </div> -->

    <!-- <t-divider /> -->

    <div id="label-img" ref="img" class="disease_pic"></div>

    <t-tabs v-model="value" v-if="OpeningImg">
      <t-tab-panel :value="1">
        <template #label>
          <t-icon name="scan" class="tabs-icon-margin" />病变特征检测
        </template>
        <diseaseVue :models="DiseaseModels" />
      </t-tab-panel>
      <t-tab-panel :value="2">
        <template #label>
          <t-icon name="chart-bubble" class="tabs-icon-margin" />疾病风险评估
        </template>
        <!-- <diseaseVue /> -->
      </t-tab-panel>
    </t-tabs>
  </div>
</template>

<script setup lang="ts">
import { inject, onMounted, provide, ref, watch, watchEffect } from 'vue';
import LabelImg, { Shape } from 'label-img';
import riskVue from './risk.vue';
import diseaseVue from './disease.vue';
import { SingleEyeImg, Predict, Model, ListData } from '../types';
import { ResDataType } from '@/interface';
import request from '@/utils/request';

// const { Shape } = LabelImg;
//  加载模型信息

const props = defineProps<{ update: Function }>()


const DiseaseModels = ref<Model[]>([])
const RiskModels = ref<Model[]>([])

onMounted(() => fetchModelInfo())

const model_info = ref<{ String: Model[] }>(null)
const fetchModelInfo = async () => {
  try {
    const res: ResDataType = await request.get('/api/models/list');
    if (res.code === 0) {
      model_info.value = res.data
      console.log("模型信息:", model_info.value);

      // 对模型进行归类
      DiseaseModels.value = []
      RiskModels.value = []
      for (var model in model_info.value) {
        console.log(model);
        if (model_info.value[model].category == "disease") {
          DiseaseModels.value.push(model_info.value[model])
        } else if (model_info.value[model].category == "risk") {
          RiskModels.value.push(model_info.value[model])
        }
      }
      console.log("模型归类完成:");
      console.log("disease: ", DiseaseModels.value);
      console.log("risk: ", RiskModels.value);
    }
  } catch (e) {
    console.log(e);
  }
};

// 挂载
let labeler: LabelImg
const img = ref<HTMLDivElement>(null);

// TODO: 解决ref响应式ReplImp的类型问题 ref<SingleEyeImg> 会报 “ref”表示值，但在此处用作类型。是否指“类型 ref”?
const OpeningImg: { value: SingleEyeImg } = inject('OpeningImg');
onMounted(() => {
  // https://github.com/hold-baby/label-img
  labeler = new LabelImg(<HTMLDivElement>img.value, {
    //@ts-ignore
    width: 1400,
    height: 600,
    bgColor: `#000`, // 背景色
    //@ts-ignore
    imagePlacement: 'default', // default | center
  });

  // 加载图片
  watch(OpeningImg, () => {
    console.log(OpeningImg.value);

    const url = `http://localhost:21335/api/picture/${OpeningImg.value.value}`
    console.log("<Tabs> Load url:", url);
    labeler.load(url);
  })
})

function LabelerResize() {
  labeler.resize()
}


function focus(row: ListData) {
  console.log('Focus', row);
  row.results!.forEach((label) => {
    console.log(label);
    let shapeOptions = {
      type: label.shape, // 图形类型 必填 Polygon | Ract
      positions: label.positions, // 坐标集合 ex: [[0, 0], [100, 100]]
      tag: `${label.label}:${label.confidence}`, // 展示在图形上的说明标签
      showTag: true, // 是否展示标签
      closed: true, // 是否闭合
      // visible, // 是否可见
      active: false, // 是否被选中
      disabled: true, // 是否禁用
      /**
       * { normal, active, disabled }
       * {
       *  normal: {
       *    dotColor: "red", // 坐标点颜色
       *    dotRadius: 3, // 坐标点大小
       *    lineColor: "#c30", // 连线颜色
       *    lineWidth: 2, // 连线宽度
       *    fillColor: "pink", // 填充色
       *  }
       * }
       */
      // style, // 图形样式
    }
    // @ts-ignore
    const shape = new Shape(shapeOptions)

    // 添加到画布中
    labeler.addShape(shape)
  })
}

provide('focus', focus);


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
  /* left: 25%; */
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

.controls {
  left: 25%;
  margin: auto;
  margin-top: 20px;
}
</style>
