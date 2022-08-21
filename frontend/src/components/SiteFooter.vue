<template>
  <footer>
    <div class="row" style="max-width:1140px; margin: 0 auto">
      <!-- <div class="col-1"></div> -->
      <div class="col-6" style="max-width:360px">
        <h5> &#9749; Sponsor</h5>
        If you find this little website helpful, please consider <a href="https://ko-fi.com/timbmg" target="_blank">supporting</a> <del>my caffine addiction</del> its further development with a cup of coffee.
      </div>
      <div class="col-6" style="max-width:360px">
        <h5>&#128279;	Links</h5>
        <div><a href="https://aclanthology.org" target="_blank">ACL Anthology</a></div>
        <div><a href="https://github.com/timbmg/acl-search" target="_blank">Github</a></div>
        <div><a href="https://twitter.com/timbmg" target="_blank">Twitter</a></div>
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
  position: absolute;
  bottom: 0;
  width: 100%;
  /* Set the fixed height of the footer here */
  padding: 20px;
  height: 160px;
  background-color: #f5f5f5;
}
.row {
  text-align: left;
}
a:link {
  text-decoration: none;
}

</style>
