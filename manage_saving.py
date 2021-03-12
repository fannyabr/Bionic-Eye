from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import os

from BionicEye.app import db

load_dotenv()

CONNECTION_STRING = os.getenv('CONNECTION_STRING')
OS_CONTAINER = os.getenv('OS _CONTAINER')
MAX_THREADS = 10


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance

        return cls._instances[cls]


class DBManage(metaclass=SingletonMeta):
    def __init__(self):
        self.db = db
        self.db.create_all()

    def save(self, db_object):
        self.db.session.add(db_object)
        self.db.session.commit()

    def query(self, col):
        return self.db.session.query(col)


class OSManage(metaclass=SingletonMeta):
    def __init__(self):
        self.blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
        try:
            self.blob_service_client.create_container('bionic-eye')
        except ResourceExistsError:
            pass

    def upload_file(self, file_path):
        """
        Uploads a given file to the container in he storage
        :param file_path: the file that will be uploaded
        """
        blob_path = os.path.relpath(file_path)
        blob_client = self.blob_service_client.get_blob_client(container='bionic-eye', blob=blob_path)
        if not blob_client.exists():
            print("\nUploading to Azure Storage as blob")
            print(file_path)
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data)
            print('done uploading!')

    def upload_dir(self, dir_path):
        """
        Uploads list of files to the container in the storage with multithreading
        """
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            executor.map(self.upload_file, [os.path.join(os.path.relpath(dir_path), file_name)
                                            for file_name in os.listdir(dir_path)])
