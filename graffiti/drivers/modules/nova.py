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

from graffiti.api.model.v1.capability import Capability
from graffiti.api.model.v1.resource import Resource
from graffiti.common import exception
from graffiti.drivers import base

from novaclient.v1_1 import client

from oslo.config import cfg


class NovaResourceDriver(base.ResourceInterface):

    def __init__(self):
        super(NovaResourceDriver, self).__init__()
        self.separator = ":"
        self.service_type = 'compute'

        self.endpoint_type = 'publicURL'
        self.default_namespace = "OS::COMPUTE::CPU"
        self.default_resource_type = "OS::Nova::Flavor"
        self.default_extraspec_key = "capabilities:cpu_info"

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

        nova_client = self.__get_nova_client(auth_token)

        flavor = nova_client.flavors.get(resource_id)

        flavor_resource = self.transform_flavor_to_resource(
            resource_type,
            flavor)

        return flavor_resource

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

        nova_client = self.__get_nova_client(auth_token)
        flavor = nova_client.flavors.get(resource_id)
        extraspecs = self.transform_resource_to_extraspecs(resource)
        flavor.set_keys(extraspecs)

    def find_resources(self, resource_query, auth_token,
                       endpoint_id=None, **kwargs):
        """Find resources matching the query
        :param query_string: query expression. Include resource type(s)
        :param auth_token: keystone auth_token of request user
        :param endpoint_id: id for locating the cloud resource provider
        :param **kwargs: Include additional info required by the driver,
        :returns list of resources
        """
        resource_list = dict()
        if resource_query:
            nova_client = self.__get_nova_client(auth_token)
            flavors = list(nova_client.flavors.list())
            for flavor in flavors:
                flavor_resource = self.transform_flavor_to_resource(
                    self.default_resource_type,
                    flavor
                )
                resource_list[flavor_resource.id] = flavor_resource

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

    def __get_nova_client(self, auth_token):
        auth_url = cfg.CONF.keystone.auth_url
        username = cfg.CONF.keystone.username
        password = cfg.CONF.keystone.password
        tenant_name = cfg.CONF.keystone.tenant_name

        nova_client = client.Client(
            username,
            password,
            tenant_name,
            auth_url,
            service_type="compute")

        return nova_client

    def transform_flavor_to_resource(self, resource_type, flavor):
        flavor_resource = Resource()
        flavor_resource.id = flavor.id
        flavor_resource.type = resource_type
        flavor_resource.name = flavor.name

        flavor_resource.capabilities = []
        flavor_resource.properties = {}

        flavor_resource.properties.update(
            {
                "ram": flavor.ram,
                "disk": flavor.disk,
                "vcpus": flavor.vcpus
            }
        )

        extra_spec_keys = flavor.get_keys()

        for key in extra_spec_keys:
            # capabilities:cpu_info:features=<in> aes
            # capabilities:cpu_info:vendor=Intel
            # capabilities:cpu_info:topology:cores=2
            # ssd = true
            # cap  {ct:aes, properties {name:features, value:<in>aes}}
            # cap  {ct:Intel, properties {name:vendor, value:Intel}}
            # cap  {ct:cores, properties {name:topology:cores, value=2}}
            # cap  {ct:sst, properties {name:ssd, value:true}}

            def splitFeatures(features):
                import re
                features = features.split()
                l = [v for v in features if not re.match("<(.*)>", v)]
                return l

            def extractFeatureValue(key, value):
                splited_key = key.split(':')
                splited_value = splitFeatures(value)

                c_name = splited_value[0]
                p_name = splited_key[-1]
                p_value = splited_value[0]
                return (c_name, p_name, p_value)

            def extractTopologyValue(key, value):
                splited = key.split(':')
                c_name = splited[-1]
                p_name = splited[-1]
                p_value = value
                return (c_name, p_name, p_value)

            def extractSimpleValue(key, value):
                splited = key.split(':')
                c_name = value
                p_name = splited[-1]
                p_value = value
                return (c_name, p_name, p_value)

            extraspecs_key_map = {
                "capabilities:cpu_info:features": extractFeatureValue,
                "capabilities:cpu_info:topology:cores": extractTopologyValue,
                "capabilities:cpu_info:topology:sockets": extractTopologyValue,
                "capabilities:cpu_info:topology:threads": extractTopologyValue,
            }

            capability_namespace = self.default_namespace
            capability_type = None
            property_name = None
            property_value = None

            if key in extraspecs_key_map:
                capability_type, property_name, property_value = \
                    extraspecs_key_map[key](key, extra_spec_keys[key])
            else:
                capability_type, property_name, property_value = \
                    extractSimpleValue(key, extra_spec_keys[key])

            capability_property = {property_name: property_value}

            flavor_capability = Capability()
            flavor_capability.properties = {}

            flavor_capability.capability_type_namespace = capability_namespace
            flavor_capability.capability_type = capability_type
            flavor_capability.properties.update(capability_property)

            flavor_resource.capabilities.append(flavor_capability)
        return flavor_resource

    def transform_resource_to_extraspecs(self, resource):
        extraspec = {}
        for capability in resource.capabilities:
            topology_properties = {
                "cores": "topology:cores",
                "threads": "topology:threads",
                "sockets": "topoloy:sockets",
            }

            base_key = ""
            if capability.capability_type_namespace == self.default_namespace:
                base_key = "capabilities:cpu_info"

            for property_name, property_value in capability.properties.items():
                if property_name == "features":
                    key = base_key + ':' + property_name
                    extraspec[key] = '<in> ' + property_value
                    continue
                if property_name in topology_properties:
                    key = base_key + ':' + topology_properties[property_name]
                    extraspec[key] = property_value
                    continue
                key = base_key + ':' + property_name
                extraspec[key] = property_value
        return extraspec
