from flask import Response, jsonify, request
from flask import current_app as app
from BionicEye.controllers.video_controller import add_video, get_video_paths
from BionicEye.controllers.frame_controller import get_frame


@app.route('/addVideo', methods=['POST'])
def run_add_video():
    uploaded_file = request.files['file']

    try:
        add_video(uploaded_file)
    except TypeError:
        return Response("The file must be a video", status=422)


@app.route('/videoPaths', methods=['GET'])
def run_get_video_paths():
    video_paths = get_video_paths()

    return jsonify(video_paths)


@app.route('/frame', methods=['GET'])
def run_get_frame():
    video_id = request.args.get("video_id")
    frame_index = request.args.get("frame_index")
    frame_path = get_frame(video_id, frame_index)

    return jsonify(frame_path)
