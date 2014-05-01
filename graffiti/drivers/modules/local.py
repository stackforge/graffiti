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

from graffiti.api.model.v1.dao.resource_dao_factory import \
    ResourceDAOFactory

from graffiti.drivers import base

from oslo.config import cfg


class LocalResourceDriver(base.ResourceInterface):

    def __init__(self):
        super(LocalResourceDriver, self).__init__()
        persistence_type = cfg.CONF.DEFAULT.persistence_type

        self._resource_dao = ResourceDAOFactory.create(persistence_type)

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

        res = self._resource_dao.get_resource(resource_id)
        return res

    def find_resources(self, query_string, auth_token,
                       endpoint_id=None, **kwargs):
        """Find resources matching the query
        :param query_string: query expression. Include resource type(s)
        :param auth_token: keystone auth_token of request user
        :param endpoint_id: id for locating the cloud resource provider
        :param **kwargs: Include additional info required by the driver,
        :returns list of resources
        """
        res_list = self._resource_dao.find_resources(query_string)
        if res_list:
            return res_list

        return []

    def create_resource(self, resource_type, resource, auth_token,
                        endpoint_id=None, **kwargs):
        """Create resource
        :param resource_type: resource_type set for this call
        :param resource: resource detail
        :param auth_token: keystone auth_token of request user
        :param endpoint_id: id for locating the cloud resource provider
        :param **kwargs: Include additional info required by the driver,
        """

        id = resource.id if hasattr(resource, 'id') else None
        self._resource_dao.set_resource(id, resource=resource)

        return resource

    def update_resource(self, resource_type, resource_id, resource,
                        auth_token, endpoint_id=None, **kwargs):
        """Update resource
        :param resource_type: resource_type set for this call
        :param resource_id: unique resource identifier
        :param resource: resource detail
        :param auth_token: keystone auth_token of request user
        :param endpoint_id: id for locating the cloud resource provider
        :param **kwargs: Include additional info required by the driver,
        """
        self._resource_dao.set_resource(
            resource_id,
            resource=resource
        )
        return resource

    def delete_resource(self, resource_type, resource_id, auth_token,
                        endpoint_id=None, **kwargs):
        """Delete resource
        :param resource_type: resource_type set for this call
        :param resource_id: unique resource identifier
        :param auth_token: keystone auth_token of request user
        :param endpoint_id: id for locating the cloud resource provider
        :param **kwargs: Include additional info required by the driver,
        """
        #TODO(Lakshmi): Implement delete
        pass
