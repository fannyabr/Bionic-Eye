def test_add_video(test_client):
    files = {'file': open('a.txt', 'rb')}
    res = test_client.post('http://localhost:5000/addVideo', data=files)

    assert res.status_code == 422
