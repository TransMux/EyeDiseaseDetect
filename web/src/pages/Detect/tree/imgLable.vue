<script lang="ts" setup>
import { Shape } from "@/components/Labelmg/Shape";
import { SingleEyeImg } from "@/pages/Detect/types";
import { AddNodes, AddEdges, Handle, Position } from '@braks/vue-flow'
import LabelImg from "@/components/Labelmg/main";
import { computed, inject, markRaw, onMounted, provide, ref, watch, watchEffect } from "vue";
import StaticImg from "./StaticImg.vue"
// injections
const addNodes: AddNodes = inject("addNodes")
const addEdges: AddEdges = inject("addEdges")
const getNodes = inject("getNodes")
const getEdges = inject("getEdges")
const onLayout = inject("onLayout")


const targetDiv = ref()
let labeler: LabelImg;
onMounted(() => {
  labeler = new LabelImg(targetDiv.value, {
    width: 400,
    height: 400,
    bgColor: `#000`, // 背景色
  });
  labeler.register("rect", {
    type: "Rect",
    tag: "血管瘤",
    style: {
      normal: {
        fillColor: "white",
        opacity: 0.2
      },
      disabled: {
        opacity: 0.2
      }
    }
  });
  // 加载图片
  watch(OpeningImg, () => {
    console.log(OpeningImg.value);

    const url = `http://localhost:21335/api/picture/${OpeningImg.value.value}`
    console.log("<Tabs> Load url:", url);
    labeler.load(url);
    labelStatus.value = false
    labeler.labelOff()
    labelButton.value = "Label"
  })
  // 添加辅助线
  labeler?.setGuideLine()
  // 创建标注框时
  labeler.emitter.on("create", () => {
    const shapeList = labeler.getShapeList()
    const count = shapeList.length
    const shape: Shape = shapeList[count - 1]
    console.log("Create", shape)
    console.log(shape.getPositions())
    shape.disabled()
    const newTag = `${shape.tagContent} ${count}`
    shape.setTag(newTag)

    // 添加节点和边
    // addNodes([
    //     {
    //       id: newTag,
    //       position: {x: 150, y: 50},
    //       label: 'Node 2',
    //       template: markRaw(StaticImg),
    //     }
    //   ]
    // )
    // addEdges([
    //   {
    //     id: 'e' + newTag,
    //     animated: true,
    //     source: 'root',
    //     target: newTag,
    //   }
    // ])
    // onLayout("LR")
  })
})
const OpeningImg: { value: SingleEyeImg } = inject('OpeningImg');

const labelStatus = ref(false)
const labelButton = ref("Label")

function ChooseLabel() {
  if (labelStatus.value) {
    labeler.labelOff()
    labelButton.value = "Label"
    labelStatus.value = false
  } else {
    labeler.label("rect");
    labelButton.value = "LabelOff"
    labelStatus.value = true
  }
}
</script>

<template>
  <div>
    <button @click="ChooseLabel" class="label_button">{{ labelButton }}</button>
    <div ref="targetDiv"/>
  </div>
</template>

<style>
.label_button {
  margin: auto;
}

</style>
