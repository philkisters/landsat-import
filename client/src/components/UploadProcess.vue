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

      Get official tools and libraries for your project:
      <a href="https://pinia.vuejs.org/" target="_blank" rel="noopener">Pinia</a>,
      <a href="https://router.vuejs.org/" target="_blank" rel="noopener">Vue Router</a>,
      <a href="https://test-utils.vuejs.org/" target="_blank" rel="noopener">Vue Test Utils</a>, and
      <a href="https://github.com/vuejs/devtools" target="_blank" rel="noopener">Vue Dev Tools</a>. If
      you need more resources, we suggest paying
      <a href="https://github.com/vuejs/awesome-vue" target="_blank" rel="noopener">Awesome Vue</a>
      a visit.
    </ProcessItem>

    <ProcessItem v-if="step >= 3">
      <template #icon>
        <IconCheck />
      </template>
      <template #heading>Done</template>

      Got stuck? Ask your question on
      <a href="https://chat.vuejs.org" target="_blank" rel="noopener">Vue Land</a>
      (our official Discord server), or
      <a href="https://stackoverflow.com/questions/tagged/vue.js" target="_blank" rel="noopener">StackOverflow</a>. You
      should also follow the official
      <a href="https://bsky.app/profile/vuejs.org" target="_blank" rel="noopener">@vuejs.org</a>
      Bluesky account or the
      <a href="https://x.com/vuejs" target="_blank" rel="noopener">@vuejs</a>
      X account for latest news in the Vue world.
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
import { ref } from 'vue'

const step = ref(0);
const filename = ref('')

const uploadedFile = (file) => {
  filename.value = file;
  step.value += 1;
  console.log(`Uploaded ${file}`)
} 
</script>