# Copyright (c) 2014 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from graffiti.api.model.v1.dao.ns_db_dao \
    import DBNSDAO
from graffiti.api.model.v1.dao.ns_file_dao \
    import FileNSDAO
from graffiti.api.model.v1.dao.ns_mem_dao \
    import MemNSDAO
from oslo.config import cfg


class NSDAOFactory(object):

    __dao = None
    __dao_type = cfg.CONF.DEFAULT.persistence_type

    def __init__(self, **kwargs):
        super(NSDAOFactory, self).__init__(**kwargs)

    @staticmethod
    def create(dao_type, **kwargs):
        if dao_type.lower() == 'memory':
            print "Namespace persistence = memory"
            NSDAOFactory.__dao = MemNSDAO(**kwargs)
            return NSDAOFactory.__dao
        elif dao_type.lower() == "db":
            print "Namespace persistence = db"
            NSDAOFactory.__dao = DBNSDAO(**kwargs)
            return NSDAOFactory.__dao
        elif dao_type.lower() == "file":
            print "Namespace persistence = File"
            NSDAOFactory.__dao = FileNSDAO(**kwargs)
            return NSDAOFactory.__dao

        return None

    @staticmethod
    def get():
        if NSDAOFactory.__dao:
            return NSDAOFactory.__dao
        else:
            return NSDAOFactory.create(
                NSDAOFactory.__dao_type)
