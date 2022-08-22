<template>
  <footer>
    <div class="container">

    
    <div class="row" style="max-width:1140px">
      <!-- <div class="col-1"></div> -->
      <div class="col-8" style="max-width:360px">
        <h5> &#9749; Sponsor</h5>
        If you find this little website helpful, please consider <a href="https://ko-fi.com/timbmg" target="_blank">supporting</a> <del>my caffine addiction</del> its further development with a cup of coffee.
      </div>
      <div class="col-4" style="max-width:360px">
        <h5>&#128279;	Links</h5>
        <div><a href="https://aclanthology.org" target="_blank"><i class="bi bi-book"></i> ACL Anthology</a></div>
        <div><a href="https://github.com/timbmg/acl-search" target="_blank"><i class="bi bi-github"></i> Github</a></div>
        <div><a href="https://twitter.com/timbmg" target="_blank"><i class="bi bi-twitter"></i> Twitter</a></div>
      </div>
    </div>
    </div>
  </footer>
</template>

<script>
export default {
    name: "SiteFooter",

}
</script>
<style>

footer {
  margin-top: 20px;
  padding: 20px;
  padding-left: var(--bs-gutter-x,.75rem);
  height: 160px;
  background-color: #f5f5f5;

}
.row {
  text-align: left;
}
a {

  color: #2c3e50;
}
a:link {
  text-decoration: none;
}

</style>
