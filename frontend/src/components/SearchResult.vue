<template>
  <div class="card publication-card">
    <h5 class="card-title tooltip-test" :title="'Score='+score">
      <a :href="aclUrl" target="_blank">
        📝 {{publication.title}}
      </a>
    </h5>
    <div class="card-subtitle">
      <span>&#127980; {{publication.venue_short}}</span> <span>{{publication.year}}</span> 
      <span class="spacer"> | </span>
      <span>✍️ </span>
      <span v-for="(author, authorIndex) in publication.authors" :key="authorIndex">
        {{author.firstname}} {{author.lastname}}<span v-if="authorIndex < publication.authors.length - 1">, </span>
      </span>
    </div>
    <div class="card-text">
      <button class="btn btn-outline-primary btn-sm" :id="`bibtext-copy-button-${publicationIndex}`" @click="copyBibtexToClipboard" title="Copy Bibkey"><i class="bi bi-clipboard2" :id="`bibtext-copy-icon-${publicationIndex}`"></i> BibTex</button>
      <button class="btn btn-outline-primary btn-sm abstract-button" type="button" data-bs-toggle="collapse" :data-bs-target="`#collapse-abs-${publicationIndex}`">
        <i class="bi bi-card-text"></i> Abstract
      </button>

      <div class="collapse col-9 abstract-card" :id="`collapse-abs-${publicationIndex}`" >
        <div class="card card-body p-2">
          {{publication.abstract}}
        </div>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: "SearchResult",
  props: {
    publication: Object,
    publicationIndex: Number,
    score: Number,
  },
  mounted() {
    if (this.publication.abstract.length == 0) {
      this.$el.querySelector('.abstract-button').classList.add('disabled')
    }
  },
  computed: {
    aclUrl() {
      return `https://aclanthology.org/${this.publication.url}`
    },
    bibTexIcon() {
      return `#bibtext-copy-icon-${this.publicationIndex}`
    },
    bibTexButton() {
      return `#bibtext-copy-button-${this.publicationIndex}`
    }
  },
  methods : {
    toggleClass(elem, classA, classB) {
      if (elem.classList.contains(classA)) {
        elem.classList.remove(classA)
        elem.classList.add(classB)
      } else {
        elem.classList.remove(classB)
        elem.classList.add(classA)
      }
    },
    async copyBibtexToClipboard() {
      navigator.clipboard.writeText(this.publication.bibkey)

      this.toggleClass(this.$el.querySelector(this.bibTexIcon), 'bi-clipboard2', 'bi-clipboard2-check')
      this.toggleClass(this.$el.querySelector(this.bibTexButton), 'btn-outline-primary', 'btn-primary')
      await new Promise(resolve => setTimeout(resolve, 3000));
      this.toggleClass(this.$el.querySelector(this.bibTexIcon), 'bi-clipboard2', 'bi-clipboard2-check')
      this.toggleClass(this.$el.querySelector(this.bibTexButton), 'btn-outline-primary', 'btn-primary')

    }
  }
}
</script>

<style>
.publication-card {
  text-align: left;
  border: none;
}
.abstract-card{
  margin-top: 6px;
}
.card-body {
  padding: 0;
}
a:link {
  text-decoration: none;
}
.spacer {
  padding-left: 3px;
  padding-right: 3px;
}
.bibkey {
  cursor: pointer;
}
.card-text button {
  margin-right: 6px;
}
</style>
