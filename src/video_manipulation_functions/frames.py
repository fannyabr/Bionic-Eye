import cv2
import shutil
import os
from BionicEye.src.singelton_classes.db_manager import DBManager
from BionicEye.src.singelton_classes.os_manager import OSManager
from BionicEye.src.models import Frame, Video
from BionicEye.src.video_manipulation_functions.metadata import save_metadata

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

    if not cap.isOpened():
        raise Exception("Can't open video")

    try:
        frame_number = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    except Exception as e:
        print(e)
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

    if not cap.isOpened():
        raise Exception("Can't open video")

    file_name = os.path.basename(video_path)
    video_name, _ = os.path.splitext(file_name)
    video_os_path = os.path.join(video_name, file_name)
    video_id = DB_MANAGER.query(Video.id).filter_by(video_path=video_os_path).one()
    video_dir = os.path.dirname(video_path)
    frames_dir = os.path.join(video_dir, 'frames')

    os.makedirs(frames_dir, exist_ok=True)

    read_correctly, frame = cap.read()

    while read_correctly:
        frame_file_name = f'{frame_number}.png'
        frame_path = os.path.join(frames_dir, frame_file_name)
        cv2.imwrite(frame_path, frame)

        metadata_id = save_metadata(frame)
        frame_os_path = os.path.relpath(frame_path)

        if not DB_MANAGER.query(Frame.id).filter_by(frame_path=frame_os_path).one_or_none():
            db_frame = Frame(video_id=video_id, metadata_id=metadata_id,
                             frame_path=frame_os_path, frame_index=frame_number)
            DB_MANAGER.save(db_frame)

        frame_number += 1
        read_correctly, frame = cap.read()

    cap.release()
    OS_MANAGER.upload_dir(frames_dir, frames_dir)
    shutil.rmtree(video_dir)
