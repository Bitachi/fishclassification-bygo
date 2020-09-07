from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

#DBファイル名と保存先を指定する（同一ディレクトリにdata.dbファイルを作成する）
database_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data.db')
#SQlineを指定
engine = create_engine('sqlite:///' + database_file, convert_unicode=True, echo=True)
db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)
Base = declarative_base()
Base.query = db_session.query_property()

#DBテーブルを作成
def init_db():
    import flaski.dbmodels
    Base.metadata.create_all(bind=engine)