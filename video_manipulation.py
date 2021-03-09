from BionicEye.models import Video, Frame, Metadata, db
from BionicEye.given_functions import generate_metadata, is_frame_tagged
from BionicEye.blob_storage import BlobFileUploader
import cv2
import os


def save_video_to_db(video_path):
    """
    Saves given video information to the data base
    :param video_path: path to the video file we want to save to the db
    """
    video_file_name = video_path.split('\\', -1)[-1]
    observation_post_name = video_file_name.split('_')[0]
    captured_video = cv2.VideoCapture(video_path)
    frames_amount = int(captured_video.get(cv2.CAP_PROP_FRAME_COUNT))
    video = Video(observation_post_name=observation_post_name, video_path=video_file_name, frames_amount=frames_amount)

    db.session.add(video)
    db.session.commit()


def save_frames(video_path):
    """
    Save frames of the given video to the db and to os. Also, saves the metadata of the frame to the db if not exists.
    :param video_path:
    :return:
    """
    frame_number = 0
    captured_video = cv2.VideoCapture(video_path)
    video_name = video_path.split('\\')[-1]
    os.makedirs('frames', exist_ok=True)
    all_frames_dir = os.path.join(os.getcwd(), 'frames')
    video_frames_dir = os.path.join(all_frames_dir, f'{video_name}-frames')

    os.makedirs(video_frames_dir, exist_ok=True)

    while captured_video.isOpened():

        # Save frames locally
        read_correctly, frame = captured_video.read()
        if not read_correctly:
            break
        frame_file_name = f'{frame_number}.jpg'
        frame_path = os.path.join(video_frames_dir, frame_file_name)
        cv2.imwrite(frame_path, frame)

        # Save frames metadata to db if not exists
        fov, azimuth, elevation = generate_metadata(frame)
        frame_tag = is_frame_tagged(frame)
        metadata_id = db.session.query(Metadata.id)\
            .filter_by(frame_tag=frame_tag, camera_fov=fov, azimuth=azimuth, elevation=elevation)\
            .first()

        if not metadata_id:
            metadata = Metadata(frame_tag=is_frame_tagged(frame), camera_fov=fov, azimuth=azimuth, elevation=elevation)
            db.session.add(metadata)
            db.session.commit()
            metadata_id = db.session.query(Metadata.id) \
                .filter_by(frame_tag=is_frame_tagged(frame), camera_fov=fov, azimuth=azimuth, elevation=elevation) \
                .first()

        # Save frame to db
        frame_os_path = f'{video_name}/{frame_file_name}'
        video_os_path = video_path.split('\\')[-1]
        video_id = db.session.query(Video.id).filter_by(video_path=video_os_path).first()
        db_frame = Frame(video_id=video_id, metadata_id=metadata_id, frame_path=frame_os_path, frame_index=frame_number)
        db.session.add(db_frame)
        db.session.commit()

        frame_number += 1

    captured_video.release()

    # Save all the frames in the folder to the blob storage ad delete locally
    container_name = 'frames'
    blob_frames_uploader = BlobFileUploader(container_name, video_frames_dir)
    blob_frames_uploader.upload_all_files()
