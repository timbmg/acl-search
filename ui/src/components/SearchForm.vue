<template>
   <input
      placeholder=""
      outline
      v-model="query"
      @input="onInput"
    />
    <va-list v-if="publications">
    <va-list-label>
      Publications
    </va-list-label>

    <va-list-item
      v-for="(publication, index) in publications"
      :key="index"
    >

      <va-list-item-section>
        <va-list-item-label>
          {{ publication.title }}
        </va-list-item-label>

        <va-list-item-label caption>
          <span v-for="(author, indexAuthor) in publication.authors" :key="indexAuthor">
            <span v-if="indexAuthor != 0">, </span>
            <span>{{ author.lastname }}</span>
          </span>
        </va-list-item-label>
      </va-list-item-section>

    </va-list-item>
  </va-list>

</template>

<script>
import axios from 'axios'

export default {
  name: 'SearchForm',
  props: {
  },
  data () {
    return {
      query: null,
      publications: null,
    };
  },
  methods: {
    onInput: function(e) {
      console.log("onInput", e)
      this.query = e.target.value
      axios
      .get(`http://localhost:8000/api/index/publication?query=${this.query}`)
      .then(response => (this.publications = response.data))
    },
    onSubmit: function(e) {
      console.log("onSubmit", e)
    }
  }
};
</script>

<style scoped>
</style>
