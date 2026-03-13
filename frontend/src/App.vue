<template>
  <RouterView />
</template>

<script setup>
import { RouterView } from 'vue-router'
</script>

<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { background: #0f1624; color: #e2e8f0; font-family: 'Inter', system-ui, sans-serif; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #1e2533; }
::-webkit-scrollbar-thumb { background: #374151; border-radius: 3px; }
</style>
