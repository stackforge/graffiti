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

from graffiti.api.model.v1.dao.ns_dao_factory \
    import NSDAOFactory
from graffiti.api.model.v1.namespace import Namespace
from oslo.config import cfg
import six


class NamespaceController(RestController):
    def __init__(self):
        super(RestController, self).__init__()
        self.status = 200
        self._controller = self._load_controller()

    def _load_controller(self):
        controller_type = cfg.CONF.DEFAULT.persistence_type
        _controller = NSDAOFactory.create(controller_type)
        return _controller

    @wsexpose
    def options(self):
        pass

    @wsexpose(Namespace, six.text_type)
    def get_one(self, namespace_name):
        namespace = self._controller.get_namespace(namespace_name)
        return namespace

    @wsexpose([Namespace])
    def get_all(self, query_string=None):
        namespace_list = self._controller.find_namespaces(query_string)
        return namespace_list

    @wsexpose(Namespace, body=Namespace)
    def post(self, namespace):
        """Create Namespace
        :namespace param:
         graffiti.api.model.v1.namespace.Namespace
        """

        self._controller.set_namespace(namespace)
        return namespace

    @wsexpose(Namespace, six.text_type, body=Namespace)
    def put(self, namespace_name, namespace):
        self._controller.put_namespace(namespace_name, namespace)
        return namespace

    @wsexpose(Namespace, six.text_type)
    def delete(self, namespace_name):
        print "namespace", namespace_name
        namespace = self._controller.delete_namespace(namespace_name)
        return namespace
