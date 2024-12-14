from mongoengine import Document, StringField, IntField, BooleanField, DictField, EmbeddedDocument, EmbeddedDocumentField, ObjectIdField

class Properties(EmbeddedDocument):
    distinct_id = StringField(required=True)
    session_id = StringField(required=True)
    journey_id = StringField(required=True)
    current_url = StringField(required=True)
    host = StringField(required=True)
    pathname = StringField(required=True)
    browser = StringField(required=True)
    device = StringField(required=True)
    referrer = StringField(required=True)
    referring_domain = StringField(required=True)
    screen_height = IntField(required=True)
    screen_width = IntField(required=True)
    eventType = StringField(required=True)
    elementType = StringField(required=True)
    elementText = StringField(required=True)
    elementAttributes = DictField()
    timestamp = StringField(required=True)
    x = IntField(required=True)
    y = IntField(required=True)
    mouseButton = IntField(required=True)
    ctrlKey = BooleanField(required=True)
    shiftKey = BooleanField(required=True)
    altKey = BooleanField(required=True)
    metaKey = BooleanField(required=True)

class Event(Document):
    event = StringField(required=True)
    properties = EmbeddedDocumentField(Properties, required=True)
    timestamp = StringField(required=True)
    _id = ObjectIdField()

    meta = {
        'collection': 'events'
    }