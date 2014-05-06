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

from graffiti.api.model.v1.property_type import PropertyType
import wsme
from wsme import types


class DerivedPropertyType(PropertyType):
    '''mandatory is set to False instead of True, since wsme will complain
    while deserializing the properties to model. derived properties are
    dynamically added after the model is deserialized from persistence
    '''
    derived_from_capability_namespace = wsme.wsattr(
        types.text, mandatory=False)
    derived_from_capability_name = wsme.wsattr(types.text, mandatory=False)

    _wsme_attr_order = ('type', 'description', 'default', 'required',
                        'minimum', 'maximum', 'minLength', 'maxLength',
                        'pattern', 'confidential', 'items', 'uniqueItems',
                        'additionalItems', 'derived_from_capability_name',
                        'derived_from_capability_namespace')

    def __init__(self, **kwargs):
        super(DerivedPropertyType, self).__init__(**kwargs)
