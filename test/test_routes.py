def test_run_add_video_text_file_error(test_client):
    files = {'file': open('a.txt', 'rb')}
    res = test_client.post('http://localhost:5000/addVideo', data=files)

    assert res.status_code == 422


def test_run_add_video_not_file_error(test_client):
    res = test_client.post('http://localhost:5000/addVideo', data={"file": "k"})

    assert res.status_code == 400


def test_run_add_video_video_file_success(test_client):
    files = {'file': open('C:/Users/Fanny/Desktop/Hafifa/python/BionicEye/local_videos/TelAviv_15_06_34_12_06_00'
                          '.mp4', 'rb')}
    res = test_client.post('http://localhost:5000/addVideo', data=files)

    assert res.status_code == 200
