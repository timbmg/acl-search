<template>
  <div class="container">
    <div class="row">
      <div class="col-1 d-sm-none d-md-block">
        <img src="/aclsearch.png" alt="ACL Search" class="img-fluid">
      </div>
      <div class="col-6">
        <SearchBar @search="searchResultPublications"/>
      </div>
    </div>
    <div class="row" v-for="(publication, publicationIndex) in publications" :key="publicationIndex">
      <div class="col gy-3">
        <SearchResult :publication="publication"/>
      </div>
    </div>
    <!-- <div v-if="publications">
      <button type="button" class="btn btn-primary" @click="loadMore">Load more</button>
    </div> -->
  </div>
  <div class="fixed-bottom container-fluid">
    <SiteFooter/>
  </div>
</template>

<script>
import SearchBar from './components/SearchBar.vue'
import SearchResult from './components/SearchResult.vue'
import SiteFooter from './components/SiteFooter.vue'
// import SearchFilter from './components/SearchFilter.vue'

export default {
  name: 'App',
  components: {
    SearchBar, 
    SearchResult,
    SiteFooter
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
.fixed-bottom {
  padding: 0;
}
body {
  margin-bottom: 200px;
}
</style>
