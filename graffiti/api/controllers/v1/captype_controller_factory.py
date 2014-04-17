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


from graffiti.api.controllers.v1.captype_db_controller \
    import DBCapabilityTypeController
from graffiti.api.controllers.v1.captype_file_controller \
    import FileCapabilityTypeController
from graffiti.api.controllers.v1.captype_mem_controller \
    import MemCapabilityTypeController


class CapTypeControllerFactory(object):

    def __init__(self, **kwargs):
        super(CapTypeControllerFactory, self).__init__(**kwargs)

    @staticmethod
    def create(controller_type, **kwargs):
        if controller_type.lower() == 'memory':
            print "Dictionary persistence = memory"
            return MemCapabilityTypeController(**kwargs)
        elif controller_type.lower() == "db":
            print "Dictionary persistence = db"
            return DBCapabilityTypeController(**kwargs)
        elif controller_type.lower() == "file":
            print "Dictionary persistence = File"
            return FileCapabilityTypeController(**kwargs)

        return None
