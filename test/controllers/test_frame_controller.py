from BionicEye.src.singelton_classes.db_manager import DBManager
from BionicEye.src.models import Frame, Video, Metadata


def test_get_video_frames_id_doesnt_exist(test_client):
    from BionicEye.src.controllers.frame_controller import get_video_frames
    frames = get_video_frames(5)

    assert len(frames) == 0


def test_get_video_frames_invalid_id(test_client):
    from BionicEye.src.controllers.frame_controller import get_video_frames

    try:
        get_video_frames('a')
    except TypeError:
        assert True
    else:
        assert False


def test_get_video_frames_valid_id(test_client):
    from BionicEye.src.controllers.frame_controller import get_video_frames

    db_manager = DBManager()
    video1 = Video(observation_post_name='Jerusalem', video_path='testVideo/Jerusalem', frames_amount=47)
    video2 = Video(observation_post_name='Eilat', video_path='testVideo/Eilat', frames_amount=53)

    db_manager.save(video1)
    db_manager.save(video2)

    metadata = Metadata(frame_tag=False, camera_fov=2.2, azimuth=1.1, elevation=0.6)

    db_manager.save(metadata)

    frame1 = Frame(video_id=1, metadata_id=1, frame_path='abc/5.png', frame_index=5)
    frame2 = Frame(video_id=1, metadata_id=1, frame_path='abc/7.png', frame_index=7)
    frame3 = Frame(video_id=2, metadata_id=1, frame_path='def/5.png', frame_index=5)

    db_manager.save(frame1)
    db_manager.save(frame2)
    db_manager.save(frame3)

    frames = get_video_frames(1)

    db_manager.delete_db()

    assert len(frames) == 2


def test_get_frame_id_doesnt_exist(test_client):
    from BionicEye.src.controllers.frame_controller import get_frame

    db_manager = DBManager()
    video = Video(observation_post_name='Jerusalem', video_path='testVideo/Jerusalem', frames_amount=47)
    metadata = Metadata(frame_tag=False, camera_fov=2.2, azimuth=1.1, elevation=0.6)
    frame = Frame(video_id=1, metadata_id=1, frame_path='def/5.png', frame_index=5)

    db_manager.save(video)
    db_manager.save(metadata)
    db_manager.save(frame)

    frame_path = get_frame(9, 5)

    db_manager.delete_db()

    assert frame_path is None


def test_get_frame_index_doesnt_exist(test_client):
    from BionicEye.src.controllers.frame_controller import get_frame

    db_manager = DBManager()
    video = Video(observation_post_name='Jerusalem', video_path='testVideo/Jerusalem', frames_amount=47)
    metadata = Metadata(frame_tag=False, camera_fov=2.2, azimuth=1.1, elevation=0.6)
    frame = Frame(video_id=1, metadata_id=1, frame_path='def/5.png', frame_index=5)

    db_manager.save(video)
    db_manager.save(metadata)
    db_manager.save(frame)

    frame_path = get_frame(1, 8)

    db_manager.delete_db()

    assert frame_path is None


def test_get_frame_invalid_id(test_client):
    from BionicEye.src.controllers.frame_controller import get_frame

    try:
        get_frame('a', 6)
    except TypeError:
        assert True
    else:
        assert False


def test_get_frame_invalid_index(test_client):
    from BionicEye.src.controllers.frame_controller import get_frame

    db_manager = DBManager()
    video = Video(observation_post_name='Jerusalem', video_path='testVideo/Jerusalem', frames_amount=47)
    metadata = Metadata(frame_tag=False, camera_fov=2.2, azimuth=1.1, elevation=0.6)
    frame = Frame(video_id=1, metadata_id=1, frame_path='def/5.png', frame_index=5)

    db_manager.save(video)
    db_manager.save(metadata)
    db_manager.save(frame)

    try:
        get_frame(1, 't')
    except TypeError:
        assert True
    else:
        assert False
    finally:
        db_manager.delete_db()


def test_get_frame_valid(test_client):
    from BionicEye.src.controllers.frame_controller import get_frame

    db_manager = DBManager()
    video = Video(observation_post_name='Jerusalem', video_path='testVideo/Jerusalem', frames_amount=47)
    metadata = Metadata(frame_tag=False, camera_fov=2.2, azimuth=1.1, elevation=0.6)
    frame = Frame(video_id=1, metadata_id=1, frame_path='def/5.png', frame_index=5)

    db_manager.save(video)
    db_manager.save(metadata)
    db_manager.save(frame)

    frame_path = get_frame(1, 5)[0]

    db_manager.delete_db()

    assert frame_path == 'def/5.png'
