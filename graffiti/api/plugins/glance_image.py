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

from glanceclient import Client
from graffiti.api.model.v1.capability import Capability
from graffiti.api.model.v1.property import Property
from graffiti.api.model.v1.resource import Resource


class GlanceImage(object):

    def __init__(self, glance_endpoint, auth_token):
        self.glance_endpoint = glance_endpoint
        self.auth_token = auth_token
        self.glance = Client('1', endpoint=glance_endpoint, token=auth_token)
        self.separator = "."

    def get_resource(self, image_id):
        # glance_image_properties = {
        #    "GLANCE.MySQL.Port": "3605",
        #    "GLANCE.MySQL.Home": "/opt/mysql",
        #    "GLANCE.Apache.Port": "8080",
        #    "GLANCE.Apache.docroot": "/var/apache/static"
        # }
        image = self.glance.images.get(image_id)
        glance_image_properties = image.properties
        image_resource = Resource()
        image_capability = Capability()
        image_capabilities = []
        image_resource.capabilities = image_capabilities

        image_resource.id = image_id
        image_resource.type = 'image'
        # image_resource.name = "ubuntu 12.04"
        image_resource.name = image.name

        for key in glance_image_properties:
            # replace if check with pattern matching
            if key.count(self.separator) == 2:
                (namespace, capability_type, prop_name) = key.split(".")
                image_properties = []
                image_property = Property()
                image_property.name = prop_name
                image_property.value = glance_image_properties[key]

                image_capability = None
                for capability in image_resource.capabilities:
                    if capability.capability_type_namespace == namespace and \
                            capability.capability_type == capability_type:
                        image_capability = capability

                if not image_capability:
                    image_capability = Capability()
                    image_resource.capabilities.append(image_capability)

                image_capability.capability_type_namespace = namespace
                image_capability.capability_type = capability_type
                image_properties.append(image_property)

                image_capability.properties = image_properties

        return image_resource

    def update_resource(self, resource):
        """Update Glance Image
        :type param: graffiti.api.model.v1.resource.Resource
        """

        image_properties = {}
        for capability in resource.capabilities:
            properties = capability.properties
            capability_type = capability.capability_type
            capability_type_namespace = capability.capability_type_namespace
            for property in properties:
                prop_name = capability_type_namespace + \
                    self.separator + \
                    capability_type + \
                    self.separator + \
                    property.name
                image_properties[prop_name] = property.value

        image = self.glance.images.get(resource.id)
        image.update(properties=image_properties, purge_props=False)
