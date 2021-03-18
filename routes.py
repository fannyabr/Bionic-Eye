from flask import Response, jsonify
from flask import current_app as app
import os
from BionicEye.controllers.video_controller import add_video, get_video_paths


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


@app.route('/framePaths', methods=['GET'])
def run_get_video_frames():
    from draft.BionicEye.controllers.frame_controller import get_video_frames

    frame_paths = get_video_frames()

    return jsonify(frame_paths)


if __name__ == '__main__':
    os.makedirs('videos', exist_ok=True)
    app.run()
