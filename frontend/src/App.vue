<template>
  <div id="app" class="container-fluid">
    <!-- <router-view/> -->
    <app-header></app-header>
    <div class="container-fluid">
        <app-main></app-main>
    </div>
  </div>
</template>

<script>
import appHeader from "./components/AppHeader.vue"
import appMain from "./components/AppMain.vue"

export default {
  name: 'app',
  components : {
    "app-header": appHeader,
    "app-main": appMain
  }
}
</script>

<style>
  body {
    padding-top: 4rem;
  }
</style>
