from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import os
from BionicEye.src.singelton_classes.singelton_meta import SingletonMeta


load_dotenv()

CONNECTION_STRING = os.getenv('CONNECTION_STRING')
OS_CONTAINER = os.getenv('OS_CONTAINER')
TEST_OS_CONTAINER = os.getenv('TEST_OS_CONTAINER')
MAX_THREADS = 100
DOWNLOADS_DIR = os.path.join(os.getcwd(), 'downloads')


class OSManager(metaclass=SingletonMeta):
    def __init__(self, testing=False):
        """
        Stores connection to the os and creates the container if it doesn't exist
        """
        try:
            self.blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
            if testing:
                self.blob_service_client.create_container(TEST_OS_CONTAINER)
            else:
                self.blob_service_client.create_container(OS_CONTAINER)
        except ResourceExistsError:
            pass
        except ValueError:
            raise Exception("Can't connect to to azure blob storage")

    def upload_file(self, paths):
        """
        Uploads a given file to the os
        :param paths: tuple with the file path to upload and the os path it will be saved in
        """
        file_path = paths[0]
        os_path = paths[1]
        blob_client = self.blob_service_client.get_blob_client(container=OS_CONTAINER, blob=os_path)

        if not blob_client.exists():
            print("\nUploading to Azure Storage as blob")
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data)
            print('done uploading!')
        else:
            print('blob already exists')

    def upload_dir(self, dir_path, dir_os_path):
        """
        Uploads all files in the given directory to the os with multithreading.
        The files will be saved in the os with their relative path
        :param dir_path: path to the directory
        :param dir_os_path: the os path of the dir
        """
        args = []

        for file_name in os.listdir(dir_path):
            file_path = os.path.join(os.path.abspath(dir_path), file_name)
            if not os.path.isfile(file_path):
                raise Exception("Can't save dir to os")

            file_os_path = os.path.join(dir_os_path, file_name)
            args.append((file_path, file_os_path))

        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            executor.map(self.upload_file, args)

    def download_file(self, os_path):
        """
        Downloads a file from the os
        :param os_path: path to the blob we want to download
        """
        blob_client = self.blob_service_client.get_blob_client(container=OS_CONTAINER, blob=os_path)
        download_file_path = os.path.join(DOWNLOADS_DIR, str(os_path))
        os.makedirs(os.path.dirname(download_file_path), exist_ok=True)
        with open(download_file_path, "wb") as file:
            try:
                file.write(blob_client.download_blob().readall())
            except ResourceNotFoundError:
                print("The file doesn't exist in the os")

    def download_files(self, os_path_list):
        """
        Downloads files from the os with multithreading
        :param os_path_list: list of os paths to the blobs we want to download
        """
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            executor.map(self.download_file, [path for path in os_path_list])
