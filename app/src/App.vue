<template>
  <div id="app">
    <main v-masonry item-selector=".comic"
      transition-duration="0.3s">
      <Comic
        v-for="comic in comics"
        v-bind:key="comic.xkcd" :ref="comic.xkcd"
        v-bind:xkcd="comic"
        v-on:click.native="openModal(comic)"
        v-masonry-tile class="comic"
      ></Comic>
    </main>

    <Modal
      v-if="modalComic"
      v-bind:xkcd="modalComic"
      @prev="shiftModal(1)"
      @next="shiftModal(-1)"
      @close="closeModal"
    ></Modal>

    <sub v-if="moreToLoad">Loading…</sub>
    <sub v-else>You have finished xkcd.</sub>
  </div>
</template>

<script>
import {VueMasonryPlugin} from 'vue-masonry'
import axios from 'axios'
import Vue from 'vue'
import Comic from './components/Comic'
import Modal from './components/Modal'

Vue.use(VueMasonryPlugin)

export default {
  name: 'App',
  components: { Comic, Modal },
  data () {
    return {
      comics: [],
      page: 0,
      moreToLoad: true,
      modalComic: null
    }
  },
  methods: {
    initScrollListener () {
      const _this = this

      window.onscroll = () => {
        const d = document.documentElement
        if (d.scrollHeight - d.scrollTop === d.clientHeight) {
          _this.fetchComics()
        }
      }
    },
    fetchComics () {
      const _this = this

      axios.get(`http://127.0.0.1:8000/xkcds/?page=${++_this.page}`)
      // axios.get(`http://api.emilykarp.com/xkcds?page=${++_this.page}`)
        .then(response => {
          if (response.data.comics) {
            _this.comics = _this.comics.concat(response.data.comics)
            _this.page = response.data.page
          } else {
            _this.moreToLoad = false
          }
        })
    },
    openModal (comic) {
      this.modalComic = comic
    },
    shiftModal (shift) {
      const currIndex = this.comics.indexOf(this.modalComic)
      this.modalComic = this.comics[currIndex + shift]

      const comicElem = this.$refs[this.modalComic.xkcd][0].$el
      comicElem.scrollIntoView()
    },
    closeModal () {
      this.modalComic = null
    }
  },
  mounted () {
    const _this = this
    _this.fetchComics()
    _this.initScrollListener()

    window.addEventListener('keyup', function (e) {
      if (_this.modalComic) {
        switch (e.keyCode) {
          case 37: _this.shiftModal(-1)
            break
          case 39: _this.shiftModal(1)
        }
      }
    })
  }
}
</script>

<style>
body {
  background-color: cornflowerblue;
  height: calc(100vh + 5px);
  margin-bottom: 5px;
}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  margin-top: 60px;
}
.comic {
  max-width: 22%;
  margin: 10px;
}
img {
  max-width: 100%;
}
sub {
  display: flex;
  justify-content: space-between;
  font-size: .6em;
}
figcaption {
  text-align: center;
}
</style>
