from BionicEye.singelton_classes.singelton_meta import SingletonMeta
from BionicEye.app import db


class DBManager(metaclass=SingletonMeta):
    def __init__(self):
        """
        Stores db connection and creates all the tables
        """
        self.db = db
        self.db.create_all()

    def save(self, db_object):
        """
        Saves object to the db
        :param db_object: Object that represents row in one of the db tables
        """
        self.db.session.add(db_object)
        self.db.session.commit()

    def query(self, col):
        """
        Executes a query on the db
        :param col: col name from a table
        :return: the query
        """
        return self.db.session.query(col)
