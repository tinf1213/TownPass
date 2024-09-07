export const getLocation = () => {
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

