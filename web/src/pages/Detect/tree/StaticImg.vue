<template>
  <Handle id="a" type="target" :position="Position.Left"/>
  <div>
    Hello
  </div>
  <Handle id="a" type="source" :position="Position.Right"/>
</template>

<script setup lang="ts">
import { Handle, Position } from '@braks/vue-flow'


</script>
