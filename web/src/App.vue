<template>
  <div id="app">
    <Tabs @clicked="handleSwitch" />
    <span class="divider" />
    <Workers v-if="scene === 0" />
    <Tracks v-if="scene === 1" />
    <Train v-if="scene === 3" />
  </div>
</template>

<script>
import Tabs from './components/Tabs.vue';
import Workers from './components/Worker/Workers.vue';
import Tracks from './components/Tracks/Tracks.vue';
import Train from './components/Train/Train.vue';

export default {
  name: 'App',
  components: {
    Tabs,
    Workers,
    Tracks,
    Train,
  },
  data() {
    return {
      scene: 0,
    }
  },
  methods: {
    handleSwitch(k){
      this.scene = k
    },
  },
};
</script>

<style lang="scss">
:root{
  --trainBlue: #828EFF;
  --trainAccentBlue: #4472CA;
}

body{
  margin: 0;
  padding: 0;
}

h1, h2, h3, h4 {
    font-family: 'Raleway', sans-serif;
    font-weight: bold !important;
    margin: 0 !important;
}

#app {
  font-family: 'Roboto', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100vh;
  width: 100vw;
  display: flex;
  overflow: hidden;
}

.divider{
  width: 7px;
  height: 100vh;
  background-color: var(--trainBlue);
}
</style>
