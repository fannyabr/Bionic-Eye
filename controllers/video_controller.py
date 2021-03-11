from BionicEye.video_manipulation import *
from BionicEye.app import Video
import os
from flask import request, jsonify


VIDEOS_DIR = os.path.join(os.getcwd(), 'videos')


def add_video():
    uploaded_file = request.files['file']
    videos_dir = os.path.join(os.getcwd(), 'videos')
    video_path = os.path.join(videos_dir, uploaded_file.filename)

    uploaded_file.save(video_path)

    save_video(video_path)
    save_frames(video_path)


def get_video_paths():
    video_paths = DB_MANAGE.query(Video.video_path).all()
    return jsonify(path_list=[path for (path,) in video_paths])