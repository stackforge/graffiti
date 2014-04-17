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

from captype_controller import CapabilityTypeControllerBase


class MemCapabilityTypeController(CapabilityTypeControllerBase):

    def __init__(self, **kwargs):
        super(MemCapabilityTypeController, self).__init__(**kwargs)
        self._type = 'MemCapabilityTypeController'
        self._capability_types = {}

    def get_capability_type(self, name, namespace):
        id = namespace + ":" + name
        return self._capability_types[id]

    def find_capability_types(self, query_string):
        return self._capability_types.itervalues()

    def set_capability_type(self, capability_type):
        id = capability_type.namespace + ":" + capability_type.name
        self._capability_types[id] = capability_type

        return capability_type

    def put_capability_type(self, name, namespace, capability_type):
        id = namespace + ":" + name
        self._capability_types[id] = capability_type

        return capability_type

    def delete_capability_type(self, name, namespace):
        id = namespace + ":" + name
        capability_type = None
        if self._capability_types[id]:
            capability_type = self._capability_types[id]
            self._capability_types.pop(id)

        return capability_type
