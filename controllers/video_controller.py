import os
from dotenv import load_dotenv
from BionicEye.singelton_classes.db_manager import DBManager
from BionicEye.singelton_classes.os_manager import OSManager
from BionicEye.models import Video
from BionicEye.video_manipulation_functions.videos import save_video
from BionicEye.video_manipulation_functions.frames import save_frames

DB_MANAGER = DBManager()
OS_MANAGER = OSManager()

load_dotenv()


def add_video(uploaded_file):
    """
    Gets video file in a post request and saves it to the db and the os
    :param uploaded_file: video file to save
    """
    video_name, extension = os.path.splitext(uploaded_file.filename)

    if extension not in os.getenv('VIDEO_EXTENSIONS'):
        raise TypeError("The file must be a video")

    os.makedirs(video_name, exist_ok=True)
    video_path = os.path.join(video_name, uploaded_file.filename)

    uploaded_file.save(video_path)
    save_video(video_path, video_path)
    save_frames(video_path)


def get_video_paths():
    """
    Get all video paths from the db
    :return: list of video paths in the os
    """
    video_paths = DB_MANAGER.query(Video.video_path).all()

    return [path for (path,) in video_paths]
