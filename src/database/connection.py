from urllib.parse import quote

from mongoengine import connect

from config.settings import settings


def database_url() -> str:
    DATABASE_DOMAIN = settings.DATABASE_HOST
    encoded_password = quote(settings.DATABASE_PASSWORD.replace("%", "%%"))

    return f"mongodb://{settings.DATABASE_USER}:{encoded_password}@{DATABASE_DOMAIN}/{settings.DATABASE_NAME}?retryWrites=true&w=majority"

client = connect(host=database_url())
