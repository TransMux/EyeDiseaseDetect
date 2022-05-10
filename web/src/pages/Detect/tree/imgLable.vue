<script lang="ts" setup>
import { SingleEyeImg } from "@/pages/Detect/types";
import LabelImg from "label-img";
import { inject, onMounted, ref, watch, watchEffect } from "vue";

const targetDiv = ref()

onMounted(() => {
  // @ts-ignore
  // labelImgDiv = document.getElementById("target")
  const labeler = new LabelImg(targetDiv.value, {
    width: 600,
    height: 600,
    bgColor: `#000`, // 背景色
  });
// 加载图片
  watch(OpeningImg, () => {
    console.log(OpeningImg.value);

    const url = `http://localhost:21335/api/picture/${OpeningImg.value.value}`
    console.log("<Tabs> Load url:", url);
    labeler.load(url);
  })
})
const OpeningImg: { value: SingleEyeImg } = inject('OpeningImg');


</script>

<template>
  <div ref="targetDiv"/>
</template>
