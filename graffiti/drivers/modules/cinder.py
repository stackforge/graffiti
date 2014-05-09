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

from cinderclient import client
from graffiti.api.model.v1.capability import Capability
from graffiti.api.model.v1.property import Property
from graffiti.api.model.v1.resource import Resource
from graffiti.common import exception
from graffiti.drivers import base
from graffiti.openstack.common import log as logging

import keystoneclient.v2_0.client as ksclient

from oslo.config import cfg


LOG = logging.getLogger(__name__)


class CinderResourceDriver(base.ResourceInterface):

    def __init__(self):
        super(CinderResourceDriver, self).__init__()
        self.volume_type = 'OS::Cinder::Volume'
        self.snapshot_type = 'OS::Cinder::VolumeSnapshot'
        self.separator = "."
        self.service_type = 'volume'
        self.endpoint_type = 'publicURL'
        self.default_namespace_suffix = "::Default"
        self.unknown_properties_type = "AdditionalProperties"
        self.unmodifiable_properties = [u'instance_uuid', u'kernel_id',
                                        u'ramdisk_id', u'disk_format',
                                        u'image_name', u'image_id',
                                        u'readonly', u'container_format',
                                        u'checksum', u'size']

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

        cinder_client = self.__get_cinder_client(endpoint_id, auth_token)

        cinder_resource = None

        if resource_type == self.volume_type:
            cinder_resource = cinder_client.volumes.get(resource_id)
        elif resource_type == self.snapshot_type:
            cinder_resource = cinder_client.volume_snapshots.get(resource_id)

        if cinder_resource:
            cinder_resource = self.transform_to_resource(
                resource_type, cinder_resource)

        return cinder_resource

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

        cinder_client = self.__get_cinder_client(endpoint_id, auth_token)

        cinder_properties = {}
        for capability in resource.capabilities:
            if capability.capability_type_namespace \
                    == resource_type + self.default_namespace_suffix \
                    and capability.capability_type \
                    == self.unknown_properties_type:
                # For unknown properties, just directly set property name.
                for property_name, property_value in \
                        capability.properties.iteritems():
                    cinder_properties[property_name] = property_value
            else:
                properties = capability.properties
                capability_type = self.replace_colon_from_name(
                    capability.capability_type
                )
                capability_type_namespace = self.replace_colon_from_name(
                    capability.capability_type_namespace
                )

                for property_name, property_value in properties.iteritems():
                    prop_name = capability_type_namespace + \
                        self.separator + \
                        capability_type + \
                        self.separator + \
                        self.replace_colon_from_name(property_name)
                    cinder_properties[prop_name] = property_value

        cinder_resource = None

        if resource_type == self.volume_type:
            cinder_resource = cinder_client.volumes.get(resource_id)
        elif resource_type == self.snapshot_type:
            cinder_resource = cinder_client.volume_snapshots.get(resource_id)

        properties_to_remove = \
            self._get_merged_properties(cinder_resource).keys()
        #TODO(Travis) metadata_to_delete = []
        for property_to_keep in cinder_properties:
            try:
                properties_to_remove.remove(property_to_keep)
            except ValueError:
                #Sometimes properties to delete don't exist on server
                pass

        try:
            cinder_resource.set_metadata(cinder_resource, cinder_properties)
            #TODO(Travis) cinder_client.volumes.
            # delete_metadata(volume, properties_to_remove)
        except AttributeError:
            #Temporary until bug fixed
            LOG.debug('Hit error: https://bugs.launchpad.net/bugs/1315175')
            pass

    def find_resources(self, resource_query, auth_token,
                       endpoint_id=None, **kwargs):
        """Find resources matching the query
        :param resource_query: query object. Includes resource type(s)
        :param auth_token: keystone auth_token of request user
        :param endpoint_id: id for locating the cloud resource provider
        :param **kwargs: Include additional info required by the driver,
        :returns list of resources
        """
        result = dict()
        #TODO(Travis): Filter based on resource type for snapshot etc
        if resource_query:
            cinder_client = self.__get_cinder_client(endpoint_id, auth_token)
            for resource_type in resource_query.resource_types:
                cinder_resource_list = []
                if resource_type == self.volume_type:
                    cinder_resource_list = cinder_client.volumes.list()
                elif resource_type == self.snapshot_type:
                    cinder_resource_list = \
                        cinder_client.volume_snapshots.list()
                for cinder_resource in cinder_resource_list:
                    if cinder_resource.status and \
                            cinder_resource.status == 'available':
                        resource = self.transform_to_resource(
                            resource_type,
                            cinder_resource)
                        if resource:
                            result[resource.id] = resource

        return result

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

    def __get_cinder_client(self, endpoint_id, auth_token):
        keystone = ksclient.Client(
            auth_url=cfg.CONF.keystone.auth_url,
            username=cfg.CONF.keystone.username,
            password=cfg.CONF.keystone.password,
            tenant_name=cfg.CONF.keystone.tenant_name
        )

        cinder_public_url = None
        if endpoint_id:
            for entry in keystone.service_catalog.catalog.get(
                    'serviceCatalog'):
                for endpoint in entry['endpoints']:
                    if endpoint['id'] == endpoint_id:
                        cinder_public_url = endpoint['publicURL']
                        break
                if cinder_public_url:
                    break
        else:
            cinder_public_url = keystone.service_catalog.url_for(
                service_type=self.service_type,
                endpoint_type=self.endpoint_type
            )

        cinder_client = client.Client(
            '1',
            cfg.CONF.keystone.username,
            cfg.CONF.keystone.password,
            cfg.CONF.keystone.tenant_name,
            cfg.CONF.keystone.auth_url
        )
        return cinder_client

    def _get_merged_properties(self, volume):
        cinder_volume_properties = {}
        volume_metadata = {}
        volume_image_metadata = {}
        try:
            volume_image_metadata = volume.volume_image_metadata
        except AttributeError:
            pass
        try:
            volume_metadata = volume.metadata
        except AttributeError:
            pass
        cinder_volume_properties = dict(volume_metadata,
                                        **volume_image_metadata)
        return cinder_volume_properties

    def transform_to_resource(self, resource_type, volume):

        cinder_volume_properties = self._get_merged_properties(volume)

        result = Resource()
        result_capabilities = []
        result.capabilities = result_capabilities

        result.id = volume.id
        result.type = resource_type
        #v1 / v2 clients have landmines
        result.name = None
        try:
            result.name = volume.name
        except AttributeError:
            result.name = volume.display_name

        for key in cinder_volume_properties:
            if key in self.unmodifiable_properties:
                continue

            if key.count(self.separator) == 2:
                (namespace, capability_type, prop_name) = key.split(".")
                namespace = self.replace_hash_from_name(namespace)
                capability_type = self.replace_hash_from_name(capability_type)
                prop_name = self.replace_hash_from_name(prop_name)
            else:
                namespace = resource_type + self.default_namespace_suffix
                capability_type = self.unknown_properties_type
                prop_name = key

            result_property = Property()
            result_property.name = prop_name
            result_property.value = cinder_volume_properties[key]

            result_capability = None
            for capability in result.capabilities:
                if capability.capability_type_namespace == namespace and \
                        capability.capability_type == capability_type:
                    result_capability = capability

            if not result_capability:
                result_capability = Capability()
                result_capability.properties = {}
                result.capabilities.append(result_capability)

            result_capability.capability_type_namespace = namespace
            result_capability.capability_type = capability_type
            result_capability.properties[result_property.name] = \
                result_property.value

        return result

    def replace_colon_from_name(self, name):
        if name:
            return name.replace(':', '#')
        return

    def replace_hash_from_name(self, name):
        if name:
            return name.replace('#', ':')
        return
