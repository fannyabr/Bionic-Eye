from BionicEye.singelton_classes.singelton_meta import SingletonMeta
from BionicEye.app import db


class DBManage(metaclass=SingletonMeta):
    def __init__(self):
        self.db = db
        self.db.create_all()

    def save(self, db_object):
        self.db.session.add(db_object)
        self.db.session.commit()

    def query(self, col):
        return self.db.session.query(col)
