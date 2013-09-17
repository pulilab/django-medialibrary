import datetime

def setup_upload_route(instance, filename=None):
    today = datetime.datetime.today()
    return '%s/%s-%02d-%02d/%s' % (instance.shelf.__class__.__name__.lower(),
                                       today.year, today.month, today.day,
                                       filename)

content_type_restriction = None