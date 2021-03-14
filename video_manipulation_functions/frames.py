import cv2
import shutil
import os
from BionicEye.singelton_classes.db_manager import DBManager
from BionicEye.singelton_classes.os_manager import OSManager
from BionicEye.models import Frame, Video
from BionicEye.video_manipulation_functions.metadata import save_metadata

DB_MANAGER = DBManager()
OS_MANAGER = OSManager()
ALL_FRAMES_DIR = os.path.join(os.getcwd(), 'frames')


def count_frames(video_path):
    """
    Counts frames in a video
    :param video_path: path to a video file
    :return: the amount of frames in the video
    """
    frame_number = 0
    cap = cv2.VideoCapture(video_path)

    try:
        frame_number = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    except:
        read_correctly, frame = cap.read()

        while read_correctly:
            frame_number += 1
            read_correctly, frame = cap.read()

    return frame_number


def save_frames(video_path):
    """
    Save frames of the given video to the db and to os
    :param video_path: path to the video file we break into frames
    """
    frame_number = 0
    cap = cv2.VideoCapture(video_path)
    video_file_name = os.path.basename(video_path)
    os.makedirs(f'frames/{video_file_name}-frames', exist_ok=True)
    video_frames_dir = os.path.join(ALL_FRAMES_DIR, f'{video_file_name}-frames')
    read_correctly, frame = cap.read()

    while read_correctly:
        frame_file_name = f'{frame_number}.png'
        frame_path = os.path.join(video_frames_dir, frame_file_name)
        cv2.imwrite(frame_path, frame)

        metadata_id = save_metadata(frame)
        frame_os_path = os.path.relpath(frame_path)
        video_os_path = os.path.relpath(video_path)
        video_id = DB_MANAGER.query(Video.id).filter_by(video_path=video_os_path).one()
        if not DB_MANAGER.query(Frame.id).filter_by(frame_path=frame_os_path).one_or_none():
            db_frame = Frame(video_id=video_id, metadata_id=metadata_id,
                             frame_path=frame_os_path, frame_index=frame_number)
            DB_MANAGER.save(db_frame)

        frame_number += 1
        read_correctly, frame = cap.read()

    cap.release()
    OS_MANAGER.upload_dir(video_frames_dir)
    shutil.rmtree(ALL_FRAMES_DIR)
    shutil.rmtree(os.path.dirname(video_path))
