from BionicEye.src.singelton_classes.db_manager import DBManager
from BionicEye.src.singelton_classes.os_manager import OSManager
from BionicEye.src.models import Frame, Metadata


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


def get_frame(video_id, frame_index):
    """
    Gets from the db the frame path with the index and video id given in the request
    :param video_id: id of a video in the db
    :param frame_index: index of a frame in the video
    :return: path of the frame in the os
    """
    frame_path = DB_MANAGER.query(Frame.frame_path).filter_by(video_id=video_id, frame_index=frame_index).one_or_none()

    return frame_path


def download_tagged_frames(video_id):
    """
    Downloads the tagged frames from the video given in the request
    :param video_id: id of a video in the db
    """
    tagged_frame_paths = DB_MANAGER.query(Frame.frame_path).filter_by(video_id=video_id).join(Metadata)\
        .filter(Metadata.frame_tag == 'True').all()
    os_paths = [path for (path,) in tagged_frame_paths]

    OS_MANAGER.download_files(os_paths)
