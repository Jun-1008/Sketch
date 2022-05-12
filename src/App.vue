<template>
  <div id="app">
    <RootView title="Sketch User Interface" />
  </div>
</template>

<script>
import RootView from "./components/RootView.vue";

export default {
  name: "App",
  components: {
    RootView
  },
  mounted: function() {},
  methods: {}
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
