
<div align="center">
<img src="imgs/aclsearch.png" width="200"/>
<h3><a href="https://aclsear.ch" target="_blank">ACL Search</a></h3>
<p>A search-as-you-type web app for the <a href="https://aclanthology.org" target="_blank">ACL Anthology</a></p>
</div>


## Architecture
The search engine relies on [Elasticsearch](https://www.elastic.co/), specifically its [search-as-you-type](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-as-you-type.html) feature. Instead of only indexing full words, it creates n-grams of the text for faster retrieval.

The app is built based on the principles outlined in the [12 factor app](https://12factor.net/).

### Core Services
#### Search
The search service provides an API to search through the publication index in Elasticsearch. Currently, we search only for matches the title. Future updates will include search through available abstracts and for all pubications of a specific author.
#### Index
The index service checks for new files in the [ACL Anthology github](https://github.com/acl-org/acl-anthology/tree/master/data/xml) on a regular basis. If a file update is discovered, publications are imported into an Elasticsearch index. The schedule is implemented in the `index-beat` service using [celery beat](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html#periodic-tasks). The `index-worker` service processes and indexes the files that have been updated.



## Preview
<div align="center">
<img src="https://user-images.githubusercontent.com/11020443/190440903-1edf81a0-b796-4582-8b02-c412f8056f80.gif" width="768"/>
</div>

