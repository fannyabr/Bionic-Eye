from BionicEye.singelton_classes.db_manager import DBManager
from BionicEye.singelton_classes.os_manager import OSManager
from BionicEye.models import Frame

DB_MANAGER = DBManager()
OS_MANAGER = OSManager()


def get_video_frames(video_id):
    """
    Gets from the db all the frame paths from the video given in the request
    :param video_id: id of a video in the db
    :return: list of frame paths in the os
    """
    frame_paths = DB_MANAGER.query(Frame.frame_path).filter_by(video_id=video_id).all()

    return [path for (path,) in frame_paths]
