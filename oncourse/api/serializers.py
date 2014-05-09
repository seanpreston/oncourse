from bson import json_util, objectid
import datetime
import json


class MongoJsonEncoderDecoder(json.JSONEncoder, json.JSONDecoder):
    """
    Provides a MongoDB-aware JSON encoder.

    This encoder can't handle some of the more esoteric types (e.g. Binary,
    Code, MaxKey/MinKey), but is good enough for most usage.

    The decoder will *not* convert ISO formatted dates and ObjectIds unless
    they use the right syntax, e.g.

        {"$date": <isodateformat>, "$id" <objectid>}

    Because we don't really want people using the API to submit JSON data
    in POST/PUT requests that looks like that.

    """

    def default(self, obj):
        """
        Handler for converting pymongo/python datatypes to JSON-compatible
        types.

        """
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        elif isinstance(obj, objectid.ObjectId):
            return unicode(obj)
        return json.JSONEncoder.default(self, obj)

    def decode(self, obj):
        """
        Handler for converting JSON strings to pymongo/python-compatible
        types.

        """
        return json_util.loads(obj)
