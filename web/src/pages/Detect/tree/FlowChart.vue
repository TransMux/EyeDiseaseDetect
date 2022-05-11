<script lang="ts" setup>
import dagre from 'dagre'
import { VueFlow, MiniMap, Controls, useVueFlow, isNode, Elements } from '@braks/vue-flow'
import { useElementHover } from "@vueuse/core";
import { provide, ref, watch } from "vue";
import ImageLabelNode from "./imgLable.vue"
import { Handle, Position } from '@braks/vue-flow'

// dagre
const dagreGraph = new dagre.graphlib.Graph()
dagreGraph.setDefaultEdgeLabel(() => ({}))

// elements
const elements = ref<Elements>([
  {
    id: 'root',
    type: 'root',
    label: 'Node 1',
    style: {border: '1px solid #0163f7', padding: '5px', borderRadius: "5px"},
    position: {x: 250, y: 5}
  },
  {id: '2', label: 'Node 2', position: {x: 100, y: 100}},
  {id: '3', label: 'Node 3', position: {x: 400, y: 100}},
  {id: 'e1-2', source: 'root', target: '2', animated: true},
  {id: 'e1-3', source: 'root', target: '3'},
])


// init Vue flow
const {
  nodesDraggable,
  zoomOnScroll,
  instance,
  addNodes,
  addEdges,
  getNodes,
  getEdges
} = useVueFlow({
  modelValue: elements,
})

provide("addNodes", addNodes)
provide("addEdges", addEdges)
provide("getNodes", getNodes)
provide("getEdges", getEdges)

// utils
const onLayout = (direction: string) => {
  const isHorizontal = direction === 'LR'
  dagreGraph.setGraph({rankdir: direction})

  elements.value.forEach((el) => {
    console.log(el)
    if (isNode(el)) {
      dagreGraph.setNode(el.id, {width: 150, height: 50})
    } else {
      dagreGraph.setEdge(el.source, el.target)
    }
  })

  dagre.layout(dagreGraph)

  elements.value.forEach((el) => {
    if (isNode(el)) {
      const nodeWithPosition = dagreGraph.node(el.id)
      if (el.type === "root") {
        nodeWithPosition.x -= 250
        nodeWithPosition.y -= 180
      }
      el.targetPosition = isHorizontal ? Position.Left : Position.Top
      el.sourcePosition = isHorizontal ? Position.Right : Position.Bottom
      el.position = {x: nodeWithPosition.x, y: nodeWithPosition.y}
    }
  })
  // 居中
  instance.value?.fitView()
  // setTimeout(() => instance.value?.fitView(), 1)
}

// Disable drag and zoom on hovering root node
const RootNode = ref()
const rootIsHovering = useElementHover(RootNode);
watch(rootIsHovering, () => {
  nodesDraggable.value = !rootIsHovering.value
  zoomOnScroll.value = !rootIsHovering.value
})

provide("onLayout", onLayout)

</script>


<template>
  <VueFlow fit-view-on-init>
    <MiniMap/>
    <Controls/>
    <template #node-root>
      <Handle id="a" type="source" :position="Position.Right"/>
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
      <div>
        <button @click="onLayout('LR')">LayoutLR</button>
      </div>
    </div>
  </VueFlow>
</template>


<style>
.vue-flow {
  height: 80vh;
}
</style>
