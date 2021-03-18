from flask import request
from draft.BionicEye.singelton_classes.db_manager import DBManager
from draft.BionicEye.singelton_classes.os_manager import OSManager
from draft.BionicEye.models import Frame, Metadata

DB_MANAGER = DBManager()
OS_MANAGER = OSManager()


def download_tagged_frames():
    """
    Downloads the tagged frames from the video given in the request
    """
    video_id = request.args.get("video_id")
    tagged_frame_paths = DB_MANAGER.query(Frame.frame_path).filter_by(video_id=video_id).join(Metadata)\
        .filter(Metadata.frame_tag == 'True').all()
    os_paths = [path for (path,) in tagged_frame_paths]

    OS_MANAGER.download_files(os_paths)
