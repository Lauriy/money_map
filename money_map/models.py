from datetime import datetime

from pyramid.security import Allow, Everyone
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(
    sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class AuditMixin(object):
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class BankAccountStatement(Base, AuditMixin):
    __tablename__ = 'bank_account_statement'

    id = Column(Integer, primary_key=True)
    file = Column(String, nullable=False)
    # uid = Column(Integer, primary_key=True)
    # title = Column(Text, unique=True)
    # body = Column(Text)


class Root(object):
    __acl__ = [(Allow, Everyone, 'view'),
               (Allow, 'group:editors', 'edit')]

    def __init__(self, request):
        pass
