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

from graffiti.api.model.v1.namespace import Namespace
from graffiti.db import api as dbapi
from ns_controller import NSTypeControllerBase


class DBNSController(NSTypeControllerBase):

    def __init__(self, **kwargs):
        super(DBNSController, self).__init__(**kwargs)
        self._type = 'DBNSController'

    def get_type(self):
        return self._type

    def get_namespace(self, namespace_name):
        db_namespace = dbapi.namespace_get(namespace_name)
        if not db_namespace:
            res = Namespace(Namespace(), status_code=404,
                            error="Namespace Not Found")
            return res

        return Namespace.to_model(db_namespace)

    def find_namespaces(self, query_string):
        dbnamespaces = dbapi.namespace_get_all()
        namespaces = []
        for ns in dbnamespaces:
            namespaces.append(Namespace.to_model(ns))
        return namespaces

    def set_namespace(self, namespace):
        created_namespace = dbapi.namespace_create(namespace.to_dict())
        return Namespace.to_model(created_namespace)

    def put_namespace(self, namespace_name, namespace):
        dbapi.namespace_update(namespace_name, namespace.to_dict())

    def delete_namespace(self, namespace_name):
        db_namespace = dbapi.namespace_get(namespace_name)
        if db_namespace:
            dbapi.namespace_delete(namespace_name)
            return Namespace.to_model(db_namespace)
