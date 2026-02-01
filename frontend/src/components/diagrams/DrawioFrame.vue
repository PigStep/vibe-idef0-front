<template>
  <iframe
    ref="iframeRef"
    :src="embedUrl"
    allowFullScreen
    frameborder="0"
    class="drawio-frame"
  ></iframe>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { config } from '@config'

const props = defineProps({
  drawioService: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['ready'])

const iframeRef = ref(null)
const embedUrl = config.drawio.embedUrl

onMounted(async () => {
  if (iframeRef.value) {
    await props.drawioService.init(iframeRef.value)
    emit('ready')
  }
})

onUnmounted(() => {
  props.drawioService.destroy()
})
</script>

<style scoped>
.drawio-frame {
  flex: 1;
  width: 100%;
  border: none;
  display: block;
}
</style>
