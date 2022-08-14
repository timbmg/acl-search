<template>
  <div id="app">
    <b-container fluid="sm">
      <b-row>
        <SearchInput/>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import SearchInput from './components/SearchInput.vue'

export default {
  name: 'App',
  components: {
    SearchInput
  }
}
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
