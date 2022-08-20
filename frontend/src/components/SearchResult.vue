<template>
  <div class="card">
    <h5 class="card-title">
      {{publication.title}}
    </h5>
    <div class="card-subtitle">
      <a :href="aclUrl" alt="Go to publication in ACL Antology"><span>&#128213;</span></a>
      <span class="bibkey" @click="copyBibtexToClipboard">&#128221;</span>
      <span class="spacer"> | </span>
      <span>{{publication.conference_short}}</span> <span>{{publication.year}}</span> 
      <span class="spacer"> | </span>
      <span v-for="(author, authorIndex) in publication.authors" :key="authorIndex">
        {{author.firstname}} {{author.lastname}}<span v-if="authorIndex < publication.authors.length - 1">, </span>
      </span>
    </div>
    <div class="card-body">
      
    </div>
  </div>
</template>

<script>
export default {
  name: "SearchResult",
  props: {
    publication: Object
  },
  methods : {
    aclUrl() {
      return `https://aclantology.org/${this.publication.url}`
    },
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
