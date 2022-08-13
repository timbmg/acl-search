<template>
   <input
      placeholder=""
      outline
      v-model="query"
      @input="onInput"
    />
    <ul>
      <li v-for="publication in publications"  :key="publication">
        {{publication.title}}
      </li>
    </ul>
    <!-- <div v-for="publication in publications">{{publication.title}}</div> -->
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
