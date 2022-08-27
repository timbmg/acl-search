<template>
    <section id="Home">
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
                <div class="col-11 offset-sm-0 offset-md-1">
                  <SearchFilter @yearUpdate="yearUpdate"/>
                </div>
            </div>
          </div>
          <div  v-if="publications">
            <div class="row" v-for="(publication, publicationIndex) in publications.search_results" :key="publicationIndex">
              <div class="col gy-3">
                <SearchResult :publication="publication.publication"/>
              </div>
            </div>
            <div class="row">
              <div class="col gy-3 gx-3" >
                <button v-if="publications.search_results.length < hits" class="btn btn-outline-primary btn-pagination" @click="loadMore">Load More</button>
                <a v-if="publications.search_results.length > 0" class="btn btn-outline-primary btn-pagination" href="#Home" role="button">Back To Top</a>
              </div>
            </div>
            <div class="row">
              <div class="col-2 gy-3">
              
              </div>
            </div>
          </div>
          <!-- <div v-if="publications">
          <button type="button" class="btn btn-primary" @click="loadMore">Load more</button>
          </div> -->
      </div>
      
      <div class="mt-auto">
          <SiteFooter/>
      </div>
    </section>
</template>

<script>
import axios from 'axios'

import SearchBar from '@/components/SearchBar.vue'
import SearchResult from '@/components/SearchResult.vue'
import SiteFooter from '@/components/SiteFooter.vue'
import SearchFilter from '@/components/SearchFilter.vue'

export default {
  name: 'Home',
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
      publications: null,
      hits: 0,
      from: 0,
      size: 10
    }
  },
  // created() {
  //   this.query = this.$router.query.q
  // },
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
    loadMore() {
      this.search(true);
      console.log(this.publications.search_results.length);
    },
    search(push=false) {
      // this.$router.push({query: {q: this.query}})
      if (this.query.length == 0) {
        this.publications = null
          return
        }
      if (push) {
        this.from += this.size;
      } else {
        this.from = 0;
      }
      var start = new Date().getTime();
      console.log('searching for ' + this.query + ' from ' + this.minYear + ' to ' + this.maxYear)
      axios.get(
          `${process.env.VUE_APP_SEARCH_URL}/api/search/publications`,
          {
              params: {
                  query: this.query,
                  year_gte: this.minYear,
                  year_lte: this.maxYear,
                  from_: this.from,
                  size: this.size
              }
          }
      ).then(response => {
          this.took = new Date().getTime() - start;
          if (push) {
            this.publications.search_results.push(...response.data.search_results)
          } else {
            this.publications = response.data
            this.hits = response.data.hits
          }
      })
      .catch(error => {console.log(error)})
    }
  }
}
</script>

<style>
.search-bar-row {
  margin-bottom: 12px;
}
.btn-pagination {
  margin-right: 12px;
  width: 120px;
}
</style>
