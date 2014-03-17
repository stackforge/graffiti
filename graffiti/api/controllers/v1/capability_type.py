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

from graffiti.api.model.v1.capability_type import CapabilityType

import six

capability_types = []


class CapabilityTypeController(RestController):
    def __init__(self):
        super(RestController, self).__init__()
        self.status = 200

    @wsexpose
    def options():
        pass

    @wsexpose(CapabilityType, six.text_type)
    def get_one(self, name):
        global capability_types

        for capability_type in capability_types:
            if capability_type.name.lower() == name.lower():
                return capability_type

        res = CapabilityType(CapabilityType(), status_code=404,
                             error="CapabilityType Not Found")
        return res

    @wsexpose([CapabilityType])
    def get_all(self):
        global capability_types
        return capability_types

    @wsexpose(CapabilityType, body=CapabilityType)
    def post(self, capability_type):
        global capability_types
        capability_types.append(capability_type)
