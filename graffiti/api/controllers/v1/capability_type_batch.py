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


from graffiti.api.model.v1.capability_type import CapabilityType
from graffiti.api.model.v1.dao.captype_dao_factory \
    import CapabilityTypeDAOFactory
from graffiti.api.model.v1.dao.ns_dao_factory import NSDAOFactory

from graffiti.common import exception as exc
from graffiti.common.utilities.capability_type_tree import CapabilityTypeTree

from oslo.config import cfg
from pecan.rest import RestController
from wsmeext.pecan import wsexpose


class CapabilityTypeBatchController(RestController):
    def __init__(self):
        super(RestController, self).__init__()
        self.status = 200
        self._cap_controller = None
        self._ns_controller = None
        self._load_controller()

    def _load_controller(self):
        dao_type = cfg.CONF.DEFAULT.persistence_type
        self._cap_controller = CapabilityTypeDAOFactory.create(dao_type)
        self._ns_controller = NSDAOFactory.get()

    @wsexpose
    def options(self):
        pass

    @wsexpose([CapabilityType], body=[CapabilityType])
    def post(self, capability_types):
        """Batch create capability types
        @param capability_types: list of CapabilityTypes
        """

        cap_types = []
        # Verify all namespaces exists
        self.__verify_namespaces(capability_types)

        tree = CapabilityTypeTree()
        tree.build(capability_types)

        # TODO(wko): verify external derived roots
        # self.__verify_external_derived_roots_exist(
        #    tree.types_with_external_root)

        for cap_key, cap_node in tree.root_types.iteritems():
            self.create_capability_type_recursively(cap_node, cap_types)

        return cap_types

    def create_capability_type_recursively(self, tree_node, cap_types):
        if tree_node:
            capability_type = tree_node.cap_type
            exists_ct = self._cap_controller.get_capability_type(
                capability_type.name, capability_type.namespace)

            if exists_ct:
                # update
                self._cap_controller.put_capability_type(
                    capability_type.name, capability_type.namespace,
                    capability_type
                    )
                cap_types.append(capability_type)
            else:
                # add
                new_ct = self._cap_controller.set_capability_type(
                    capability_type)
                cap_types.append(new_ct)

            for cap_key, child_node in tree_node.children.iteritems():
                self.create_capability_type_recursively(child_node, cap_types)

    def __verify_namespaces(self, capability_types):
        namespaces = []
        for ct in capability_types:
            if ct.namespace not in namespaces:
                namespaces.append(ct.namespace)

        found_namespace = False
        for namespace in namespaces:
            found_namespace = self._ns_controller.get_namespace(namespace)
            if not found_namespace:
                raise exc.NotFound("namespace:{0} - does not exist".
                                   format(namespace))
