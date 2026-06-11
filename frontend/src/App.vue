<script setup lang="ts">
import Navbar from './components/common/Navbar.vue'
import Footer from './components/common/Footer.vue'
</script>

<template>
  <div class="flex min-h-screen flex-col bg-gray-50 dark:bg-gray-950">
    <Navbar />
    <main class="flex-1">
      <router-view />
    </main>
    <Footer />
  </div>
</template>
