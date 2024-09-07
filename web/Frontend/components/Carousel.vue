<script setup>
import { ref } from 'vue';

const images = ref([
  { link: 'image/Taipei_101_Tower_E_0.png', alt: 'Taipei 101 Tower', text: "台北101" ,description:"台北101是台北市的著名地標，位於信義區，是台灣最高的建築物之一。它以其獨特的設計和壯觀的景觀而聞名，是台北市的象徵之一。"},
  { link: 'image/National_Palace.png', alt: 'Taipei 101 Tower', text: "故宮博物院" ,description:"故宮博物院是台北市的一個著名博物館，收藏了大量的中國古代文物和藝術品。它以其豐富的歷史和文化價值而聞名，是台灣最重要的博物館之一。"},
  { link: 'image/Memorial_Hall.png', alt: 'Taipei 101 Tower', text: "中正紀念堂", description:"中正紀念堂是台北市的一個著名紀念堂，位於中正區，以紀念中華民國國父孫中山先生而聞名。它以其宏偉的建築和歷史意義而聞名，是台北市的象徵之一。"},
  { link: 'image/Taipei_101_Tower_E_0.png', alt: 'Taipei 101 Tower', text: "台北車站" ,description:"台北車站是台北市的一個著名車站，位於中正區，是台灣最重要的交通樞紐之一。它以其繁忙的交通和歷史意義而聞名，是台北市的象徵之一。"},
  { link: 'image/Taipei_101_Tower_E_0.png', alt: 'Taipei 101 Tower', text: "西門町" ,description:"西門町是台北市的一個著名商圈，位於中正區，以其繁華的商業和娛樂活動而聞名。它以其獨特的設計和多元化的商業活動而聞名，是台北市的象徵之一。"},
]);
</script>

<template>
  <div class="carousel">
    <div class="carousel-inner">
      <div v-for="(image, index) in images" :key="index" class="carousel-item">
      <NuxtLink :to="`/chat?location=${image.text}`">
        <img :src="image.link" :alt="image.alt" />
        <div class="text-list">
          {{ image.text }}
        </div>
        <div class="description-list">
          {{ image.description }}
        </div>
      </NuxtLink>
      </div>
    </div>
  </div>
</template>

<style scoped>
.carousel {
  width: 100%;
  height: 480px;
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
  background-color: #f0f0f0;
  border-radius: 3%;
}

.carousel-item img {
  border-radius: 3%;
  width: 100%;
  height: 70%;
  object-fit: cover;
}

.text-list {
  padding: 10px;
  font-size:24px;
  font-weight: bold;
}

.description-list {
  padding: 10px;
  font-size: 16px;
}
</style>
