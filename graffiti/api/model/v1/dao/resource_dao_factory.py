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

from graffiti.api.model.v1.dao.resource_db_dao import DBResourceDAO
from graffiti.api.model.v1.dao.resource_file_dao import FileResourceDAO
from graffiti.api.model.v1.dao.resource_mem_dao import MemResourceDAO


class ResourceDAOFactory(object):

    def __init__(self, **kwargs):
        super(ResourceDAOFactory, self).__init__(**kwargs)

    @staticmethod
    def create(dao_type, **kwargs):
        if dao_type.lower() == 'memory':
            print "Directory persistence = memory"
            return MemResourceDAO(**kwargs)
        elif dao_type.lower() == 'file':
            print "Directory persistence = file"
            return FileResourceDAO(**kwargs)
        elif dao_type.lower() == 'db':
            print "Directory persistence = db"
            return DBResourceDAO(**kwargs)

        return None
