from django.conf import settings


def is_debug():
    """
    Is debug mode?
    :return: True / False
    """
    return getattr(settings, 'DEBUG', True)

def get_db_url():
    database = getattr(settings, 'COUCHDB_DATABASES', {})
    return database.get('url')
