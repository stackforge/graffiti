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

import pecan
from pecan.rest import RestController


from wsme.api import Response
from wsmeext.pecan import wsexpose

from graffiti.api.model.v1.resource import Resource
from graffiti.common import driver_factory

import six


class ResourceController(RestController):

    def __init__(self):
        super(ResourceController, self).__init__()
        self.status = 200
        self.default_resource_type = "GFT::Local"

    @wsexpose(None, six.text_type, six.text_type, six.text_type)
    def options(self, param1, param2=None, param3=None):
        return Response(None, status_code=204)

    @wsexpose(Resource, six.text_type, six.text_type, six.text_type)
    def get_one(self, param1, param2=None, param3=None):
        """Retrieve the resource based on the passed parameters
        Depending on the number of parameters passed, the meaning
        of the parameter is determined.

        Use case #1: only param1 is set
        eg. /v1/resource/12345
        param1 is treated as resource id and resource type is defaulted
        to graffiti local resource

        Use case #2: param1 and param2 are set
        eg /v1/resource/OS::Glance::Image/d24a33343
        param1 = resource type
        param2 = resource id

        Use case #3: param1, param2 and param3 are set
        eg /v1/resource/OS::Glance::Image/d24a33343/e8dd383a838c83
        param1 = resource type
        param2 = resource id
        param3 = endpoint id

        """
        print "args:", param1, param2, param3
        auth_token = pecan.request.headers.get('X-Auth-Token')
        endpoint_id = None

        if not param2:
            #Use case #1
            resource_id = param1
            resource_type = self.default_resource_type
        else:
            #Use case #2
            resource_type = param1
            resource_id = param2

        if param3:
            endpoint_id = param3

        driver = driver_factory.get_driver(resource_type)
        if driver.resource:
            res = driver.resource.get_resource(
                resource_id,
                auth_token,
                endpoint_id
            )
            return res
        else:
            error_str = "Driver not found for the resource type %s", \
                        resource_type

        res = Response(Resource(), status_code=404, error=error_str)
        return res

    @wsexpose([Resource], six.text_type, six.text_type)
    def get_all(self, resource_type=None, query_string=None):
        auth_token = pecan.request.headers.get('X-Auth-Token')

        if not resource_type:
            resource_type = self.default_resource_type

        driver = driver_factory.get_driver(resource_type)
        if driver.resource:
            res_list = driver.resource.find_resources(
                query_string,
                auth_token
            )
            if res_list:
                return res_list.itervalues()
        else:
            resource = Response(
                Resource(),
                status_code=404,
                error="Driver not found for the resource type")
            return resource

        return []

    @wsexpose(Resource, six.text_type, body=Resource)
    def put(self, resource_id, resource):
        """Modify resource
        :resource param: graffiti.api.model.v1.resource.Resource
        """

        auth_token = pecan.request.headers.get('X-Auth-Token')
        endpoint_id = resource.provider.id

        if not resource.type:
            resource_type = self.default_resource_type
        else:
            resource_type = resource.type

        driver = driver_factory.get_driver(resource_type)
        if driver.resource:
            driver.resource.update_resource(
                resource_id,
                resource,
                auth_token,
                endpoint_id=endpoint_id
            )
        else:
            resource = Response(
                Resource(),
                status_code=404,
                error="Driver not found for the resource type"
            )

        return resource

    @wsexpose(Resource, body=Resource)
    def post(self, resource):
        auth_token = pecan.request.headers.get('X-Auth-Token')

        if not resource.type:
            resource_type = self.default_resource_type
        else:
            resource_type = resource.type

        driver = driver_factory.get_driver(resource_type)
        if driver.resource:
            resource = driver.resource.create_resource(resource, auth_token)

        return resource
