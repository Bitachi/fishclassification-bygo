from sqlalchemy import Column, Integer, String, Boolean
from flaski.database import Base

#テーブル情報　魚
class FishMaster(Base):
    #テーブル名の設定
    __tablename__ = "fish_master"
    #列の設定
    fish_name = Column(String, primary_key=True)
    poison = Column(Integer)
    poison_part = Column(String)
    wiki_url = Column(String)
    picture_path = Column(String)
    copyright_owner = Column(String)
    copyright_url = Column(String)

    def __init__(self, fish_name=None, poison=None, poison_part=None, wiki_url=None, picture_path=None, copyright_owner=None, copyright_url=None):
        self.fish_name = fish_name
        self.poison = poison
        self.poison_part = poison_part
        self.wiki_url = wiki_url
        self.picture_path = picture_path
        self.picture_path = picture_path
        self.copyright_owner = copyright_owner
        self.copyright_url = copyright_url