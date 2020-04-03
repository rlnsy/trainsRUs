<template>
  <div id="app">
    <Tabs @clicked="handleSwitch"/>
    <span class="divider"></span>
    {{scene}}
  </div>
</template>

<script>
import Tabs from './components/Tabs.vue';

export default {
  name: 'App',
  components: {
    Tabs,
  },
  data() {
    return {
      scene: 0,
    }
  },
  methods: {
    handleSwitch(k){
      this.scene = k
    }
  },
};
</script>

<style lang="scss">
:root{
  --trainBlue: #828EFF;
}

body{
  margin: 0;
  padding: 0;
}

#app {
  font-family: 'Raleway', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100vh;
  width: 100vw;
  display: flex;
  overflow: hidden;
}

.divider{
  width: 7px;
  height: 100%;
  background-color: var(--trainBlue);
}
</style>
