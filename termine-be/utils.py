import json

from datetime import date, datetime

class JSONExtendedEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, date):
            return (str(z))
        elif isinstance(z, datetime):
            return (str(z))
        else:
            return super().default(z)
