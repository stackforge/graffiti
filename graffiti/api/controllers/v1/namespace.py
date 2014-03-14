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

from graffiti.api.model.v1.namespace import Namespace

import six

namespaces = []


class NamespaceController(RestController):
    def __init__(self):
        super(RestController, self).__init__()
        self.status = 200

    @wsexpose
    def options():
        pass

    @wsexpose(Namespace, six.text_type)
    def get_one(self, name):
        global namespaces

        for namespace in namespaces:
            if namespace.name.lower() == name.lower():
                return namespace

        res = Namespace(Namespace(), status_code=404,
                        error="Namespace Not Found")
        return res

    @wsexpose([Namespace])
    def get_all(self):
        global namespaces
        return namespaces

    @wsexpose(Namespace, body=Namespace)
    def post(self, namespace):
        global namespaces
        namespaces.append(namespace)
