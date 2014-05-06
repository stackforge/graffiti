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


class CapabilityTypeDAOBase(object):

    def __init__(self, **kwargs):
        super(CapabilityTypeDAOBase, self).__init__(**kwargs)
        self._type = "CapabilityTypeDAOBase"

    def get_type(self):
        return self._type

    def get_capability_type(self, name, namespace):
        return None

    def get_capability_type_with_derived_properties(self, name, namespace):
        return None

    def find_capability_types(self, query_string):
        return []

    def set_capability_type(self, capability_type=None):
        pass

    def put_capability_type(self, name, namespace, capability_type=None):
        pass

    def delete_capability_type(self, name, namespace):
        pass
