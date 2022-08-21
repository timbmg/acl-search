<template>
  <div class="search-bar input-group input-group-lg">
    <input 
        ref="searchInput"
        type="search" 
        class="form-control" 
        id="query" 
        v-model="query" 
        @input="search"
        placeholder="Search for a publication"
    >
  </div>
</template>

<script>

import { ref, onMounted, nextTick } from 'vue';
import axios from 'axios'

export default {
    name: 'SearchBar',
    props: {},
    data() {
        return {
            query: '',
            took: null,
            publications: []
        }
    },
    setup() {
        const searchInput = ref(null);

        onMounted(() => {
            nextTick(() => {
                searchInput.value.focus();
            });
        });

        return {
            searchInput
        };
    },
    methods: {
        search() {
            var start = new Date().getTime();
            axios.get(`${process.env.VUE_APP_SEARCH_URL}/api/search/publications?query=${this.query}`)
            .then(response => {
                this.took = new Date().getTime() - start;
                this.publications = response.data
                this.$emit('search', this.publications)
            })
            .catch(error => {console.log(error)})
        }
    }
}
</script>

<style>
.search-bar {
    max-width: 756px;
    margin-bottom: 32px;
}
</style>
