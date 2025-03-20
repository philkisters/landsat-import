<template>
  <diV class="upload-container">
    <div v-if="selectedFile == null">
      <input v-on:change="selectedFileChanged" type="file">
    </div>
    <div v-else class="upload-container">
      <span>
        {{ selectedFile.name }} selected.
      </span>
      <div class="button-row">
        <Button @click="ResetFile">Remove File</Button>
        <Button @click="UploadFile">Upload File</Button>
      </div>
    </div>
  </diV>
</template>
<script setup lang="ts">
import Button from './ui/ButtonComponent.vue'
import { ref } from 'vue'

const selectedFile = ref(null)

const selectedFileChanged = (event) => {
  const files = event.target.files;
  if (files.length > 0) {
    selectedFile.value = files[0];
  } else {
    selectedFile.value = null;
  }
}

const ResetFile = () => {
  selectedFile.value = null;
}

const UploadFile = () => {
  if (selectedFile.value === null) {
    return;
  }

  const formData = new FormData();
  formData.append('file', selectedFile.value);

  fetch('http://127.0.0.1:5000/upload', {
    method: 'POST',
    body: formData
  })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

</script>
<style lang="css" scoped>
.upload-container {
  display: flex;
  flex-direction: column;
}

.button-row {
  display: flex;
  flex-direction: row;
}
</style>