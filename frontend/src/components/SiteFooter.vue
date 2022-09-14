<template>
  <footer>
    <div class="container">
      <div class="row" style="max-width: 1140px">
        <!-- <div class="col-1"></div> -->
        <div class="col-9" style="max-width: 360px">
          <h5>&#9749; Sponsor</h5>
          If you find this little website helpful, please consider
          <a href="https://ko-fi.com/timbmg" target="_blank">supporting </a>
          <del>my caffine addiction</del> its further development with a cup of
          coffee (if you can afford). Or leave a star
          <i class="bi bi-star-fill"></i> on
          <u
            ><a href="https://github.com/timbmg/acl-search" target="_blank"
              >github</a
            ></u
          >.
        </div>
        <div class="col-3" style="max-width: 360px">
          <h5>&#128279; Links</h5>
          <div>
            <a href="/contact"><i class="bi bi-envelope"></i> Contact</a>
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
          <div>
            <a href="https://aclanthology.org" target="_blank"
              ><i class="bi bi-book"></i> ACL Anthology</a
            >
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: "SiteFooter",
};
</script>
<style>
footer {
  margin-top: 20px;
  padding: 20px;
  padding-left: var(--bs-gutter-x, 0.75rem);
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
