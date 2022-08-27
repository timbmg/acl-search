<template>
  <div class="card">
    <h5 class="card-title tooltip-test" :title="'Score='+score">
        {{publication.title}}
    </h5>
    <div class="card-subtitle">
      <span class="tooltip-test" title="Go to ACL Anthology"><a :href="aclUrl" target="_blank">&#128213;</a></span>
      <span class="bibkey tooltip-test" @click="copyBibtexToClipboard" title="Copy Bibkey">&#128221;</span>
      <span class="spacer"> | </span>
      <span>{{publication.venue_short}}</span> <span>{{publication.year}}</span> 
      <span class="spacer"> | </span>
      <span v-for="(author, authorIndex) in publication.authors" :key="authorIndex">
        {{author.firstname}} {{author.lastname}}<span v-if="authorIndex < publication.authors.length - 1">, </span>
      </span>
    </div>
  </div>
</template>

<script>
export default {
  name: "SearchResult",
  props: {
    publication: Object,
    score: Number
  },
  computed: {
    aclUrl() {
      return `https://aclanthology.org/${this.publication.url}`
    }
  },
  methods : {
    copyBibtexToClipboard() {
      navigator.clipboard.writeText(this.publication.bibkey)
    }
  }
}
</script>

<style>
.card {
  text-align: left;
  border: none;
}
.card-body {
  padding: 0;
}
a:link {
  text-decoration: none;
}
.spacer {
  padding-left: 6px;
  padding-right: 6px;
}
.bibkey {
  cursor: pointer;
}
</style>
