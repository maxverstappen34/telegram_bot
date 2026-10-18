from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import sessionmaker,declarative_base

Base=declarative_base()

class CartItem(Base):
    __tablename__='cart_item'
    id=Column(Integer,primary_key=True)
    user_id=Column(Integer)
    item_name=Column(String)
    quantity=Column(Integer,default=1)

engine=create_engine('sqlite:///shop.db')
session_local=sessionmaker(bind=engine)
Base.metadata.create_all(engine)

