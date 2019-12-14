<template>
  <figure>

    <figcaption>{{this.xkcd.name}}</figcaption>
    <img :src="permalink" :alt="this.xkcd.name">

    <sub>
      {{this.xkcd.xkcd}}
      <time :datetime="this.xkcd.date">{{this.xkcd.date}}</time>
    </sub>

  </figure>
</template>

<script>
export default {
  name: 'Comic',
  props: ['xkcd'],
  computed: {
    permalink: function () {
      return `${window.imagePath}${this.xkcd.file}`
    }
  }
}
</script>
