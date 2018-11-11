import copy

from django.db.backends.base.creation import BaseDatabaseCreation
from djangotoolbox.db.base import NonrelDatabaseFeatures, NonrelDatabaseWrapper, NonrelDatabaseOperations, \
    NonrelDatabaseIntrospection, NonrelDatabaseValidation, NonrelDatabaseClient
from djangotoolbox.db.creation import NonrelDatabaseCreation
from shotgun_api3 import Shotgun


class DatabaseFeatures(NonrelDatabaseFeatures):
    supports_microsecond_precision = False
    supports_long_model_names = False
    can_rollback_ddl = False


class DatabaseOperations(NonrelDatabaseOperations):

    def sql_flush(self, style, tables, sequences, allow_cascade=False):
        return []


class DatabaseCreation(NonrelDatabaseCreation):

    def _create_test_db(self, verbosity, autoclobber, keepdb=False):
        pass


class DatabaseIntrospection(NonrelDatabaseIntrospection):

    def django_table_names(self, only_existing=False, include_views=True):
        return None


class DatabaseValidation(NonrelDatabaseValidation):
    pass

class DatabaseClient(NonrelDatabaseClient):
    pass


class DatabaseWrapper(NonrelDatabaseWrapper):
    client_class = DatabaseClient
    features_class = DatabaseFeatures
    ops_class = DatabaseOperations
    introspection_class = DatabaseIntrospection
    validation_class = DatabaseValidation
    creation_class = DatabaseCreation

    def __init__(self, settings_dict, *args, **kwargs):

        super(DatabaseWrapper, self).__init__(settings_dict, *args, **kwargs)

        self.connected = False
        del self.connection


    def connect(self):
        settings = copy.deepcopy(self.settings_dict)

        db_url = getattr(settings, 'SHOTGUN_URL', None)
        script_name = getattr(settings, 'SHOTGUN_SCRIPT_NAME', None)
        api_key = getattr(settings, 'SHOTGUN_KEY', None)

        self.connected = True
        self.connection = Shotgun(base_url=db_url, script_name=script_name, api_key=api_key)


    def _reconnect(self):
        if self.connected:
            del self.connected
            del self.database
            self.connected = False
        self.connect()

    def _cursor(self):
        return ShotgunCursor()

    def get_autocommit(self):
        pass

    def _commit(self):
        pass

    def _rollback(self):
        pass

    def close(self):
        pass

class ShotgunCursor(object):

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __getattribute__(self, name):
        raise Database.NotSupportedError("Cursors are not supported.")

    def __setattr__(self, name, value):
        raise Database.NotSupportedError("Cursors are not supported.")

    def execute(self, *args, **kwargs):
        pass


class Database(object):
    class Error(Exception):
        pass

    class InterfaceError(Error):
        pass

    class DatabaseError(Error):
        pass

    class DataError(DatabaseError):
        pass

    class OperationalError(DatabaseError):
        pass

    class IntegrityError(DatabaseError):
        pass

    class InternalError(DatabaseError):
        pass

    class ProgrammingError(DatabaseError):
        pass

    class NotSupportedError(DatabaseError):
        pass