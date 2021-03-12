from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, Response
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Video(db.Model):
    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True)
    observation_post_name = Column(String)
    video_path = Column(String)
    frames_amount = Column(Integer)


class Metadata(db.Model):
    __tablename__ = 'metadata'

    id = Column(Integer, primary_key=True)
    frame_tag = Column(Boolean)
    camera_fov = Column(Float)
    azimuth = Column(Float)
    elevation = Column(Float)


class Frame(db.Model):
    __tablename__ = 'frames'

    id = Column(Integer, primary_key=True)
    video_id = Column(Integer, ForeignKey('videos.id'))
    metadata_id = Column(Integer, ForeignKey('metadata.id'))
    frame_path = Column(String)
    frame_index = Column(Integer)


@app.route('/addVideo', methods=['POST'])
def run_add_video():
    from BionicEye.video_manipulation import add_video
    add_video()

    return Response()


@app.route('/videoPaths', methods=['GET'])
def run_get_video_paths():
    from BionicEye.video_manipulation import get_video_paths
    return get_video_paths()


if __name__ == '__main__':
    app.run()
