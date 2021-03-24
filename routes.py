from flask import Response, jsonify, request
from flask import current_app as app
from azure.core.exceptions import ResourceNotFoundError
from BionicEye.controllers.video_controller import add_video, get_video_paths, download_video


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


@app.route('/downloadVideo', methods=['GET'])
def run_download_video():
    os_path = request.args.get("os_path")

    try:
        download_video(os_path)
    except ResourceNotFoundError as e:
        return Response(str(e), status=422)
    else:
        return Response()
