from BionicEye.src.singelton_classes.db_manager import DBManager
from BionicEye.src.models import Video


def test_get_video_paths_one_video(test_client):
    from BionicEye.src.controllers.video_controller import get_video_paths

    video = Video(observation_post_name='Jerusalem', video_path='testVideo/Jerusalem', frames_amount=47)
    db_manager = DBManager()
    db_manager.save(video)
    paths = get_video_paths()

    db_manager.delete_db()

    assert len(paths) == 1


def test_get_video_paths_few_videos(test_client):
    from BionicEye.src.controllers.video_controller import get_video_paths

    video1 = Video(observation_post_name='Jerusalem', video_path='testVideo/Jerusalem', frames_amount=47)
    video2 = Video(observation_post_name='Eilat', video_path='testVideo/Eilat', frames_amount=59)
    video3 = Video(observation_post_name='Jerusalem', video_path='testVideo/Jerusalem2', frames_amount=101)
    db_manager = DBManager()

    db_manager.save(video1)
    db_manager.save(video2)
    db_manager.save(video3)

    paths = get_video_paths()

    db_manager.delete_db()

    assert len(paths) == 3


def test_get_video_paths_no_video(test_client):
    from BionicEye.src.controllers.video_controller import get_video_paths
    paths = get_video_paths()

    assert len(paths) == 0


def test_get_video_path_id_doesnt_exist(test_client):
    from BionicEye.src.controllers.video_controller import get_video_path
    video_path = get_video_path(5)

    assert video_path is None


def test_get_video_path_invalid_id(test_client):
    from BionicEye.src.controllers.video_controller import get_video_path

    try:
        get_video_path('a')
    except TypeError:
        assert True
    else:
        assert False


def test_get_video_path_valid_id(test_client):
    from BionicEye.src.controllers.video_controller import get_video_path

    video = Video(observation_post_name='Jerusalem', video_path='testVideo/Jerusalem2', frames_amount=101)
    db_manager = DBManager()

    db_manager.save(video)

    video_path = get_video_path(1)[0]

    db_manager.delete_db()

    assert video_path == 'testVideo/Jerusalem2'
