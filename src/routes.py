from flask import Response, jsonify, request
from flask import current_app as app
from azure.core.exceptions import ResourceNotFoundError
from BionicEye.src.controllers.video_controller import add_video, get_video_paths, get_video_path, download_video
from BionicEye.src.controllers.frame_controller import get_video_frames, get_frame, download_tagged_frames


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

    try:
        video_path = get_video_path(video_id)
    except TypeError as e:
        return Response(str(e), status=400)

    return jsonify(video_path)


@app.route('/framePaths', methods=['GET'])
def run_get_video_frames():
    video_id = request.args.get("video_id")
    frame_paths = get_video_frames(video_id)

    return jsonify(frame_paths)


@app.route('/frame', methods=['GET'])
def run_get_frame():
    video_id = request.args.get("video_id")
    frame_index = request.args.get("frame_index")
    frame_path = get_frame(video_id, frame_index)

    return jsonify(frame_path)


@app.route('/downloadVideo', methods=['GET'])
def run_download_video():
    os_path = request.args.get("os_path")

    try:
        download_video(os_path)
    except ResourceNotFoundError as e:
        return Response(str(e), status=422)
    else:
        return Response()


@app.route('/downloadTaggedFrames', methods=['GET'])
def run_download_tagged_frames():
    video_id = request.args.get("video_id")

    try:
        download_tagged_frames(video_id)
    except ResourceNotFoundError as e:
        return Response(str(e), status=422)
    else:
        return Response()
