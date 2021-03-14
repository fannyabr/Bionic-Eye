from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import os
from BionicEye.singelton_classes.singelton_meta import SingletonMeta


load_dotenv()

CONNECTION_STRING = os.getenv('CONNECTION_STRING')
OS_CONTAINER = os.getenv('OS _CONTAINER')
MAX_THREADS = 100


class OSManage(metaclass=SingletonMeta):
    def __init__(self):
        """
        Stores connection to the os and creates the container if not exists
        """
        self.blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
        try:
            self.blob_service_client.create_container('bionic-eye')
        except ResourceExistsError:
            pass

    def upload_file(self, file_path):
        """
        Uploads a given file to the os
        :param file_path: the file that will be uploaded
        """
        blob_path = os.path.relpath(file_path)
        blob_client = self.blob_service_client.get_blob_client(container='bionic-eye', blob=blob_path)
        if not blob_client.exists():
            print("\nUploading to Azure Storage as blob")
            print(blob_path)
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data)
            print('done uploading!')

    def upload_dir(self, dir_path):
        """
        Uploads all files in the given directory to the os with multithreading
        :param dir_path: path to the directory
        """
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            executor.map(self.upload_file, [os.path.join(dir_path, file_name)
                                            for file_name in os.listdir(dir_path)])
