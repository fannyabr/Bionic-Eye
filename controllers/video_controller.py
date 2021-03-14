import os
from flask import request, jsonify
from BionicEye.singelton_classes.db_manager import DBManage
from BionicEye.app import Video

DB_MANAGE = DBManage()


def add_video():
    """
    Gets video file in a post request and saves it to the db and the os
    """
    from BionicEye.video_manipulation_functions.video_manipulation import save_video, save_frames

    uploaded_file = request.files['file']
    os.makedirs('videos', exist_ok=True)
    videos_dir = os.path.join(os.getcwd(), 'videos')
    video_path = os.path.join(videos_dir, uploaded_file.filename)
    _, extension = os.path.splitext(video_path)

    if extension != '.mp4':
        raise Exception('File type should be mp4')

    uploaded_file.save(video_path)
    save_video(video_path)
    save_frames(video_path)


def get_video_paths():
    """
    Get all video paths from the db
    :return: json object with the list of paths
    """
    video_paths = DB_MANAGE.query(Video.video_path).all()

    return jsonify(path_list=[path for (path,) in video_paths])
