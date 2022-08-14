from fastapi import APIRouter, HTTPException, Query

from index.core import ACLClient, ElasticSearchClient, GithubClient

router = APIRouter()
acl_client = ACLClient()
elasticsearch_client = ElasticSearchClient()
github_client = GithubClient()


@router.post("/{filename}")
def update_index(
    filename: str = Query(
        description="The filename of the ACL file in the acl-org/acl-anthology repository to update the index with"
    ),
):
    file = github_client.get_file_from_repo(
        repo="acl-org/acl-anthology", dir="data/xml", filename=filename
    )
    if file is None:
        raise HTTPException(status_code=404, detail=f"File {filename} not found.")

    xml = acl_client.get_xml_from_url(file["download_url"])
    try:
        conference = acl_client.get_conference_from_filename(filename)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    for publication in acl_client.get_publications_from_xml(xml, conference):
        elasticsearch_client.index_publication(publication)
