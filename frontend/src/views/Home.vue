<template>
    <section id="Home">
      <div class="content container d-flex flex-column" style="min-height: calc(100vh - 240px)">
          <div style="margin-bottom: 32px;">
            <div class="row search-bar-row">
                <div class="col-1 d-none d-sm-none d-md-block align-middle">
                  <a href="/"><img src="/aclsearch.png" alt="ACL Search" width="56"/></a>
                </div>
                <div class="col-8">
                  <SearchBar @queryUpdate="queryUpdate"/>
                </div>
            </div>
            <div class="row">
                <div class="col-5 offset-sm-0 offset-md-1">
                  <SearchFilter 
                    :minYear="minYear" :maxYear="maxYear" @yearUpdate="yearUpdate" 
                    :venues="venues" @venuesUpdate="venuesUpdate" 
                  />
                </div>
                <div class="col-3 text-right font-weight-light stats">
                  <span v-if="hits != null && took != null" class="d-none d-md-block">{{hits}} results in {{took}} ms</span>
                  <span v-if="hits != null && took != null" class="d-md-none">{{hits}}#/{{took}}ms</span>
                </div>
            </div>
          </div>
          <div  v-if="publications">
            <div class="row" v-for="(publication, publicationIndex) in publications.search_results" :key="publicationIndex">
              <div class="col gy-3">
                <SearchResult :publication="publication.publication" :publicationIndex="publicationIndex" :score="publication.score"/>
              </div>
            </div>
            <div class="row">
              <div class="col gy-3 gx-3" >
                <button v-if="publications.search_results.length < hits" class="btn btn-primary btn-pagination" @click="loadMore">Load More</button>
                <a v-if="publications.search_results.length > 0" class="btn btn-primary btn-pagination" href="#" role="button">Back To Top</a>
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
      publications: null,
      took: null,
      hits: null,
      from: 0,
      size: 10,
      venues: [],
      venuesToInclude: [],
    }
  },
  mounted() {
    this.fetchVenues();
  },
  methods: {
    queryUpdate(query) {
      query = this.parseQuery(query);
      this.query = query;
      this.search();
    },
    parseQuery(query) {
      let venueStartIndex = query.search("v:");
      if (venueStartIndex != -1) {
        let venueEndIndex = query.indexOf(" ", venueStartIndex)
        if (venueEndIndex == -1) {
          venueEndIndex = query.length
        } 
        let venueParams = query.substring(venueStartIndex+2, venueEndIndex)
        this.venuesToInclude = venueParams.split(",").filter(venue => venue.length > 0)
        query = query.substring(0, venueStartIndex) + query.substring(venueEndIndex, query.length)
        console.log(query, venueStartIndex, venueEndIndex, this.venuesToInclude)
      }
      let yearStartIndex = query.search("y:");
      if (yearStartIndex != -1) {
        let yearEndIndex = query.indexOf(" ", yearStartIndex)
        if (yearEndIndex == -1) {
          yearEndIndex = query.length
        } 
        let yearParams = query.substring(yearStartIndex+2, yearEndIndex)
        if (yearParams.length == 4) {
          this.minYear = yearParams
          this.maxYear = yearParams
        } else if (yearParams.length == 9) {
          this.minYear = yearParams.substring(0, 4)
          this.maxYear = yearParams.substring(5, 9)
        }
        query = query.substring(0, yearStartIndex) + query.substring(yearEndIndex, query.length)
        console.log(query, yearStartIndex, yearEndIndex, this.minYear, this.maxYear)
      }

      return query
    },
    yearUpdate(values) {
      this.minYear = values[0];
      this.maxYear = values[1];
      this.search();
    },
    venuesUpdate(venues) {
      this.venuesToInclude = venues;
      this.search();
    },
    loadMore() {
      this.search(true);
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

      let params = new URLSearchParams();
      params.append('query', this.query);
      params.append('year_gte', this.minYear);
      params.append('year_lte', this.maxYear);
      params.append('from_', this.from);
      params.append('size', this.size);
      var venuesArray = Array.from(this.venuesToInclude)
      for (let i = 0; i < venuesArray.length; i++) {
        params.append('venues', venuesArray[i]);
      }
      
      var start = new Date().getTime();
      axios.get(
          `${process.env.VUE_APP_SEARCH_URL}/search/publications`,
          {
              params: params
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
    },
    fetchVenues() {
      axios.get(
          `${process.env.VUE_APP_SEARCH_URL}/venues`
      ).then(response => {
          this.venues = response.data;
          this.venues.sort(function (a, b) {
              var textA = a.acronym.toUpperCase();
              var textB = b.acronym.toUpperCase();
              return (textA < textB) ? -1 : (textA > textB) ? 1 : 0;
            }
          )
          this.selectedVenues = this.venues.filter(venue => venue.is_toplevel).map(venue => venue.acronym)
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
.stats {
  color: #6c757d;
  text-align: right;
}
</style>
