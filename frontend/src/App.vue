<template>
  <div class="container-md">
    <div class="row">
      <div class="col-md-1">
        <img src="/aclsearch.png" alt="ACL Search" class="img-fluid">
      </div>
      <div class="col-md-6">
        <SearchBar @search="searchResultPublications"/>
      </div>
    </div>
    <div class="row" v-for="(publication, publicationIndex) in publications" :key="publicationIndex">
      <div class="col gy-3">
        <SearchResult :publication="publication"/>
      </div>
    </div>
  </div>
</template>

<script>
import SearchBar from './components/SearchBar.vue'
import SearchResult from './components/SearchResult.vue'
// import SearchFilter from './components/SearchFilter.vue'

export default {
  name: 'App',
  components: {
    SearchBar, 
    SearchResult
    // SearchFilter
  },
  data() {
    return {
      publications: null
    }
  },
  methods: {
    searchResultPublications(v) {
      this.publications = v
    },
    setSearchFilters(v) {
      this.filters = v
    }
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
