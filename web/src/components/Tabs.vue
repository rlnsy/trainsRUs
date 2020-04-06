<template>
  <div class="tabs">
    <button
      class="active"
      id="0"
      @click="handleClick(0)"
    >
      Welcome
    </button>
    <button
      id="1"
      @click="handleClick(1)"
    >
      Workers
    </button>
    <button
      id="2"
      @click="handleClick(2)"
    >
      Tracks
    </button>
    <button
      id="3"
      @click="handleClick(3)"
    >
      Train
    </button>
  </div>
</template>

<script>
export default {
  name: 'Tabs',
  methods: {
      handleClick(k) {
          var buttons = document.querySelectorAll(".tabs > button")
          buttons.forEach(button => button.classList.remove("active"))
          buttons.item(k).classList.add("active")
          this.$emit('clicked', k)
      },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.tabs {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 130px;
  background-color: #414141;
  overflow: hidden;

  > button {
      font-size: 18px;
      font-family: 'Roboto', sans-serif;  
      border: 0;
      padding: 0;
      display: flex;
      height: 110px;
      justify-content: center;
      align-items: center;
      border-bottom: lightgray solid 1px;
      background-color: white;
      color: black;
  }

  > .active {
      color: white;
      background-color: var(--trainBlue);
      border-bottom: var(--trainBlue) solid 1px;
  }

  > button:hover{
      background-color: var(--trainBlue);
      color: white;
      border-bottom: var(--trainBlue) solid 1px;
  }
}
</style>
