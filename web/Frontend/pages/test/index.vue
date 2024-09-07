<template>
  <div>
    <p v-if="latitude && longitude">Latitude: {{ latitude }}</p>
    <p v-if="latitude && longitude">Longitude: {{ longitude }}</p>
    <p v-else>{{ error }}</p>
    <button @click="getLocation">取得經緯度</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// 定義 reactive 的 latitude, longitude 和 error
const latitude = ref(null)
const longitude = ref(null)
const error = ref(null)

// 定義取得地理位置的函數
const getLocation = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        latitude.value = position.coords.latitude
        longitude.value = position.coords.longitude
      },
      (err) => {
        error.value = `無法取得位置: ${err.message}`
      }
    )
  } else {
    error.value = "瀏覽器不支援 Geolocation"
  }
}
</script>
