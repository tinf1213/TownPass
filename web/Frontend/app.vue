
<!-- 全域樣式 -->
<style>
/* 頁面過渡動畫 */
/* Reset default body styles */
body {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: Arial, sans-serif;
  line-height: 1.6;
  background-color: #FDF8ED;
  color: #333;
}

/* Ensure all elements use border-box */
*, *::before, *::after {
  box-sizing: inherit;
}

.page-enter-active,
.page-leave-active {
  transition: all 0.1s;
}
</style>
<template>
  <div>
    <NuxtPage/>
  </div>
</template>
