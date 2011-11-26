"""This module contains fields that depend on importing `bson`. `bson` is
as part of the pymongo distribution.
"""

from dictshield.base import BaseField, ShieldException

import bson

class ObjectIdField(BaseField):
    """An field wrapper around MongoDB ObjectIds.  It is correct to say they're
    bson fields, but I am unaware of bson being used outside MongoDB.
    """

    def __init__(self, auto_fill=True, **kwargs):
        self.auto_fill = auto_fill
        super(ObjectIdField, self).__init__(**kwargs)    

    def __set__(self, instance, value):
        """Convert any text values provided into Python UUID objects and
        auto-populate any empty values should auto_fill be set to True.
        """
        if not value and self.audo_fill is True:
            value = bson.objectid.ObjectId()

        if isinstance(value, (str, unicode)):
            value = bson.objectid.ObjectId(unicode(value))

        instance._data[self.field_name] = value
    
    def _jsonschema_type(self):
        return 'string'

    def for_python(self, value):
        try:
            return bson.objectid.ObjectId(unicode(value))
        except Exception, e:
            raise ShieldException('Invalid ObjectId', self.field_name, value)

    def for_json(self, value):
        return str(value)

    def validate(self, value):
        try:
            bson.objectid.ObjectId(unicode(value))
        except Exception, e:
            raise ShieldException('Invalid ObjectId', self.field_name, value)
