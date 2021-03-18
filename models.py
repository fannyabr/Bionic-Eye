from sqlalchemy import ForeignKey
from . import db


class Video(db.Model):
    __tablename__ = 'videos'

    id = db.Column(db.Integer, primary_key=True)
    observation_post_name = db.Column(db.String)
    video_path = db.Column(db.String)
    frames_amount = db.Column(db.Integer)


class Metadata(db.Model):
    __tablename__ = 'metadata'

    id = db.Column(db.Integer, primary_key=True)
    frame_tag = db.Column(db.Boolean)
    camera_fov = db.Column(db.Float)
    azimuth = db.Column(db.Float)
    elevation = db.Column(db.Float)


class Frame(db.Model):
    __tablename__ = 'frames'

    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, ForeignKey('videos.id'))
    metadata_id = db.Column(db.Integer, ForeignKey('metadata.id'))
    frame_path = db.Column(db.String)
    frame_index = db.Column(db.Integer)
