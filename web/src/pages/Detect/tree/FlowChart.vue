<script lang="ts" setup>
import { VueFlow, MiniMap, Controls, useVueFlow } from '@braks/vue-flow'
import { useElementHover } from "@vueuse/core";
import { ref, watch } from "vue";
import ImageLabelNode from "./imgLable.vue"

// init Vue flow
const {
  nodesDraggable,
  zoomOnScroll,
} = useVueFlow({
  modelValue: [
    {id: '1', type: 'root', label: 'Node 1', position: {x: 250, y: 5}},
    {id: '2', label: 'Node 2', position: {x: 100, y: 100}},
    {id: '3', label: 'Node 3', position: {x: 400, y: 100}},
    {id: '4', label: 'Node 4', position: {x: 400, y: 200}},
    {id: 'e1-2', source: '1', target: '2', animated: true},
    {id: 'e1-3', source: '1', target: '3'},
  ],
})


// Disable drag and zoom on hovering root node
const RootNode = ref()
const rootIsHovering = useElementHover(RootNode);
watch(rootIsHovering, () => {
  nodesDraggable.value = !rootIsHovering.value
  zoomOnScroll.value = !rootIsHovering.value
})

</script>


<template>
  <VueFlow>
    <MiniMap/>
    <Controls/>
    <template #node-root>
      <ImageLabelNode ref="RootNode"/>
    </template>
    <div :style="{ position: 'absolute', left: 10, top: 10, zIndex: 4 }">
      <div>
        <label for="draggable">
          nodesDraggable
          <input id="draggable" v-model="nodesDraggable" type="checkbox"/>
        </label>
      </div>
      <div>
        <label for="zoomonscroll">
          zoomOnScroll
          <input id="zoomonscroll" v-model="zoomOnScroll" type="checkbox"/>
        </label>
      </div>
    </div>
  </VueFlow>
</template>


<style>
.vue-flow {
  height: 100vh;
}
</style>
