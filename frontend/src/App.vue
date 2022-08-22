<template>
  <div class="content container d-flex flex-column" style="min-height: calc(100vh - 220px)">
    <div style="margin-bottom: 32px;">
      <div class="row search-bar-row">
        <div class="col-1 d-none d-sm-none d-md-block align-middle">
          <img src="/aclsearch.png" alt="ACL Search" width="56">
        </div>
        <div class="col-11">
          <SearchBar @queryUpdate="queryUpdate"/>
        </div>
      </div>
      <div class="row">
        <div class="col-11 offset-1">
          <SearchFilter @yearUpdate="yearUpdate"/>
        </div>
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
  
  <div class="mt-auto">
    <SiteFooter/>
  </div>
</template>

<script>
import axios from 'axios'


import SearchBar from './components/SearchBar.vue'
import SearchResult from './components/SearchResult.vue'
import SiteFooter from './components/SiteFooter.vue'
import SearchFilter from './components/SearchFilter.vue'

export default {
  name: 'App',
  components: {
    SearchBar, 
    SearchResult,
    SiteFooter,
    SearchFilter
  },
  data() {
    return {
      query: '',
      minYear: null, 
      maxYear: null, 
      took: null,
      publications: null
    }
  },
  methods: {
    queryUpdate(query) {
      this.query = query;
      this.search();
    },
    yearUpdate(values) {
      this.minYear = values[0];
      this.maxYear = values[1];
      this.search();
    },
    search() {
      if (this.query.length == 0) {
        this.publications = null
          return
        }
      var start = new Date().getTime();
      console.log('searching for ' + this.query + ' from ' + this.minYear + ' to ' + this.maxYear)
      axios.get(
          `${process.env.VUE_APP_SEARCH_URL}/api/search/publications`,
          {
              params: {
                  query: this.query,
                  year_gte: this.minYear,
                  year_lte: this.maxYear
              }
          }
      ).then(response => {
          this.took = new Date().getTime() - start;
          this.publications = response.data
      })
      .catch(error => {console.log(error)})
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
.search-bar-row {
  margin-bottom: 12px;
}
</style>
