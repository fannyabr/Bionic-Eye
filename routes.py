from flask import Response, jsonify
from flask import current_app as app
import os
from BionicEye.controllers.video_controller import add_video, get_video_paths


@app.route('/addVideo', methods=['POST'])
def run_add_video():
    try:
        add_video()
    except TypeError:
        return Response("The file must be a video", status=422)


@app.route('/videoPaths', methods=['GET'])
def run_get_video_paths():
    video_paths = get_video_paths()

    return jsonify(video_paths)


@app.route('/frame', methods=['GET'])
def run_get_frame():
    from draft.BionicEye.controllers.frame_controller import get_frame

    frame_path = get_frame()

    return jsonify(frame_path)


if __name__ == '__main__':
    os.makedirs('videos', exist_ok=True)
    app.run()
