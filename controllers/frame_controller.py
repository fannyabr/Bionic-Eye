from flask import request
from draft.BionicEye.singelton_classes.db_manager import DBManager
from draft.BionicEye.singelton_classes.os_manager import OSManager
from draft.BionicEye.models import Frame

DB_MANAGER = DBManager()
OS_MANAGER = OSManager()


def get_frame():
    """
    Gets from the db the frame path with the index and video id given in the request
    :return: path of the frame in the os
    """
    video_id = request.args.get("video_id")
    frame_index = request.args.get("frame_index")
    frame_path = DB_MANAGER.query(Frame.frame_path).filter_by(video_id=video_id, frame_index=frame_index).one_or_none()

    return frame_path
