from logging.config import fileConfig

from celery import Celery
from celery.signals import setup_logging

from index.settings import RabbitMQSettings, RedisSettings


rabbit_mq_settings = RabbitMQSettings()
redis_settings = RedisSettings()


app = Celery(
    "index",
    backend=redis_settings.connection_string,
    broker=rabbit_mq_settings.connection_string,
    include=["index.tasks.tasks"],
)


@setup_logging.connect
def config_loggers(*args, **kwargs):
    fileConfig("/app/logging.conf")
