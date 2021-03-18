from flask import Response, jsonify
from flask import current_app as app
import os
from BionicEye.controllers.video_controller import add_video, get_video_paths, get_video_path


@app.route('/addVideo', methods=['POST'])
def run_add_video():
    try:
        add_video()
    except:
        Response().set_data("Couldn't save video")

    return Response()


@app.route('/videoPaths', methods=['GET'])
def run_get_video_paths():
    video_paths = get_video_paths()

    return jsonify(video_paths)


@app.route('/videoPath', methods=['GET'])
def run_get_video():
    video_path = get_video_path()

    return jsonify(video_path)


if __name__ == '__main__':
    os.makedirs('videos', exist_ok=True)
    app.run()
