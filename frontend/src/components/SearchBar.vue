<template>
  <div class="search-bar input-group input-group-lg">
    <input 
        ref="searchInput"
        type="search" 
        class="form-control" 
        id="query" 
        v-model="query" 
        @input="this.$emit('queryUpdate', query)"
        placeholder="Search for a publication"
    >
  </div>
</template>

<script>

import { ref, onMounted, nextTick } from 'vue';


export default {
    name: 'SearchBar',
    data() {
        return {
            query: '',
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
    }
}
</script>

<style>
</style>
