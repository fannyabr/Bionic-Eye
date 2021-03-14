import cv2
import shutil
import os
from BionicEye.video_manipulation_functions.given_functions import generate_metadata, is_frame_tagged
from BionicEye.app import Video, Metadata, Frame
from BionicEye.singelton_classes.db_manager import DBManage
from BionicEye.singelton_classes.os_manager import OSManage

DB_MANAGE = DBManage()
OS_MANAGE = OSManage()


def count_frames(video_path):
    """
    Counts frames in a video
    :param video_path: path to a video file
    :return: the amount of frames in the video
    """
    frame_number = 0
    cap = cv2.VideoCapture(video_path)
    read_correctly, frame = cap.read()

    while read_correctly:
        frame_number += 1
        read_correctly, frame = cap.read()

    return frame_number


def save_video(video_path):
    """
    Saves given video information to the db and the os if not exists already
    :param video_path: path to the video file we want to save
    """
    video_os_path = os.path.relpath(video_path)
    video_file_name = os.path.basename(video_path)
    observation_post_name = video_file_name.split('_')[0]
    frames_amount = count_frames(video_path)
    if not DB_MANAGE.query(Video.id).filter_by(video_path=video_os_path).first():
        video = Video(observation_post_name=observation_post_name,
                      video_path=video_os_path, frames_amount=frames_amount)
        DB_MANAGE.save(video)
    OS_MANAGE.upload_file(video_path)


def save_metadata(frame):
    """
    Save frames metadata to db if not exists
    :param frame: frame from some video
    :return: db id of the metadata of the given frame
    """
    fov, azimuth, elevation = generate_metadata(frame)
    frame_tag = is_frame_tagged(frame)
    metadata_id = DB_MANAGE.query(Metadata.id) \
        .filter_by(frame_tag=frame_tag, camera_fov=fov, azimuth=azimuth, elevation=elevation) \
        .first()

    if not metadata_id:
        metadata = Metadata(frame_tag=frame_tag, camera_fov=fov, azimuth=azimuth, elevation=elevation)
        DB_MANAGE.save(metadata)
        metadata_id = DB_MANAGE.query(Metadata.id) \
            .filter_by(frame_tag=frame_tag, camera_fov=fov, azimuth=azimuth, elevation=elevation) \
            .first()

    return metadata_id


def save_frames(video_path):
    """
    Save frames of the given video to the db and to os
    :param video_path: path to the video file we break into frames
    """
    frame_number = 0
    cap = cv2.VideoCapture(video_path)
    video_file_name = os.path.basename(video_path)
    os.makedirs(f'frames/{video_file_name}-frames', exist_ok=True)
    all_frames_dir = os.path.join(os.getcwd(), 'frames')
    video_frames_dir = os.path.join(all_frames_dir, f'{video_file_name}-frames')
    read_correctly, frame = cap.read()

    while read_correctly:
        frame_file_name = f'{frame_number}.png'
        frame_path = os.path.join(video_frames_dir, frame_file_name)
        cv2.imwrite(frame_path, frame)

        metadata_id = save_metadata(frame)
        frame_os_path = os.path.relpath(frame_path)
        video_os_path = os.path.relpath(video_path)
        video_id = DB_MANAGE.query(Video.id).filter_by(video_path=video_os_path).first()
        if not DB_MANAGE.query(Frame.id).filter_by(frame_path=frame_os_path).first():
            db_frame = Frame(video_id=video_id, metadata_id=metadata_id,
                             frame_path=frame_os_path, frame_index=frame_number)
            DB_MANAGE.save(db_frame)

        frame_number += 1
        read_correctly, frame = cap.read()

    cap.release()
    OS_MANAGE.upload_dir(video_frames_dir)
    shutil.rmtree(all_frames_dir)
    shutil.rmtree(os.path.dirname(video_path))
