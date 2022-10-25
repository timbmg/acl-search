<template>
  <section id="Contact">
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
            <h1>Contact</h1>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col gy-3">
          <h3>Tim Baumgärnter</h3>
          <div>
            <a href="mailto:baumgaertner.t@gmail.com?subject=[ACL Search]: "
              ><i class="bi bi-envelope"></i> baumgaertner.t@gmail.com</a
            >
          </div>
          <div>
            <a href="https://twitter.com/timbmg" target="_blank"
              ><i class="bi bi-twitter"></i> @timbmg</a
            >
          </div>
          <div>
            <a href="https://github.com/timbmg/acl-search" target="_blank"
              ><i class="bi bi-github"></i> timbmg/acl-search</a
            >
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
