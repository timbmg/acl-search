
<div align="center">
<img src="imgs/aclsearch.png" width="200"/>
<h3>ACL Search</h3>
<p>An search-as-you-type web app for the <a href="https://aclanthology.org" target="_blank">ACL Anthology</a></p>
</div>

## Architecture
### Index
The index service checks for new files in the [ACL Anthology github](https://github.com/acl-org/acl-anthology/tree/master/data/xml) on a regular basis. If a file update is discovered, publications are imported into an Elasticsearch index. The schedule is implemented in the `index-beat` service using [celery beat](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html#periodic-tasks). The `index-worker` service processes and indexes the files that have been updated.

### Search
The search service provides an API to search through the publication index in Elasticsearch.


