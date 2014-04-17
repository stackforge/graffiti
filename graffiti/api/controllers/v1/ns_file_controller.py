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
import json
from ns_controller import NSTypeControllerBase
from oslo.config import cfg
from wsme.rest.json import fromjson
from wsme.rest.json import tojson


class FileNSController(NSTypeControllerBase):

    def __init__(self, **kwargs):
        super(FileNSController, self).__init__(**kwargs)
        self._type = 'FileNSController'
        self._graffiti_folder = cfg.CONF.FILE_PERSISTENCE.dictionary_folder
        self._filename = "namespaces.json"
        self._namespacefile = self._graffiti_folder + self._filename
        self._namespaces = self.__file_to_memory()

    def get_namespace(self, namespace_name):
        return self._namespaces[namespace_name]

    def find_namespaces(self, query_string):
        return self._namespaces.itervalues()

    def set_namespace(self, namespace):
        self._namespaces[namespace.name] = namespace
        self.__memory_to_file()
        return namespace

    def put_namespace(self, namespace_name, namespace):
        self._namespaces[namespace_name] = namespace
        self.__memory_to_file()
        return namespace

    def delete_namespace(self, namespace_name):
        namespace = None
        if self._namespaces[namespace_name]:
            namespace = self._namespaces[namespace_name]
            self._namespaces.pop(namespace_name)
            self.__memory_to_file()
        return namespace

    def __file_to_memory(self):
        try:
            namespaces = {}
            with open(self._namespacefile, "r") as gfile:
                doc = json.load(gfile)
                for namespace in doc:
                    namespaces[namespace] = fromjson(Namespace, doc[namespace])
                return namespaces

        except IOError:
            with open(self._namespacefile, "w+") as gfile:
                gfile.write("")
            return {}

    def __memory_to_file(self):
        namespaces = {}
        for (namespace_name, namespace) in self._namespaces.items():
            json_data = tojson(Namespace, namespace)
            namespaces[namespace_name] = json_data

        with open(self._namespacefile, "w+") as gfile:
            json.dump(namespaces, gfile)
