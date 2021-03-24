from flask import Response, jsonify, request
from flask import current_app as app
import os
from BionicEye.controllers.video_controller import add_video, get_video_paths, get_video_path


@app.route('/addVideo', methods=['POST'])
def run_add_video():
    uploaded_file = request.files['file']

    try:
        add_video(uploaded_file)
    except TypeError as e:
        return Response(str(e), status=422)
    else:
        return Response()


@app.route('/videoPaths', methods=['GET'])
def run_get_video_paths():
    video_paths = get_video_paths()

    return jsonify(video_paths)


@app.route('/videoPath', methods=['GET'])
def run_get_video():
    video_id = request.args.get("video_id")
    video_path = get_video_path(video_id)

    return jsonify(video_path)
