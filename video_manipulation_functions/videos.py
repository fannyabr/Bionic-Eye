import os
from BionicEye.models import Video
from BionicEye.singelton_classes.db_manager import DBManager
from BionicEye.singelton_classes.os_manager import OSManager
from BionicEye.video_manipulation_functions.frames import count_frames

DB_MANAGER = DBManager()
OS_MANAGER = OSManager()


def save_video(video_path, video_os_path):
    """
    Saves given video information to the db and the os if not exists already
    :param video_path: path to the video file we want to save
    :param video_os_path: path to the video file in the os
    """
    video_file_name = os.path.basename(video_path)
    observation_post_name = video_file_name.split('_')[0]
    frames_amount = count_frames(video_path)
    if not DB_MANAGER.query(Video.id).filter_by(video_path=video_os_path).one_or_none():
        video = Video(observation_post_name=observation_post_name,
                      video_path=video_os_path, frames_amount=frames_amount)
        DB_MANAGER.save(video)
    OS_MANAGER.upload_file((video_path, video_os_path))
