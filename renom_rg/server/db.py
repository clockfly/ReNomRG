import pickle
import datetime
import configparser
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm import relationship

Base = declarative_base()

from sqlalchemy import Column, BigInteger, Integer, TEXT, BLOB, FLOAT, DateTime, ForeignKey

NONE_PICLKLES = pickle.dumps(None)

class DatasetDef(Base):
    __tablename__ = 'dataset_def'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(TEXT)
    description = Column(TEXT)
    target_column_id = Column(Integer)
    target_column_ids = Column(BLOB)
    labels = Column(BLOB)
    train_ratio = Column(FLOAT)
    train_index = Column(BLOB)
    valid_index = Column(BLOB)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    updated = Column(DateTime, default=datetime.datetime.utcnow,
                     onupdate=datetime.datetime.utcnow)


class Model(Base):
    __tablename__ = 'model'

    id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer, ForeignKey(DatasetDef.id, ondelete="CASCADE"))
    state = Column(Integer, default=0)
    algorithm = Column(Integer, default=0)
    algorithm_params = Column(BLOB, default=NONE_PICLKLES)
    batch_size = Column(Integer)
    epoch = Column(Integer)
    train_loss_list = Column(BLOB, default=NONE_PICLKLES)
    valid_loss_list = Column(BLOB, default=NONE_PICLKLES)
    best_epoch = Column(Integer, nullable=True)
    best_epoch_valid_loss = Column(FLOAT, nullable=True)
    best_epoch_rmse = Column(FLOAT, nullable=True)
    best_epoch_max_abs_error = Column(FLOAT, nullable=True)
    best_epoch_r2 = Column(FLOAT, nullable=True)
    valid_predicted = Column(BLOB, default=NONE_PICLKLES)
    valid_true = Column(BLOB, default=NONE_PICLKLES)
    sampled_train_pred = Column(BLOB, default=NONE_PICLKLES)
    sampled_train_true = Column(BLOB, default=NONE_PICLKLES)
    confidence_data = Column(BLOB, default=NONE_PICLKLES)
    weight = Column(TEXT, nullable=True)
    deployed = Column(Integer, default=0)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    updated = Column(DateTime, default=datetime.datetime.utcnow,
                     onupdate=datetime.datetime.utcnow)

    dataset = relationship('DatasetDef')

def get_engine():
    config = configparser.ConfigParser()
    config.read('alembic.ini')
    url = config['alembic']['sqlalchemy.url']
    engine = create_engine(url, echo=False)
    return engine

def initsession(engine):
    global _session
    _session = scoped_session(sessionmaker(bind=engine))

def session():
    return _session

def initdb():
    ret = os.system("alembic upgrade head")
    if ret:
        raise RuntimeError("Failed to upgrade database")

    engine = get_engine()
    initsession(engine)
