from azure.storage.blob import BlobServiceClient
from concurrent.futures import ThreadPoolExecutor
from azure.core.exceptions import ResourceNotFoundError
import os

CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
MAX_THREADS = 10


class BlobFileUploader:
    def __init__(self, container_name, files_dir=None):
        """
        Create object to mange the blob storage
        :param container_name: the container that organize set of blobs (stores files)
        :param files_dir: optional, if you want to upload all the files in the directory to the container
        """
        self.container_name = container_name
        self.files_dir = files_dir
        self.blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)

    def create_container(self):
        """
        Creates a container in the blob storage
        """
        self.blob_service_client.create_container(self.container_name)

    def delete_container(self):
        """
        Deletes a container in the blob storage
        """
        self.blob_service_client.delete_container(self.container_name)

    def upload_file(self, file_name):
        """
        Uploads a given file to the container in he storage
        :param file_name: the file that will be uploaded
        """
        blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=file_name)
        upload_file_path = os.path.join(self.files_dir, file_name)
        print("\nUploading to Azure Storage as blob")
        with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(data)
        print('done uploading!')

    def upload_all_files(self):
        """
        Uploads list of files to the container in the storage with multithreading
        """
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            executor.map(self.upload_file, [file for file in os.listdir(self.files_dir)])


if __name__ == '__main__':
    videos_container_name = 'videos'
    video_uploader = BlobFileUploader(videos_container_name)

    frames_container_name = 'frames'
    frames_uploader = BlobFileUploader(frames_container_name)

    try:
        # delete containers
        video_uploader.delete_container()
        frames_uploader.delete_container()

    except ResourceNotFoundError:
        print("Containers not found")
