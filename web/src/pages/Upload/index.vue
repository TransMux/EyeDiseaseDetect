<template>
  <div class="t-upload__file-flow-demo">
    <t-upload v-model="files" action="http://127.0.0.1:21335/api/upload" placeholder="只能上传图片文件，支持批量上传文件，支持拖拽上传"
      theme="file-flow" multiple :use-mock-progress="false" :auto-upload="false" draggable :fail="onUploadFail"
      :max="100">
    </t-upload>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const files = ref([]);

function onUploadFail({ e }) {
  console.log(e);
}
</script>

<style>
.t-upload__file-flow-demo {
  background-color: white;
  padding-top: 30px;
  padding-bottom: 30px;
}

.t-upload__flow {
  margin: auto;
}
</style>
