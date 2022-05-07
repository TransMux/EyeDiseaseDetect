<template>
  <div :class="prefix + '-footer'">Mux - All Rights Reserved @ Eye disease detection</div>
</template>

<script setup lang="ts">
import { prefix } from '@/config/global';
</script>

<style lang="less" scoped>
@import '@/style/variables';

.@{prefix}-footer {
  color: @text-color-placeholder;
  line-height: 20px;
  text-align: center;
}
</style>
