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


class ResourceControllerBase(object):

    def __init__(self, **kwargs):
        super(ResourceControllerBase, self).__init__(**kwargs)

        self._type = 'None'

    def get_resource(self, id):
        return None

    def get_type(self):
        return self._type

    def find_resources(self, query_string):
        return []

    def set_resource(self, id=None, resource_definition=None):
        pass


class LocalResourceController(ResourceControllerBase):

    def __init__(self, **kwargs):
        super(LocalResourceController, self).__init__(**kwargs)

        self._type = 'LocalResourceController'

        self._resources = dict()
        self._last_id = 0

    def get_resource(self, id):
        return self._resources[id]

    def find_resources(self, query_string):
        return self._resources

    def set_resource(self, id=None, resource_definition=None):
        if not id:
            id = self._generate_id()

        self._resources[id] = resource_definition

    def _generate_id(self):
        return_value = self._last_id
        self._last_id += 1

        return return_value
