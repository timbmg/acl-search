import logging
from typing import Union

from celery.schedules import crontab

from index.core import ACLClient, GithubClient, ElasticSearchClient
from index.core.celery import app as celery_app
from index.models.elasticsearch.file import File

logger = logging.getLogger(__name__)

acl_client = ACLClient()
github_client = GithubClient()
elasticsearch_client = ElasticSearchClient()


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    logger.info("Setting up periodic tasks.")
    sender.add_periodic_task(
        # crontab(hour=0, minute=0),
        crontab(minute="*/1"),
        # crontab(minute=0),
        check_new_files_in_github.s(),
        name="check_new_files_in_github_every_day",
    )


@celery_app.task
def check_new_files_in_github():
    logger.info("Checking for new files in github")

    files = github_client.get_all_files_from_repo(
        repo="acl-org/acl-anthology", dir="data/xml"
    )

    for file in files:
        es_file: Union[None, File] = elasticsearch_client.get_file_by_id(
            _id=file["name"]
        )
        scheduled = 0
        if es_file is None or es_file.last_modified < file["last_modified"]:
            task = index_publications_from_file.delay(file["name"])
            logger.info(
                "Scheduled to index from file={} with task_id={}.".format(
                    file["name"], task.id
                )
            )

            scheduled += 1
            if scheduled == 1:
                break


@celery_app.task
def index_publications_from_file(filename):

    logger.info("Indexing publications from file: {}".format(filename))

    file = github_client.get_file_from_repo(
        repo="acl-org/acl-anthology", dir="data/xml", filename=filename
    )
    if file is None:
        raise RuntimeError(f"File {filename} not found.")

    xml = acl_client.get_xml_from_url(file["download_url"])

    conference = acl_client.get_conference_from_filename(filename)

    for publication in acl_client.get_publications_from_xml(xml, conference):
        elasticsearch_client.index_publication(publication)

    elasticsearch_client.index_file(file)
