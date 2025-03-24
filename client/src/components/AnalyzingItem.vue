<template>
  <div>
    Analyzing {{ filename }}...
  </div>
</template>
<script setup lang="ts">
import { onMounted } from 'vue';

const props = defineProps({
  filename: {
    type: String,
    required: true
  }
});
const emit = defineEmits(['success']);

onMounted(() => {
  fetch('http://127.0.0.1:5000/analyze', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      filename: props.filename,
    })
  })
    .then(response => response.json())
    .then(data => {
      if (!data.error) {
        emit('success')
        return;
      }
      console.log('Error:', data);
    })
    .catch(error => {
      console.error('Error:', error);
    });
});

</script>