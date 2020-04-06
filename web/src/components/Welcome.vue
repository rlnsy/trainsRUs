<template>
  <div class="welcome text-center">
    <h2>Welcome to Trains'R'Us!</h2><br>
    <img
      src="@/assets/train.png"
      alt="train wallpaper"
    ><br>
    <p>This is a database management website for a railway corperation</p><br>
    <p>
      For HR, manage all employees in <b>'Workers'</b><br>
      For maintenance employees, view track status in <b>'Tracks'</b><br>
      For on-train employees, view shifts and check tickets in <b>'Train'</b>
    </p>
  </div>
</template>

<script>
export default {
    name: 'Welcome',
}
</script>

<style lang="scss" scoped>
.welcome{
    height: 100%;
    width: 100%;
    margin-top: 15vh;
    display:flex;
    flex-direction: column;
    align-content: center;
    align-items: center;
    font-size: 22px;
    > img {
        height: 300px;
        width: auto;
    }
}
</style>