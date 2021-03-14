import os
from flask import request
from BionicEye.singelton_classes.db_manager import DBManager
from BionicEye.models import Video
from BionicEye.video_manipulation_functions.videos import save_video
from BionicEye.video_manipulation_functions.frames import save_frames

DB_MANAGER = DBManager()
VIDEOS_DIR = os.path.join(os.getcwd(), 'videos')


def add_video():
    """
    Gets video file in a post request and saves it to the db and the os
    """
    # from BionicEye.video_manipulation_functions.video_manipulation import save_video, save_frames

    uploaded_file = request.files['file']
    video_path = os.path.join(VIDEOS_DIR, uploaded_file.filename)
    _, extension = os.path.splitext(video_path)

    if extension != '.mp4':
        raise Exception('File type should be mp4')

    uploaded_file.save(video_path)
    save_video(video_path)
    save_frames(video_path)


def get_video_paths():
    """
    Get all video paths from the db
    :return: json object with the list of paths
    """
    video_paths = DB_MANAGER.query(Video.video_path).all()

    return [path for (path,) in video_paths]
