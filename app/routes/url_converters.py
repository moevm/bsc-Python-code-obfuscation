from werkzeug import routing

from app.database import db_engine


class StorageTypeURLConverter(routing.BaseConverter):
    def to_python(self, value):
        try:
            converted_type = db_engine.StorageType(value)
        except ValueError:
            raise routing.ValidationError('invalid storage type(={value})')
        else:
            return converted_type


    def to_url(self, value):
        return value.value


class ObjectIdURLConverter(routing.BaseConverter):
    def to_python(self, value):
        try:
            converted_id = db_engine.DBEngine.convert_to_id(value)
        except ValueError:
            raise routing.ValidationError('invalid database identifier(={value})')
        else:
            return converted_id


    def to_url(self, value):
        return str(value)


class DBViewTypeConverter(routing.BaseConverter):
    def to_python(self, value):
        try:
            converted_type = db_engine.DBViewType(value)
        except ValueError:
            raise routing.ValidationError('invalid database view type(={value})')
        else:
            return converted_type


    def to_url(self, value):
        return value.value
