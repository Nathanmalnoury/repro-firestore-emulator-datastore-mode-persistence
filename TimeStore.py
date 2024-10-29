from google.cloud import ndb


class TimeStore(ndb.Model):
    timestamp = ndb.DateTimeProperty()
