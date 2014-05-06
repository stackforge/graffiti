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

from pecan.rest import RestController

from wsmeext.pecan import wsexpose

from graffiti.api.model.v1.capability_type_derived_prop import \
    CapabilityTypeDerivedProperties
from graffiti.api.model.v1.dao.captype_dao_factory \
    import CapabilityTypeDAOFactory
from oslo.config import cfg


import six


class CapabilityTypeDerivedController(RestController):

    def __init__(self):
        super(RestController, self).__init__()
        self.status = 200
        self._cap_controller = None
        self._load_controller()

    def _load_controller(self):
        dao_type = cfg.CONF.DEFAULT.persistence_type
        self._cap_controller = CapabilityTypeDAOFactory.create(dao_type)

    @wsexpose
    def options():
        pass

    @wsexpose(CapabilityTypeDerivedProperties, six.text_type, six.text_type)
    def get_one(self, name, namespace):
        captype = self._cap_controller.\
            get_capability_type_with_derived_properties(name, namespace)
        return captype
