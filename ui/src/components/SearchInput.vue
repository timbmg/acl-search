<template>
  <div>
    <b-form-input v-model="query" placeholder="Search ACL Anthology Publications" outline @input="queryInput"></b-form-input>
    <div class="resultsWrapper">
      <div class="searchStats" v-if="publications">{{publications.length}} results in {{took}}ms</div>
      <div class="searchResults" v-if="publications">
        <div v-for="(publication, index) in publications" :key="index">
          <div class="publication">
            <a 
              class="publicationAnchor" 
              v-bind:href="aclanthologyUrl(publication.url)"
              target="_blank"
            >
              <b-card 
                v-bind:title="publication.title" 
                v-bind:sub-title="flattenAuthors(publication.authors)"
              >
                <b-card-text>
                  {{publication.conference_short.toUpperCase()}} {{publication.year}}
                </b-card-text>
              </b-card>
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'SearchInput',
  props: {
  },
  data () {
    return {
      query: null,
      publications: null,
      took : null,
    }
  },
  methods: {
    queryInput (value) {
      var start = new Date().getTime();

      this.query = value;

      axios.get(`${process.env.VUE_APP_SEARCH_URL}/api/search/publications?query=${this.query}`)
        .then(response => {
          this.took = new Date().getTime() - start;
          this.publications = response.data
        })
        .catch(error => {console.log(error)})

    },
    flattenAuthors(authors) {
      var out = []; 
      for (var i=0; i<authors.length; i++) {  
        out.push(authors[i]["firstname"] + " " + authors[i]["lastname"]); 
      } 
      return out.join(", ");
    },
    aclanthologyUrl(url) {
      return "https://aclanthology.org/" + url;
    }
  },
}
</script>

<style scoped>
.searchResults {
  text-align: left;
}
.publication {
  margin-top: 20px;
}
.publicationAnchor {
  text-decoration: none;
}
</style>
