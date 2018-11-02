import datetime
import configparser
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()

from sqlalchemy import Column, BigInteger, INTEGER, TEXT, BLOB, FLOAT, DateTime, ForeignKey

class DatasetDef(Base):
    __tablename__ = 'dataset_def'

    id = Column(BigInteger, primary_key=True)
    name = Column(TEXT)
    description = Column(TEXT)
    target_column_id = Column(INTEGER)
    labels = Column(BLOB)
    train_ratio = Column(FLOAT)
    train_index = Column(BLOB)
    valid_index = Column(BLOB)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    updated = Column(DateTime, onupdate=datetime.datetime.utcnow)


class Model(Base):
    __tablename__ = 'model'

    id = Column(BigInteger, primary_key=True)
    dataset_id = Column(BigInteger, ForeignKey(DatasetDef.id, ondelete="CASCADE"))
    state = Column(INTEGER, default=0)
    algorithm = Column(INTEGER, default=0)
    algorithm_params = Column(BLOB, nullable=True)
    batch_size = Column(INTEGER)
    epoch = Column(INTEGER)
    train_loss_list = Column(BLOB, nullable=True)
    valid_loss_list = Column(BLOB, nullable=True)
    best_epoch = Column(INTEGER, nullable=True)
    best_epoch_valid_loss = Column(FLOAT, nullable=True)
    best_epoch_rmse = Column(FLOAT, nullable=True)
    best_epoch_max_abs_error = Column(FLOAT, nullable=True)
    best_epoch_r2 = Column(FLOAT, nullable=True)
    valid_predicted = Column(BLOB, nullable=True)
    valid_true = Column(BLOB, nullable=True)
    weight = Column(TEXT, nullable=True)
    deployed = Column(INTEGER, default=0)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    updated = Column(DateTime, onupdate=datetime.datetime.utcnow)



def get_engine(path):
    config = configparser.ConfigParser()
    config.read('alembic.ini')
    url = config['alembic']['sqlalchemy.url']
    engine = create_engine(url, echo=True)
    return engine

def initdb(path):
    ret = os.system("alembic upgrade head")
    if ret:
        raise RuntimeError("Failed to upgrade database")

    engine = get_engine(path)
    session_factory = sessionmaker(engine)

    global Session
    Session = scoped_session(session_factory)()

