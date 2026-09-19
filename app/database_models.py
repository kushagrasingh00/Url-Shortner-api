from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer , String , text , ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP

Base=declarative_base()


class user_schema(Base):
    __tablename__ = 'users'

    user_id= Column(Integer ,primary_key=True,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    email= Column(String,nullable=False)
    password=Column(String,nullable=False)



class link_schema(Base):
    __tablename__ = 'Links'

    id = Column(Integer,nullable= False , primary_key=True)
    original_url = Column(String,nullable=False)
    short_code= Column(String,nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id",ondelete="CASCADE"),nullable=False)
    clicks= Column(Integer,server_default=text('0'))
    created_at= Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

    user = relationship("user_schema" , passive_deletes=True)
    