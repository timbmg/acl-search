<template>
    <section id="NotFound">
      <div
        class="content container d-flex flex-column"
        style="min-height: calc(100vh - 240px)"
      >
        <div style="margin-bottom: 32px">
          <div class="row search-bar-row">
            <div class="col-1 d-none d-sm-none d-md-block align-middle">
              <a href="/"><img src="/aclsearch.png" alt="ACL Search" width="56"/></a>
            </div>
            <div class="col-11">
              <h1>There's nothing here, except this cat &#128008;</h1>
            </div>
          </div>
        </div>
        
      </div>
      <div class="mt-auto">
        <SiteFooter />
      </div>
    </section>
  </template>
  <script>
  import SiteFooter from "@/components/SiteFooter.vue";
  export default {
    name: "Contact",
    components: {
      SiteFooter,
    },
  };
  </script>
  