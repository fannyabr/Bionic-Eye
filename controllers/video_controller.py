import os
from flask import request, Response
from dotenv import load_dotenv
from BionicEye.singelton_classes.db_manager import DBManager
from BionicEye.singelton_classes.os_manager import OSManager
from BionicEye.models import Video
from BionicEye.video_manipulation_functions.videos import save_video
from BionicEye.video_manipulation_functions.frames import save_frames

DB_MANAGER = DBManager()
OS_MANAGER = OSManager()

load_dotenv()


def add_video():
    """
    Gets video file in a post request and saves it to the db and the os
    """
    uploaded_file = request.files['file']
    video_name, extension = os.path.splitext(uploaded_file.filename)
    os.makedirs(video_name, exist_ok=True)
    video_path = os.path.join(video_name, uploaded_file.filename)

    if extension not in os.getenv('VIDEO_EXTENSIONS'):
        return Response(status=422)
    else:
        uploaded_file.save(video_path)
        save_video(video_path)
        save_frames(video_path)
        return Response()


def get_video_paths():
    """
    Get all video paths from the db
    :return: json object with the list of paths
    """
    video_paths = DB_MANAGER.query(Video.video_path).all()

    return [path for (path,) in video_paths]
