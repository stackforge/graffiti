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

from pecan.rest import RestController

from wsme.api import Response
from wsmeext.pecan import wsexpose

from graffiti.api.model.v1.resource import Resource

import six

resources = []


class ResourceController(RestController):
    def __init__(self):
        super(ResourceController, self).__init__()

        self.status = 200

    @wsexpose()
    def options():
        pass

    @wsexpose(Resource, six.text_type)
    def get_one(self, id):
        global resources

        for res in resources:
            if res.id.lower() == id.lower():
                return res

        res = Response(Resource(), status_code=404, error="Resource Not Found")
        return res

    @wsexpose([Resource])
    def get_all(self):
        global resources

        return resources

    @wsexpose(Resource, Resource)
    def post(self, resource):
        global resources

        resources.append(resource)
