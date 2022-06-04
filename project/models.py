# coding: utf-8
from sqlalchemy import BigInteger, Column, ForeignKey, Integer, LargeBinary, MetaData, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata



class Agent(Base):
    __tablename__ = 'agents'

    a_id = Column(Integer, primary_key=True)
    phoneno = Column(Integer, nullable=False)
    branch_id = Column(ForeignKey('company.id'), nullable=False)
    name = Column(String(23), nullable=False)
    _pass = Column('pass', String(23), nullable=False)

    branch = relationship('Company', primaryjoin='Agent.branch_id == Company.id', backref='agents')



class Car(Base):
    __tablename__ = 'cars'

    manufacturer = Column(String(23), nullable=False)
    price = Column(Integer, nullable=False)
    car_id = Column(Integer, primary_key=True)
    model = Column(String(23), nullable=False)
    branch_id = Column(ForeignKey('company.id', ondelete='CASCADE', onupdate='CASCADE'))
    img = Column(String(1000))
    branch = relationship('Company', primaryjoin='Car.branch_id == Company.id', backref='cars')



class Company(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True)



class Customer(Base):
    __tablename__ = 'customer'

    cname = Column(String(23), nullable=False)
    cnic = Column(BigInteger, primary_key=True)
    address = Column(String(100), nullable=False)
    passwords = Column(String(20), nullable=False)
    agent_id = Column(ForeignKey('agents.a_id'), nullable=False)
    phone = Column(BigInteger, nullable=False)
    email = Column(String(23), nullable=False)
    c_id = Column(Integer)

    agent = relationship('Agent', primaryjoin='Customer.agent_id == Agent.a_id', backref='customers')




