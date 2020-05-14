import base64
import json
import collections
import io
from PIL import Image
import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy import Table, Column, Integer, String, LargeBinary, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


def base64_str_to_bytearray(data) -> bytearray:
    decoded_data = base64.b64decode(data)
    data_as_str_list = str(decoded_data).split("\'")[1].split(",")
    data_as_int_list = [int(x) for x in data_as_str_list]
    return bytearray(data_as_int_list)


class SQL_driver:
    engine = create_engine('sqlite:///db/pampuch.db')
    metadata = MetaData(engine)
    images = None

    def create_tables(self):
        self.images = Table('images', self.metadata,
                            Column('id', Integer, primary_key=True),
                            Column('label', String),
                            Column('img', LargeBinary))
        try:
            self.images.create()
        except sqlalchemy.exc.OperationalError as e:
            pass

    def insert_image(self, image_bytes, image_label):
        # self.create_session()
        insert = self.images.insert()
        insert.execute(img=image_bytes, label=image_label)

    def select_images(self, img_id=-1, img_label=''):
        select = None
        if img_id == -1 and img_label == '':
            select = self.images.select()
        elif img_label == '':
            select = self.images.select().where(self.images.columns.id == img_id)
        elif img_id == -1:
            select = self.images.select().where(self.images.columns.label == img_label)

        if select is None:
            return

        results = select.execute()
        results = results.fetchall()
        objects_list = []
        for row in results:
            element = collections.OrderedDict()
            element['id'] = row['id']
            element['label'] = row['label']

            buffered = io.BytesIO(row['img'])
            img = Image.open(buffered)
            img.save(buffered, format="PNG")
            element['base64'] = "".join(chr(x) for x in bytearray(
                base64.b64encode(buffered.getvalue())))
            objects_list.append(element)
        return json.dumps(objects_list, indent=4)

    def select_labels(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        results = session.query(Images.label, func.count(
            Images.id)).group_by(Images.label).all()

        objects_list = []
        for row in results:
            element = collections.OrderedDict()
            element['label'] = row[0]
            element['count'] = row[1]
            objects_list.append(element)
        return json.dumps(objects_list, indent=4)


class Images(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    label = Column(String)
    img = Column(LargeBinary)

    def __init__(self, id, label, img):
        self.id = id
        self.label = label
        self.img = img
