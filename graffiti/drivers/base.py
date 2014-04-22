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

"""
Abstract base class for graffiti resource drivers.
"""

import abc
import six


@six.add_metaclass(abc.ABCMeta)
class BaseDriver(object):
    """Base class for all drivers.

    Defines resource and definitions interface.
    Any loadable driver must implement the interfaces it supports

    """

    resource = None

    #TBD in future
    #definitions = None

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def get_resource_types(self):
        """Returns the resource types supported by the implementing driver
        :returns [str]  List of resource type strings
        """


@six.add_metaclass(abc.ABCMeta)
class ResourceInterface(object):

    @abc.abstractmethod
    def get_resource(self, resource_id, auth_token, endpoint_id=None,
                     **kwargs):
        """Retrieve the resource detail
        :param resource_id: unique resource identifier
        :param auth_token: keystone auth_token of request user
        :param endpoint_id: id for locating the cloud resource provider
        :param **kwargs: Include additional info required by the driver,
        :returns resource detail
        """

    @abc.abstractmethod
    def find_resources(self, query_string, auth_token, endpoint_id=None,
                       **kwargs):
        """Find resources matching the query
        :param query_string: query expression
        :param auth_token: keystone auth_token of request user
        :param endpoint_id: id for locating the cloud resource provider
        :param **kwargs: Include additional info required by the driver,
        :returns list of resources
        """

    @abc.abstractmethod
    def create_resource(self, resource, auth_token, endpoint_id=None,
                        **kwargs):
        """Create resource
        :param resource: resource detail
        :param auth_token: keystone auth_token of request user
        :param endpoint_id: id for locating the cloud resource provider
        :param **kwargs: Include additional info required by the driver,
        """

    @abc.abstractmethod
    def update_resource(self, resource_id, resource, auth_token,
                        endpoint_id=None, **kwargs):
        """Update resource
        :param resource_id: unique resource identifier
        :param resource: resource detail
        :param auth_token: keystone auth_token of request user
        :param endpoint_id: id for locating the cloud resource provider
        :param **kwargs: Include additional info required by the driver,
        """

    @abc.abstractmethod
    def delete_resource(self, resource_id, auth_token, endpoint_id=None,
                        **kwargs):
        """Delete resource
        :param resource_id: unique resource identifier
        :param auth_token: keystone auth_token of request user
        :param endpoint_id: id for locating the cloud resource provider
        :param **kwargs: Include additional info required by the driver,
        """
