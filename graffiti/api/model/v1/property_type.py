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

from graffiti.api.model.v1.property_item_type import ItemType
import wsme
from wsme import types


class PropertyType(types.Base):
    type = wsme.wsattr(types.text, mandatory=True)
    description = wsme.wsattr(types.text, mandatory=False)
    default = wsme.wsattr(types.text, mandatory=False)
    required = wsme.wsattr(bool, mandatory=False, default=False)

    # fields for type = string
    minimum = wsme.wsattr(int, mandatory=False)
    maximum = wsme.wsattr(int, mandatory=False)

    # fields for type = integer, number
    minLength = wsme.wsattr(int, mandatory=False)
    maxLength = wsme.wsattr(int, mandatory=False)
    pattern = wsme.wsattr(types.text, mandatory=False)
    confidential = wsme.wsattr(bool, mandatory=False)

    # fields for type = array
    items = wsme.wsattr(ItemType, mandatory=False)
    uniqueItems = wsme.wsattr(bool, mandatory=False)
    minItems = wsme.wsattr(int, mandatory=False)
    maxItems = wsme.wsattr(int, mandatory=False)
    additionalItems = wsme.wsattr(bool, mandatory=False)

    _wsme_attr_order = ('type', 'description', 'default', 'required',
                        'minimum', 'maximum', 'minLength', 'maxLength',
                        'pattern', 'confidential', 'items', 'uniqueItems',
                        'additionalItems')

    def __init__(self, **kwargs):
        super(PropertyType, self).__init__(**kwargs)
