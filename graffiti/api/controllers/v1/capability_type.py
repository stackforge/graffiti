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

from wsme.api import Response
from wsmeext.pecan import wsexpose

from graffiti.api.controllers.v1.captype_controller_factory \
    import CapTypeControllerFactory
from graffiti.api.model.v1.capability_type import CapabilityType
from ns_controller_factory import NSControllerFactory
from oslo.config import cfg


import six


class CapabilityTypeController(RestController):
    def __init__(self):
        super(RestController, self).__init__()
        self.status = 200
        self._cap_controller = None
        self._ns_controller = None
        self._load_controller()

    def _load_controller(self):
        controller_type = cfg.CONF.DEFAULT.persistence_type
        self._cap_controller = CapTypeControllerFactory.create(controller_type)
        self._ns_controller = NSControllerFactory.get()

    @wsexpose
    def options():
        pass

    @wsexpose(CapabilityType, six.text_type, six.text_type)
    def get_one(self, name, namespace):
        captype = self._cap_controller.get_capability_type(name, namespace)
        return captype

    @wsexpose([CapabilityType], six.text_type)
    def get_all(self, query_string=None):
        captype_list = self._cap_controller.find_capability_types(query_string)
        return captype_list

    @wsexpose(CapabilityType, body=CapabilityType)
    def post(self, capability_type):
        """Create Capability Type
        @type capability_type:
            graffiti.api.model.v1.capability_type.CapabilityType
        @param capability_type: Capability type
        """

        # Check if namespace exists
        namespace_found = self.__check_existing_namespace(
            capability_type.namespace
        )

        # Check if derived capability type exists
        derived_checked = self.__check_derived_capability(
            capability_type.derived_from
        )

        if namespace_found and derived_checked:
            self._cap_controller.set_capability_type(
                capability_type
            )
            return capability_type
        else:
            res = Response(
                CapabilityType(),
                status_code=404,
                error="Provided namespace %s doesnt exist" %
                      capability_type.namespace)
            return res

    @wsexpose(CapabilityType, six.text_type, six.text_type,
              body=CapabilityType)
    def put(self, name, namespace, capability_type):

        # Check if namespace exists
        namespace_found = self.__check_existing_namespace(
            capability_type.namespace
        )

        # Check if derived capability type exists
        derived_checked = self.__check_derived_capability(
            capability_type.derived_from
        )

        if namespace_found and derived_checked:
            self._cap_controller.put_capability_type(
                name, namespace, capability_type
            )
            return capability_type
        else:
            res = Response(
                CapabilityType(),
                status_code=404,
                error="Provided namespace %s doesnt exist" %
                      capability_type.namespace)
            return res

    @wsexpose(CapabilityType, six.text_type, six.text_type)
    def delete(self, name, namespace):
        captype = self._cap_controller.delete_capability_type(
            name,
            namespace
        )
        return captype

    def __check_derived_capability(self, derived_from):
        derived_checked = True
        if derived_from:
            derived_checked = False
            derived_cap_found = self._cap_controller.get_capability_type(
                derived_from.name, derived_from.namespace)
            if derived_cap_found:
                derived_checked = True

        return derived_checked

    def __check_existing_namespace(self, namespace_name):
        return self._ns_controller.get_namespace(namespace_name)
