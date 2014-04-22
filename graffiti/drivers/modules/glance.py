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
from graffiti.drivers import base

import keystoneclient.v2_0.client as ksclient

from oslo.config import cfg


class GlanceResourceDriver(base.ResourceInterface):

    def __init__(self):
        super(GlanceResourceDriver, self).__init__()
        self.separator = "."

    def get_resource(self, resource_id, auth_token, endpoint_id=None,
                     **kwargs):
        """Retrieve the resource detail
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
        glance_image_properties = image.properties
        image_resource = Resource()
        image_capabilities = []
        image_resource.capabilities = image_capabilities

        image_resource.id = resource_id
        image_resource.type = 'image'
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

    def update_resource(self, resource_id, resource, auth_token,
                        endpoint_id=None, **kwargs):
        """Update resource
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

        image = glance_client.images.get(resource.id)
        image.update(properties=image_properties, purge_props=False)

    def find_resources(self, query_string, auth_token, endpoint_id=None,
                       **kwargs):
        """Find resources matching the query
        :param query_string: query expression
        :param auth_token: keystone auth_token of request user
        :param endpoint_id: id for locating the cloud resource provider
        :param **kwargs: Include additional info required by the driver,
        :returns list of resources
        """
        #TODO(Lakshmi): Implement this method
        pass

    def create_resource(self, resource, auth_token, endpoint_id=None,
                        **kwargs):
        """Create resource
        :param resource: resource detail
        :param auth_token: keystone auth_token of request user
        :param endpoint_id: id for locating the cloud resource provider
        :param **kwargs: Include additional info required by the driver,
        """
        raise exception.MethodNotSupported(method="create_resource")

    def delete_resource(self, resource_id, auth_token, endpoint_id=None,
                        **kwargs):
        """Delete resource
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
        self.__endpoint_list = keystone.endpoints.list()
        for endpoint in self.__endpoint_list:
            if endpoint.id == endpoint_id:
                glance_public_url = endpoint.publicurl
        glance_client = Client(
            '1',
            endpoint=glance_public_url,
            token=auth_token
        )
        return glance_client
