import logging
from typing import Union

from celery.schedules import crontab
from celery.utils.log import get_task_logger
from celery.signals import worker_ready

from index.core import ACLClient, GithubClient, ElasticSearchClient
from index.core.celery import app as celery_app
from index.models.elasticsearch.file import File

logger = get_task_logger(__name__)

acl_client = ACLClient()
github_client = GithubClient()
elasticsearch_client = ElasticSearchClient()


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    logger.info("Setting up periodic tasks.")
    sender.add_periodic_task(
        # crontab(hour=0, minute=0),
        crontab(minute="*/10"),
        check_new_files_in_github.s(),
        name="check_new_files_in_github_every_day",
    )


@worker_ready.connect
def index_venues(**_):
    venues = acl_client.get_venues()
    for venue in venues:
        elasticsearch_client.index_venue(venue)


@celery_app.task
def check_new_files_in_github():
    logger.info("Checking for new files in github")

    files = github_client.get_all_files_from_repo(
        repo="acl-org/acl-anthology", dir="data/xml"
    )

    for file in files:

        if not file["name"].endswith(".xml"):
            continue

        es_file: Union[None, File] = elasticsearch_client.get_file_by_id(
            _id=file["name"]
        )

        files_scheduled = 0
        if es_file is None or es_file.last_modified < file["last_modified"]:
            task = index_publications_from_file.apply_async(
                (file,), countdown=files_scheduled * 60
            )
            files_scheduled += 1

            logger.info(
                "Scheduled to index from file={} with task_id={}.".format(
                    file["name"], task.id
                )
            )


@celery_app.task
def index_publications_from_file(file):

    xml = acl_client.get_xml_from_url(url=file["download_url"])

    venue = acl_client.get_venue_from_filename(filename=file["name"])

    for publication in acl_client.get_publications_from_xml(xml, venue):
        elasticsearch_client.index_publication(publication)

    elasticsearch_client.index_file(file)
