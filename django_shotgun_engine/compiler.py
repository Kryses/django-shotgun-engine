from djangotoolbox.db.basecompiler import NonrelQuery


class ShotgunQuery(NonrelQuery):
    def __init__(self, compiler, fields):
        super(ShotgunQuery, self).__init__(compiler, fields)


