<script setup>
import { ref } from 'vue';

const images = ref([
  { src: 'https://cdn.vuetifyjs.com/images/cards/sunshine.jpg', alt: 'Image 1 Description' },
  { src: 'https://cdn.vuetifyjs.com/images/cards/docks.jpg', alt: 'Image 2 Description' },
  { src: 'https://cdn.vuetifyjs.com/images/cards/mountain.jpg', alt: 'Image 3 Description' },
]);
</script>

<template>
  <div class="carousel">
    <div class="carousel-inner">
      <div v-for="(image, index) in images" :key="index" class="carousel-item">
        <img :src="image.src" :alt="image.alt" class="d-block w-100" />
      </div>
    </div>
  </div>
</template>
<style scoped>
.carousel {
  width: 100%;
  height: 400px;
  overflow: hidden;
}

.carousel-inner {
  width: 100%;
  height: 100%;
  position: relative;
}

.carousel-item {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  opacity: 0;
  transition: opacity 0.5s ease-in-out;
}

.carousel-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.carousel-item.active {
  opacity: 1;
}
</style>
