import os
import requests

if __name__ == '__main__':
    video_dir = os.path.join(os.getcwd(), 'local_videos')
    for file_name in os.listdir(video_dir):
        file_path = os.path.join(video_dir, file_name)
        files = {'file': open('local_videos/TelAviv_15_06_34_12_06_00.mp4', 'rb')}
        r = requests.post('http://localhost:5000/addVideo', files=files)
        print(r)
