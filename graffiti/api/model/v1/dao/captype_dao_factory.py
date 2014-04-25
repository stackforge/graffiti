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

from graffiti.api.model.v1.dao.captype_db_dao \
    import DBCapabilityTypeDAO
from graffiti.api.model.v1.dao.captype_file_dao \
    import FileCapabilityTypeDAO
from graffiti.api.model.v1.dao.captype_mem_dao \
    import MemCapabilityTypeDAO


class CapabilityTypeDAOFactory(object):

    def __init__(self, **kwargs):
        super(CapabilityTypeDAOFactory, self).__init__(**kwargs)

    @staticmethod
    def create(dao_type, **kwargs):
        if dao_type.lower() == 'memory':
            print "Dictionary persistence = memory"
            return MemCapabilityTypeDAO(**kwargs)
        elif dao_type.lower() == "db":
            print "Dictionary persistence = db"
            return DBCapabilityTypeDAO(**kwargs)
        elif dao_type.lower() == "file":
            print "Dictionary persistence = File"
            return FileCapabilityTypeDAO(**kwargs)

        return None
