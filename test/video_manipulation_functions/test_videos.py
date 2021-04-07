from BionicEye.src.singelton_classes.db_manager import DBManager
from BionicEye.src.models import Video


def test_save_video_one_video_observation_post_name(test_client):
    from BionicEye.src.video_manipulation_functions.videos import save_video

    video_os_path = 'TelAviv_15_06_34_12_06_00/TelAviv_15_06_34_12_06_00.mp4'
    save_video('C:/Users/Fanny/Desktop/Hafifa/python/BionicEye/local_videos/TelAviv_15_06_34_12_06_00.mp4',
               video_os_path)

    db_manager = DBManager()
    video_observation_post_name = db_manager.query(Video.observation_post_name).filter_by(video_path=video_os_path)\
        .scalar()

    db_manager.delete_db()

    assert video_observation_post_name == 'TelAviv'


def test_save_video_same_videos(test_client):
    from BionicEye.src.video_manipulation_functions.videos import save_video

    video_os_path = 'TelAviv_15_06_34_12_06_00/TelAviv_15_06_34_12_06_00.mp4'
    save_video('C:/Users/Fanny/Desktop/Hafifa/python/BionicEye/local_videos/TelAviv_15_06_34_12_06_00.mp4',
               video_os_path)
    save_video('C:/Users/Fanny/Desktop/Hafifa/python/BionicEye/local_videos/TelAviv_15_06_34_12_06_00.mp4',
               video_os_path)

    db_manager = DBManager()
    videos_amount = db_manager.query(Video).filter_by(video_path=video_os_path).count()

    db_manager.delete_db()

    assert videos_amount == 1
