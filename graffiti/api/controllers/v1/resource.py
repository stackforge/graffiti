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

from graffiti.api.model.v1.resource_controller import LocalResourceController

from graffiti.common.utils import _

from oslo.config import cfg

import six


resource_controller_group = cfg.OptGroup('resource_controller')
resource_controller_opts = [
    cfg.StrOpt('type',
               help=_("The resource controller plugin"))
]

cfg.CONF.register_group(resource_controller_group)
cfg.CONF.register_opts(resource_controller_opts,
                       group=resource_controller_group)


class ResourceController(RestController):
    def __init__(self):
        super(ResourceController, self).__init__()

        self.status = 200

        self._controller = self._load_controller('Local')

    def _load_controller(self, which_one):
        controller_type = cfg.CONF.resource_controller.type
        controller_type = controller_type if controller_type else 'Local'

        # TODO(lakshmi): Load the controller here
        _controller = LocalResourceController()

        return _controller

    @wsexpose()
    def options():
        pass

    @wsexpose(Resource, six.text_type)
    def get_one(self, id):
        res = self._controller.get_resource(id)
        if res:
            return res

        res = Response(Resource(), status_code=404, error="Resource Not Found")
        return res

    @wsexpose([Resource], six.text_type)
    def get_all(self, query_string=None):

        res_list = self._controller.find_resources(query_string)
        if res_list:
            return res_list

        return []

    @wsexpose(Resource, six.text_type, body=Resource)
    def put(self, id, resource):

        self._controller.set_resource(id, resource_definition=resource)

        return resource

    @wsexpose(Resource, body=Resource)
    def post(self, resource):

        id = resource.id if hasattr(resource, 'id') else None
        self._controller.set_resource(id, resource_definition=resource)

        return resource
