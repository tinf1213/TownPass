<template>
  <div class="container">
    <header>
      <button class="menu-button">☰</button>
      <h1 class="title">
        文化時空
        <span class="sparkle">✨</span>
      </h1>
    </header>

    <main>
      <div v-if="locationRequested">
        <p v-if="latitude">Latitude: {{ latitude }}</p>
        <p v-if="longitude">Longitude: {{ longitude }}</p>
        <p v-if="error">{{ error }}</p>
      </div>

      <div class="message-container">
        <div v-for="(message, index) in messageLists" :key="index"
          :class="['message', message.type === 'user' ? 'user-message' : 'ai-message']">
          {{ message.text }}
        </div>
        <div v-if="isLoading" class="message ai-message">
          Thinking...
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios' // Ensure axios is imported

const latitude = ref(null)
const longitude = ref(null)
const error = ref(null)
const places = ref([])
const locationRequested = ref(true)
const messageLists = ref([])
const isLoading = ref(false)

onMounted(async () => {
  // requestLocation()
  await get_current_location()
  await getNearbyPlaces()
})

const requestLocation = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        latitude.value = position.coords.latitude
        longitude.value = position.coords.longitude
        error.value = null
        getNearbyPlaces()
      },
      (err) => {
        switch (err.code) {
          case 1: // PERMISSION_DENIED
            error.value = "User denied the request for Geolocation. Please enable location permissions in your browser settings."
            break
          case 2: // POSITION_UNAVAILABLE
            error.value = "Location information is unavailable. Please check your network connection."
            break
          case 3: // TIMEOUT
            error.value = "The request to get user location timed out. Please try again."
            break
          default:
            error.value = "An unknown error occurred."
        }
      }
    )
  } else {
    error.value = "Geolocation is not supported by this browser."
  }
}

const getNearbyPlaces = async () => {
  isLoading.value = true;
  try {
    // Create FormData object
    const formData = new FormData();
    formData.append('lat', latitude.value);
    formData.append('lon', longitude.value);
    formData.append('radius', 1500);
    formData.append('place_type', 'tourist_attraction');

    const response = await axios.post('https://adaf-211-75-133-2.ngrok-free.app/api/data', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    // Assuming response.data contains an array of places
    places.value = response.data.places || [];
    messageLists.value.push({ text: 'Places fetched successfully!', type: 'ai' });
    // console.log("testing");
    console.log("getNearbyPlaces2");
     console.log(places.value);

  } catch (error) {
    console.error('Error fetching data:', error);
    messageLists.value.push({ text: 'Failed to fetch places', type: 'ai' });
  } finally {
    isLoading.value = false;
  }
}

const get_current_location = async () => {
  console.log("getNearbyPlaces2");
  isLoading.value = true;
  try {
    const formData = new FormData();
    formData.append('location_name', '台北101');

    const response = await axios.post('https://adaf-211-75-133-2.ngrok-free.app/api/getLL', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    // Assuming response.data contains an array of places
    places.value = response.data.places || [];
    messageLists.value.push({ text: 'Places fetched successfully!', type: 'ai' });
    console.log("testing");
    console.log(places.value);
    latitude.value = places.value.latitude;
    longitude.value = places.value.longitude;

  } catch (error) {
    console.error('Error fetching data:', error);
    messageLists.value.push({ text: 'Failed to fetch places', type: 'ai' });
  } finally {
    isLoading.value = false;
  }
}
</script>
