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
from graffiti.api.model.v1.capability_type import CapabilityType
import json
from oslo.config import cfg
from wsme.rest.json import fromjson
from wsme.rest.json import tojson


class FileCapabilityTypeController(CapabilityTypeControllerBase):

    def __init__(self, **kwargs):
        super(FileCapabilityTypeController, self).__init__(**kwargs)
        self._type = 'FileCapabilityTypeController'
        self._graffiti_folder = cfg.CONF.FILE_PERSISTENCE.dictionary_folder
        self._filename = "dictionary.json"
        self._dictionaryfile = self._graffiti_folder + self._filename
        self._capability_types = self.__file_to_memory()

    def get_capability_type(self, name, namespace):
        id = namespace + ":" + name
        return self._capability_types[id]

    def find_capability_types(self, query_string):
        return self._capability_types.itervalues()

    def set_capability_type(self, capability_type):
        id = capability_type.namespace + ":" + capability_type.name
        self._capability_types[id] = capability_type
        self.__memory_to_file()
        return capability_type

    def put_capability_type(self, name, namespace, capability_type):
        id = namespace + ":" + name
        self._capability_types[id] = capability_type
        self.__memory_to_file()
        return capability_type

    def delete_capability_type(self, name, namespace):
        id = namespace + ":" + name
        capability_type = None
        if self._capability_types[id]:
            capability_type = self._capability_types[id]
            self._capability_types.pop(id)
            self.__memory_to_file()
        return capability_type

    def __file_to_memory(self):
        try:
            capability_types = {}
            with open(self._dictionaryfile, "r") as gfile:
                doc = json.load(gfile)
                for id in doc:
                    capability_types[id] = fromjson(CapabilityType, doc[id])
                return capability_types

        except IOError:
            with open(self._dictionaryfile, "w+") as gfile:
                gfile.write("")
            return {}

    def __memory_to_file(self):
        file_capability_types = {}
        for (id, capability_type) in self._capability_types.items():
            json_data = tojson(CapabilityType, capability_type)
            file_capability_types[id] = json_data

        with open(self._dictionaryfile, "w+") as gfile:
            json.dump(file_capability_types, gfile)
