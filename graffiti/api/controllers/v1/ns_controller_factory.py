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


from graffiti.api.controllers.v1.ns_db_controller \
    import DBNSController
from graffiti.api.controllers.v1.ns_file_controller  \
    import FileNSController
from graffiti.api.controllers.v1.ns_mem_controller \
    import MemNSController
from oslo.config import cfg


class NSControllerFactory(object):

    __controller = None
    __controller_type = cfg.CONF.DEFAULT.persistence_type

    def __init__(self, **kwargs):
        super(NSControllerFactory, self).__init__(**kwargs)

    @staticmethod
    def create(controller_type, **kwargs):
        if controller_type.lower() == 'memory':
            print "Namespace persistence = memory"
            NSControllerFactory.__controller = MemNSController(**kwargs)
            return NSControllerFactory.__controller
        elif controller_type.lower() == "db":
            print "Namespace persistence = db"
            NSControllerFactory.__controller = DBNSController(**kwargs)
            return NSControllerFactory.__controller
        elif controller_type.lower() == "file":
            print "Namespace persistence = File"
            NSControllerFactory.__controller = FileNSController(**kwargs)
            return NSControllerFactory.__controller

        return None

    @staticmethod
    def get():
        if NSControllerFactory.__controller:
            return NSControllerFactory.__controller
        else:
            return NSControllerFactory.create(
                NSControllerFactory.__controller_type)
