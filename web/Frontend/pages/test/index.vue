<template>
  <div>
    <p v-if="latitude && longitude">Latitude: {{ latitude }}</p>
    <p v-if="latitude && longitude">Longitude: {{ longitude }}</p>
    <p v-else>{{ error }}</p>
    <button @click="getLocation">取得經緯度</button>
  </div>
  <div style="border:1px solid #ccc; padding:10px; width:300px;">
    <h2>Taipei 101</h2>
    <p>No. 7, Section 5, Xinyi Rd, Xinyi District, Taipei City, 110</p>
    <a href="https://www.google.com/maps/dir/?api=1&destination=Taipei+101" target="_blank"
      style="color:blue; text-decoration:none;">
      Directions
    </a>
    <br />
    <a href="https://www.google.com/maps/place/Taipei+101" target="_blank" style="color:blue; text-decoration:none;">
      View larger map
    </a>
  </div>
  <iframe
    src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3621.3873249830766!2d121.56367911513436!3d25.033969983970364!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3442abb43b8e470b%3A0x9296a1be9eaa7ff!2sTaipei%20101!5e0!3m2!1sen!2stw!4v1694164650354!5m2!1sen!2stw"
    width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy"
    referrerpolicy="no-referrer-when-downgrade">
  </iframe>


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
