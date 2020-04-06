<template>
  <div id="app">
    <Tabs @clicked="handleSwitch" />
    <span class="divider" />
    <welcome v-if="scene === 0" />
    <Workers v-if="scene === 1" />
    <Tracks v-if="scene === 2" />
    <Train v-if="scene === 3" />
  </div>
</template>

<script>
import Tabs from './components/Tabs.vue';
import Workers from './components/Worker/Workers.vue';
import Tracks from './components/Tracks/Tracks.vue';
import Train from './components/Train/Train.vue';
import Welcome from './components/Welcome.vue'

export default {
  name: 'App',
  components: {
    Tabs,
    Workers,
    Tracks,
    Train,
    Welcome,
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
$primary: #828EFF;
@import 'node_modules/bootstrap/scss/bootstrap';
@import 'node_modules/bootstrap-vue/src/index.scss';

:root{
  --trainBlue: #828EFF;
  --trainAccentBlue: #4472CA;
}

body{
  margin: 0;
  padding: 0;
}

h1, h2, h3, h4 {
  font-family: 'Roboto', sans-serif;
  font-weight: 600 !important;
  margin: 0 !important;
}

#app {
  text-shadow: 1px 1px 1px rgba(0,0,0,0.004);
  text-rendering: optimizeLegibility !important;
  -webkit-font-smoothing: antialiased !important;
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
