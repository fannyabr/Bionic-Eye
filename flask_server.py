from flask import Response, request
from BionicEye.models import app
from BionicEye import models
from BionicEye.blob_storage import BlobFileUploader
from BionicEye.video_manipulation import save_video_to_db, save_frames
import os


@app.route('/addVideo', methods=['POST'])
def add_video():

    # Gets file in the request and saves it
    os.makedirs('videos', exist_ok=True)
    videos_dir = os.path.join(os.getcwd(), 'videos')
    uploaded_file = request.files['file']
    video_file = os.path.join(videos_dir, uploaded_file.filename)
    uploaded_file.save(video_file)

    # Create db
    models.db.create_all()

    # Upload video directory to the blob storage
    videos_container_name = 'videos'
    blob_videos_uploader = BlobFileUploader(videos_container_name, video_file)
    blob_videos_uploader.upload_file(video_file)

    save_video_to_db(video_file)
    save_frames(video_file)

    return Response()


if __name__ == '__main__':
    app.run()
