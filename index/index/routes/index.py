from fastapi import APIRouter, HTTPException

from index.core import ACLClient, ElasticSearchClient, GithubClient

router = APIRouter()
acl_client = ACLClient()
elasticsearch_client = ElasticSearchClient()
github_client = GithubClient()


@router.post("")
def update_index():
    pass


@router.post("/{year}/{conference}")
def update_index(year: int, conference: str):
    filename = f"{year}.{conference}.xml"
    file = github_client.get_file_from_repo(
        repo="acl-org/acl-anthology", dir="data/xml", filename=filename
    )
    if file is None:
        raise HTTPException(status_code=404, detail=f"File {filename} not found.")

    xml = acl_client.get_xml_from_url(file["download_url"])
    for publication in acl_client.get_publications_from_xml(xml):
        elasticsearch_client.index_publication(publication)


@router.get("/publication")
def get_publication(query: str):
    return elasticsearch_client.search_publications(query)
