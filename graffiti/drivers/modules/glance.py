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
from graffiti.common import exception
from graffiti.common import utils
from graffiti.drivers import base

import keystoneclient.v2_0.client as ksclient

from oslo.config import cfg


class GlanceResourceDriver(base.ResourceInterface):

    def __init__(self):
        super(GlanceResourceDriver, self).__init__()
        self.separator = "."
        self.service_type = 'image'
        self.endpoint_type = 'publicURL'
        self.default_namespace_postfix = "::Default"
        self.unknown_properties_type = "AdditionalProperties"

    def get_resource(self, resource_type, resource_id, auth_token,
                     endpoint_id=None, **kwargs):
        """Retrieve the resource detail
        :param resource_type: resource_type set for this call
        :param resource_id: unique resource identifier
        :param auth_token: keystone auth_token of request user
        :param endpoint_id: id for locating the cloud resource provider
        :param **kwargs: Include additional info required by the driver,
        :returns resource detail
        """

        # glance_image_properties = {
        #    "GLANCE.MySQL.Port": "3605",
        #    "GLANCE.MySQL.Home": "/opt/mysql",
        #    "GLANCE.Apache.Port": "8080",
        #    "GLANCE.Apache.docroot": "/var/apache/static"
        # }

        glance_client = self.__get_glance_client(endpoint_id, auth_token)

        image = glance_client.images.get(resource_id)
        image_resource = self.transform_image_to_resource(resource_type, image)

        return image_resource

    def update_resource(self, resource_type, resource_id, resource, auth_token,
                        endpoint_id=None, **kwargs):
        """Update resource
        :param resource_type: resource_type set for this call
        :param resource_id: unique resource identifier
        :param resource: resource detail
        :type param: graffiti.api.model.v1.resource.Resource
        :param auth_token: keystone auth_token of request user
        :param endpoint_id: id for locating the cloud resource provider
        :param **kwargs: Include additional info required by the driver,
        """

        glance_client = self.__get_glance_client(endpoint_id, auth_token)

        image_properties = {}
        for capability in resource.capabilities:
            if capability.capability_type_namespace \
                == resource_type + self.default_namespace_postfix \
                and capability.capability_type \
                == self.unknown_properties_type:
                # For unknown properties, just directly set property name.
                for property_name, property_value in \
                        capability.properties.iteritems():
                    image_properties[property_name] = property_value
            else:
                properties = capability.properties
                #capability_type = self.replace_colon_from_name(
                #    capability.capability_type
                #)
                #capability_type_namespace = self.replace_colon_from_name(
                #    capability.capability_type_namespace
                #)

                for property_name, property_value in properties.iteritems():
                    #prop_name = capability_type_namespace + \
                    #    self.separator + \
                    #    capability_type + \
                    #    self.separator + \
                    #    self.replace_colon_from_name(property_name)
                    prop_name = self.replace_colon_from_name(property_name)
                    image_properties[prop_name] = property_value

                # if capability doesnt have properties add capability as TAG
                if not properties:
                    tag_name = capability.capability_type
                    image_properties[tag_name] = utils.TAG_IDENTIFIER

        image = glance_client.images.get(resource.id)
        image.update(properties=image_properties, purge_props=True)

    def find_resources(self, resource_query, auth_token,
                       endpoint_id=None, **kwargs):
        """Find resources matching the query
        :param resource_query: query object. Includes resource type(s)
        :param auth_token: keystone auth_token of request user
        :param endpoint_id: id for locating the cloud resource provider
        :param **kwargs: Include additional info required by the driver,
        :returns list of resources
        """
        resource_list = dict()
        if resource_query:
            glance_client = self.__get_glance_client(
                endpoint_id,
                auth_token
            )
            images = glance_client.images.list()
            for image in list(images):
                #Filter based on requested resource types
                glance_image_properties = image.properties
                image_type = "OS::Glance::Image"
                if "image_type" in glance_image_properties.keys():
                    image_type = glance_image_properties['image_type']
                    if image_type and image_type.lower() == "snapshot":
                        image_type = "OS::Glance::Snapshot"

                if image_type in resource_query.resource_types:
                    resource = self.transform_image_to_resource(
                        image_type,
                        image
                    )
                    resource_list[resource.id] = resource
        return resource_list

    def create_resource(self, resource_type, resource, auth_token,
                        endpoint_id=None, **kwargs):
        """Create resource
        :param resource_type: resource_type set for this call
        :param resource: resource detail
        :param auth_token: keystone auth_token of request user
        :param endpoint_id: id for locating the cloud resource provider
        :param **kwargs: Include additional info required by the driver,
        """
        raise exception.MethodNotSupported(method="create_resource")

    def delete_resource(self, resource_type, resource_id, auth_token,
                        endpoint_id=None, **kwargs):
        """Delete resource
        :param resource_type: resource_type set for this call
        :param resource_id: unique resource identifier
        :param auth_token: keystone auth_token of request user
        :param endpoint_id: id for locating the cloud resource provider
        :param **kwargs: Include additional info required by the driver,
        """
        raise exception.MethodNotSupported(method="delete_resource")

    def __get_glance_client(self, endpoint_id, auth_token):
        keystone = ksclient.Client(
            auth_url=cfg.CONF.keystone.auth_url,
            username=cfg.CONF.keystone.username,
            password=cfg.CONF.keystone.password,
            tenant_name=cfg.CONF.keystone.tenant_name
        )

        glance_public_url = None
        if endpoint_id:
            for entry in keystone.service_catalog.catalog.get(
                    'serviceCatalog'):
                for endpoint in entry['endpoints']:
                    if endpoint['id'] == endpoint_id:
                        glance_public_url = endpoint['publicURL']
                        break
                if glance_public_url:
                    break
        else:
            glance_public_url = keystone.service_catalog.url_for(
                service_type=self.service_type,
                endpoint_type=self.endpoint_type
            )
        glance_client = Client(
            '1',
            endpoint=glance_public_url,
            token=auth_token
        )
        return glance_client

    def transform_image_to_resource(self, resource_type, image):
        glance_image_properties = image.properties
        image_resource = Resource()
        image_capabilities = []
        image_resource.capabilities = image_capabilities

        image_resource.id = image.id
        image_resource.type = resource_type
        image_resource.name = image.name

        for key in glance_image_properties:
            if key.count(self.separator) == 2:
                (namespace, capability_type, prop_name) = key.split(".")
                namespace = self.replace_hash_from_name(namespace)
                capability_type = self.replace_hash_from_name(capability_type)
                prop_name = self.replace_hash_from_name(prop_name)
            else:
                prop_name = key
                capability_type = None
                namespace = None

                cap_and_namespace = utils.get_qualifier(
                    key,
                    glance_image_properties[key]
                )
                if cap_and_namespace:
                    capability_type = cap_and_namespace.name
                    namespace = cap_and_namespace.namespace
                else:
                    namespace = resource_type + self.default_namespace_postfix
                    capability_type = self.unknown_properties_type

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
                image_capability.properties = {}
                image_resource.capabilities.append(image_capability)

            image_capability.capability_type_namespace = namespace
            image_capability.capability_type = capability_type
            image_capability.properties[image_property.name] = \
                image_property.value

        return image_resource

    def replace_colon_from_name(self, name):
        if name:
            return name.replace(':', '#')
        return

    def replace_hash_from_name(self, name):
        if name:
            return name.replace('#', ':')
        return
