<script setup>
import { ref } from 'vue';

const images = ref([
  { link: 'image/Taipei_101_Tower_E_0.jpg', alt: 'Taipei 101 Tower' },
  { link: 'image/Taipei_101_Tower_E_0.jpg', alt: 'Taipei 101 Tower' },
  { link: 'image/Taipei_101_Tower_E_0.jpg', alt: 'Taipei 101 Tower' },
]);
</script>

<template>
  <div class="carousel">
    <div class="carousel-inner">
      <div v-for="(image, index) in images" :key="index" class="carousel-item">
        <img :src="image.link" :alt="image.alt" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.carousel {
  width: 100%;
  height: 400px;
  overflow-x: auto;
  overflow-y: hidden;
}

.carousel-inner {
  display: flex;
  height: 100%;
}

.carousel-item {
  flex: 0 0 auto;
  width: 100%;
  height: 100%;
  margin-right: 20px;
}

.carousel-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>
