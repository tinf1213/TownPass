
<script setup>
import TextList from '@/components/TextList.vue';

const texts = ['Hello', 'World', 'This', 'Is', 'Vue'];
</script>

<template>
  <div>
    <TextList :texts="texts" />
  </div>
</template>
