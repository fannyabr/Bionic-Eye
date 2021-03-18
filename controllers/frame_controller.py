from flask import request
from draft.BionicEye.singelton_classes.db_manager import DBManager
from draft.BionicEye.singelton_classes.os_manager import OSManager
from draft.BionicEye.models import Frame

DB_MANAGER = DBManager()
OS_MANAGER = OSManager()


def get_video_frames():
    """
    Gets from the db all the frame paths from the video given in the request
    :return: list of frame paths in the os
    """
    video_id = request.args.get("video_id")

    frame_paths = DB_MANAGER.query(Frame.frame_path).filter_by(video_id=video_id).all()

    return [path for (path,) in frame_paths]
