import  os
from sqlalchemy import ForeignKey, String, create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

    
if os.path.exists('test.db'):
    os.remove('test.db')
base = create_engine('sqlite:///test.db') 

# Base class 
DatabaseModel = declarative_base()

class Switch(DatabaseModel):
    __tablename__ = 'switch'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    vendor: Mapped[str] = mapped_column(String(100),  default='')
    keyboards: Mapped["Keyboard"] = relationship(back_populates="switches")


class Keyboard(DatabaseModel):
    __tablename__ = 'keyboard'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    switch_id: Mapped[int] = mapped_column(ForeignKey("switch.id"))
    switches: Mapped["Switch"] = relationship(back_populates="keyboards")

 
# Create tables
DatabaseModel.metadata.create_all(base)
# Create session with objects
Session = sessionmaker(bind=base)
db = Session()

# add two clasess if table is empty
if not db.query(Switch).count():
    db.add(Switch(name='black', vendor='EvilCorp'))
    db.add(Switch(name='red', vendor='NoNameCorp'))

# create class instance
switch = db.query(Switch).filter_by(name = 'black').one()

# add many rows
db.add_all([
    Keyboard(name='Moonlander',switch_id=switch.id),
    Keyboard(name='ErgoDox',switch_id=switch.id),
])

def read_data():
    for keyboard in db.query(Keyboard).join(Switch).all():
        print (keyboard.id, keyboard.name, keyboard.switches.name, keyboard.switches.vendor)
    print ("")

read_data()
# write data to db and close
db.commit()
db.close()
