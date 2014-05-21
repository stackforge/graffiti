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


from graffiti.api.model.v1.capability_type_key import CapabilityTypeKey
from graffiti.common.utilities.capability_type_tree_node \
    import CapabilityTypeTreeNode


class CapabilityTypeTree():

    def __init__(self, **kwargs):
        self.root_types = {}
        self.types_with_external_root = {}

    def build(self, capability_type_list):
        capability_types = {}
        for cap_type in capability_type_list:
            # todo(wko): raise error if duplicate found
            key = CapabilityTypeKey(name=cap_type.name,
                                    namespace=cap_type.namespace)
            capability_types[key] = cap_type

        # Handle: 1) No parent 2) No children (no-op)
        #         3) Parent in tree
        #         4) Parent not processed, yet
        #         5) More than one root in input (not common ancestor)
        #         6) Type has parent, but not in input (external parent)
        types_with_unmapped_parents = {}
        for current_key, current_cap_type in capability_types.iteritems():
            current_node = CapabilityTypeTreeNode()
            current_node.cap_type = current_cap_type

            # Scenario 1 & 5
            if not current_cap_type.derived_from \
                    or not current_cap_type.derived_from.name:
                self.root_types[current_key] = current_node
                continue

            if self.insert_node(self.root_types, current_key, current_node):
                # Scenario 3
                continue
            elif self.insert_node(types_with_unmapped_parents,
                                  current_key, current_node):
                # Scenario 3 (not converged)
                continue
            else:
                # Scenario 4 part a
                types_with_unmapped_parents[current_key] = current_node

        # Scenario 4 part b
        # Perform eventual convergence on roots
        self.converge_unmapped_types(self.root_types,
                                     types_with_unmapped_parents)

        # Perform eventual convergence on types_with_unmapped_parents
        self.converge_unmapped_types(types_with_unmapped_parents,
                                     types_with_unmapped_parents)

        # Scenario 6
        self.types_with_external_root.update(types_with_unmapped_parents)

    def insert_node(self, cap_types, current_key, current_node):
        # For each cap_type
        #   if it is the parent of the current_node.cap_type
        #       set root_node as the current_node.parent_node
        #       add the current_node to root_node.children
        #       break
        #   else
        #       recursively check if parent is in root_node.children
        #       break if found
        result = False
        if cap_types:
            i = 0
            for root_key, root_node in cap_types.iteritems():
                # todo(wko): derived_from should be a CapabilityTypeKey
                current_parent_name = current_node.cap_type.derived_from.name
                current_parent_namesp = \
                    current_node.cap_type.derived_from.namespace

                if root_key.name == current_parent_name and\
                   root_key.namespace == current_parent_namesp:
                    current_node.parent_node = root_node
                    root_node.children[current_key] = current_node
                    result = True
                    break

                result = self.insert_node(root_node.children, current_key,
                                          current_node)
                if result:
                    break
                i += 1

        return result

    def converge_unmapped_types(self, root_types, types_with_unmapped_parents):

        previous_loop_unmapped_parents = 0
        num_loops_without_change = 0

        while len(types_with_unmapped_parents) > 0 \
                and num_loops_without_change < 2:
            types_with_found_parent = []
            for unmapped_key, unmapped_node in \
                    types_with_unmapped_parents.iteritems():
                result = self.insert_node(root_types, unmapped_key,
                                          unmapped_node)
                if result:
                    types_with_found_parent.append(unmapped_key)
                    continue

            for mapped_parent in types_with_found_parent:
                del types_with_unmapped_parents[mapped_parent]

            this_loop_unmapped_parents = len(types_with_unmapped_parents)
            if previous_loop_unmapped_parents == this_loop_unmapped_parents:
                num_loops_without_change += 1
            else:
                num_loops_without_change = 0

            previous_loop_unmapped_parents = this_loop_unmapped_parents
