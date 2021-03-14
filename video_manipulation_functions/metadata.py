from BionicEye.video_manipulation_functions.given_functions import generate_metadata, is_frame_tagged
from BionicEye.models import Metadata
from BionicEye.singelton_classes.db_manager import DBManager

DB_MANAGER = DBManager()


def save_metadata(frame):
    """
    Save frames metadata to db if not exists
    :param frame: frame from some video
    :return: db id of the metadata of the given frame
    """
    fov, azimuth, elevation = generate_metadata(frame)
    frame_tag = is_frame_tagged(frame)
    metadata_id = DB_MANAGER.query(Metadata.id) \
        .filter_by(frame_tag=frame_tag, camera_fov=fov, azimuth=azimuth, elevation=elevation) \
        .one_or_none()

    if not metadata_id:
        metadata = Metadata(frame_tag=frame_tag, camera_fov=fov, azimuth=azimuth, elevation=elevation)
        DB_MANAGER.save(metadata)
        metadata_id = DB_MANAGER.query(Metadata.id) \
            .filter_by(frame_tag=frame_tag, camera_fov=fov, azimuth=azimuth, elevation=elevation) \
            .one()

    return metadata_id
