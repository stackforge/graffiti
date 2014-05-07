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

import json

import pecan
from pecan.rest import RestController


from wsme.api import Response
from wsme.rest.json import fromjson
from wsmeext.pecan import wsexpose


from graffiti.api.model.v1.resource import Resource
from graffiti.api.model.v1.resource_query import ResourceQuery
from graffiti.common import driver_factory
from graffiti.common.exception import DriverNotFound
from graffiti.common.exception import DriverNotFoundForResourceType

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
                resource_type,
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
        print "args: resource_type=%s, query_string=%s" % \
              (resource_type, query_string)
        auth_token = pecan.request.headers.get('X-Auth-Token')

        resource_types = []
        if query_string:
            doc = json.loads(query_string)
            resource_query = fromjson(ResourceQuery, doc)
            resource_types = resource_query.resource_types
        else:
            if not resource_type:
                resource_types.append(self.default_resource_type)

        driver_resources = ResourceController.__group_resource_types_by_driver(
            driver_factory.get_resource_types(),
            resource_types
        )

        all_resource_list = []
        for driver_name in driver_resources.keys():
            req_resource_types = driver_resources[driver_name]
            resource_query = ResourceQuery()
            resource_query.resource_types = req_resource_types
            try:
                print "Invoking driver(%s) for resource types(%s):" % \
                      (driver_name, req_resource_types)
                driver = driver_factory.get_driver_by_name(driver_name)
            except DriverNotFound:
                resource = Response(
                    Resource(),
                    status_code=404,
                    error="Driver not found for the resource type")
                return resource

            if driver.resource:
                res_list = driver.resource.find_resources(
                    resource_query,
                    auth_token
                )
                if res_list:
                    all_resource_list += res_list.values()

        if all_resource_list:
            return all_resource_list

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
                resource_type,
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
            resource = driver.resource.create_resource(
                resource_type,
                resource,
                auth_token
            )

        return resource

    @staticmethod
    def __group_resource_types_by_driver(
            all_resource_types,
            request_resource_types):
        driver_resource_types = dict()
        for resource_type in request_resource_types:

            if resource_type in all_resource_types.keys():
                driver_name = all_resource_types[resource_type]
            else:
                raise DriverNotFoundForResourceType(
                    resource_type=resource_type
                )

            resource_list = []
            if driver_name in driver_resource_types.keys():
                resource_list = driver_resource_types[driver_name]
                if not resource_list:
                    resource_list = []
                resource_list.append(resource_type)
                driver_resource_types[driver_name] = resource_list
            else:
                resource_list.append(resource_type)
                driver_resource_types[driver_name] = resource_list

        return driver_resource_types
