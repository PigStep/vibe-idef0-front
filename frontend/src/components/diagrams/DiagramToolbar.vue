<template>
  <div class="toolbar">
    <button
      @click="$emit('create-child')"
      :disabled="!isReady"
      class="toolbar-button"
    >
      Create Child Diagram
    </button>
    <button
      @click="$emit('load-diagram')"
      :disabled="!isReady"
      class="toolbar-button"
    >
      Загрузить тест
    </button>
  </div>
</template>

<script setup>
defineProps({
  isReady: {
    type: Boolean,
    required: true,
  },
})

defineEmits(['create-child', 'load-diagram'])
</script>

<style scoped>
.toolbar {
  display: flex;
  gap: 8px;
  padding: 8px;
  background-color: #f5f5f5;
  border-bottom: 1px solid #ddd;
}

.toolbar-button {
  padding: 6px 12px;
  background-color: #0066cc;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.toolbar-button:hover:not(:disabled) {
  background-color: #0052a3;
}

.toolbar-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>
