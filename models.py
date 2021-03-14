from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey
from BionicEye.app import db


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
