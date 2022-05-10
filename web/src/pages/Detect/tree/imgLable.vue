<script lang="ts" setup>
import { SingleEyeImg } from "@/pages/Detect/types";
import { Handle, Position } from '@braks/vue-flow'
// import LabelImg from "label-img";
import LabelImg from "@/components/Labelmg/main";
import { computed, inject, onMounted, ref, watch, watchEffect } from "vue";

const targetDiv = ref()
var labeler

onMounted(() => {
  labeler = new LabelImg(targetDiv.value, {
    width: 400,
    height: 400,
    bgColor: `#000`, // 背景色
  });
  labeler.register("rect", {
    type: "Rect",
    tag: "血管瘤",
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
