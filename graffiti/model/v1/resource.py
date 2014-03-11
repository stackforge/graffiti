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

import wsme
from wsme import types

from graffiti.model.v1.capability import Capability
from graffiti.model.v1.property import Property
from graffiti.model.v1.provider import Provider
from graffiti.model.v1.requirement import Requirement


class Resource(types.Base):
    id = wsme.wsattr(types.text, mandatory=True)
    type = wsme.wsattr(types.text, mandatory=True)
    name = wsme.wsattr(types.text, mandatory=True)
    description = wsme.wsattr(types.text, mandatory=False)
    provider = wsme.wsattr(Provider, mandatory=True)
    properties = wsme.wsattr([Property], mandatory=False)
    capabilities = wsme.wsattr([Capability], mandatory=True)
    requirements = wsme.wsattr([Requirement], mandatory=True)

    _wsme_attr_order = ('id', 'name', 'description', 'type',
                        'provider', 'properties', 'capabilities',
                        'requirements')

    def __init__(self, **kwargs):
        super(Resource, self).__init__(**kwargs)
