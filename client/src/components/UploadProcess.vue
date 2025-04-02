<template>
  <div class="process-container">
    <ProcessItem :class="step === 0 ? 'active' : ''">
      <template #icon>
        <IconUpload />
      </template>
      <template #heading>
        <span v-if="step === 0">
          Upload a BT10 Tiff Image
        </span>
        <span v-else>
          File uploaded.
        </span>
      </template>
      <UploadItem v-if="step === 0" @success="uploadedFile" />
    </ProcessItem>

    <ProcessItem v-if="step >= 1" :class="step === 1 ? 'active' : ''">
      <template #icon>
        <IconAnalyze />
      </template>
      <template #heading>
        <span v-if="step === 1">
          Analyzing
        </span>
        <span v-else>
          File analyzed.
        </span>
      </template>

      <AnalyzingItem v-if="step === 1" :filename="filename" @success="step += 1" />
    </ProcessItem>

    <ProcessItem v-if="step >= 2" :class="step === 2 ? 'active' : ''">
      <template #icon>
        <IconDatabase />
      </template>
      <template #heading>Storing</template>

      <StoreItem v-if="step === 2" :filename="filename" @success="step += 1" />
    </ProcessItem>

    <ProcessItem v-if="step >= 3">
      <template #icon>
        <IconCheck />
      </template>
      <template #heading>
        <p>Done</p>
        <Button @click="reset">Add another Dataset</Button>
      </template>

      {{ filename }} successfully analyzed and stored.
    </ProcessItem>
  </div>
</template>
<script setup lang="ts">
import ProcessItem from './ProcessItem.vue'
import IconUpload from './icons/IconUpload.vue'
import IconAnalyze from './icons/IconAnalyze.vue'
import IconDatabase from './icons/IconDatabase.vue'
import IconCheck from './icons/IconCheck.vue'
import UploadItem from './UploadItem.vue'
import AnalyzingItem from './AnalyzingItem.vue'
import StoreItem from './StoreItem.vue'
import Button from './ui/ButtonComponent.vue'
import { ref } from 'vue'

const step = ref(0);
const filename = ref('')

const reset = () => {
  step.value = 0;
  filename.value = ''
}

const uploadedFile = (file) => {
  filename.value = file;
  step.value += 1;
} 
</script>