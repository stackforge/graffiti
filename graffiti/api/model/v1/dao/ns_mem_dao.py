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

from graffiti.api.model.v1.dao.ns_dao import NSDAOBase


class MemNSDAO(NSDAOBase):

    def __init__(self, **kwargs):
        super(MemNSDAO, self).__init__(**kwargs)
        self._namespaces = {}
        self._type = "MemNSDAO"

    def get_type(self):
        return self._type

    def get_namespace(self, namespace_name):
        return self._namespaces[namespace_name]

    def find_namespaces(self, query_string):
        return self._namespaces.itervalues()

    def set_namespace(self, namespace):
        self._namespaces[namespace.name] = namespace
        return namespace

    def put_namespace(self, namespace_name, namespace):
        self._namespaces[namespace.name] = namespace
        return namespace

    def delete_namespace(self, namespace_name):
        namespace = None
        if self._namespaces[namespace_name]:
            namespace = self._namespaces[namespace_name]
            self._namespaces.pop(namespace_name)

        return namespace
