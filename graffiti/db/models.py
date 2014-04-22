# Copyright (c) 2014 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
SQLAlchemy Models for storing graffiti
"""

from oslo.config import cfg
import six.moves.urllib.parse as urlparse
from sqlalchemy.ext import declarative
from sqlalchemy.orm import relationship
# from sqlalchemy import schema

# from sqlalchemy import Boolean
from sqlalchemy import Column
# from sqlalchemy import DateTime
# from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Unicode
from sqlalchemy import UnicodeText

from graffiti.openstack.common.db.sqlalchemy import models

CONF = cfg.CONF


def table_args():
    engine_name = urlparse.urlparse(cfg.CONF.database_connection).scheme
    if engine_name == 'mysql':
        return {'mysql_engine': cfg.CONF.mysql_engine,
                'mysql_charset': "utf8"}
    return None


class DictionaryBase(models.ModelBase):
    metadata = None

    @declarative.declared_attr
    def __tablename__(cls):
        # NOTE(jkoelker) use the pluralized name of the class as the table
        return cls.__name__.lower() + 's'

    def as_dict(self):
        d = {}
        for c in self.__table__.columns:
            d[c.name] = self[c.name]
        return d


Base = declarative.declarative_base(cls=DictionaryBase)


class CapabilityType(Base):
    __tablename__ = 'capability_types'

    name = Column(String(255), primary_key=True)
    namespace = Column(String(255), ForeignKey('namespaces.name'))
    description = Column(String(2000))
    parent_name = Column(String(255))
    parent_namespace = Column(String(255))
    properties_text = Column(UnicodeText())


class Namespace(Base):

    name = Column(String(255), primary_key=True)
    scope = Column(Unicode(255))
    owner = Column(String(2000))
    capability_types =\
        relationship("CapabilityType",
                     primaryjoin=name == CapabilityType.namespace,
                     cascade="all, delete")
