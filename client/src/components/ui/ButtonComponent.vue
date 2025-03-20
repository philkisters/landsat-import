<template>
  <button class="button">
    <slot>
    </slot>
  </button>
</template>
<script setup lang="ts">
</script>
<style>
.button {
  color: var(--li-c-white-mute);
  background: var(--li-c-white-soft);
  margin: 10px;
  padding: 12px 15px;
  border: 2px solid var(--li-c-white-mute);
  text-align: center;
  text-transform: uppercase;
  position: relative;
  overflow: hidden;
  transition: .3s;
  z-index: 1;
}

.button::before {
  position: absolute;
  transition: .3s;
  content: '';
  width: 0;
  bottom: 0;
  background: var(--li-c-white-mute);
  height: 120%;
  left: -10%;
  transform: skewX(20deg);
  z-index: -1;
}

.button:hover::before {
  width: 120%;
}

.button:hover {
  cursor: pointer;
  color: var(--li-c-white-soft);
}
</style>