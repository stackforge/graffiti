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
from graffiti.api.plugins.glance_image import GlanceImage


from graffiti.api.model.v1.resource_dao_factory import \
    ResourceDAOFactory

from graffiti.common.utils import _

from oslo.config import cfg

import six

import keystoneclient.v2_0.client as ksclient


resource_controller_group = cfg.OptGroup('resource_controller')
resource_controller_opts = [
    cfg.StrOpt('type',
               help=_("The resource controller plugin"))
]

cfg.CONF.register_group(resource_controller_group)
cfg.CONF.register_opts(resource_controller_opts,
                       group=resource_controller_group)


class ResourceController(RestController):

    # TODO(Lakshmi): Lookup supported types from plugin registry
    local_resource_type = 'GFT:Local'
    glance_resource_type = 'OS::Glance:Image'

    def __init__(self):
        super(ResourceController, self).__init__()

        self.status = 200

        self._controller = self._load_controller('Local')

    def _load_controller(self, which_one):
        controller_type = cfg.CONF.resource_controller.type
        controller_type = controller_type if controller_type else 'Local'

        _controller = ResourceDAOFactory.create(controller_type)

        return _controller

    @wsexpose()
    def options(self):
        pass

    @wsexpose(Resource, six.text_type, six.text_type, six.text_type,
              six.text_type)
    def get_one(self, resource_id, resource_type=None, param1=None,
                param2=None):
        print "args:", resource_id, resource_type, param1, param2
        error_str = None
        if not resource_type:
            res = self._controller.get_resource(resource_id)
            return res
        elif resource_type.lower() == \
                ResourceController.glance_resource_type.lower():
            auth_token = pecan.request.headers.get('X-Auth-Token')
            endpoint_id = param1
            image_id = resource_id
            glance_public_url = None
            keystone = ksclient.Client(
                auth_url=cfg.CONF.keystone.auth_url,
                username=cfg.CONF.keystone.username,
                password=cfg.CONF.keystone.password,
                tenant_name=cfg.CONF.keystone.tenant_name)
            for endpoint in keystone.endpoints.list():
                if endpoint.id == endpoint_id:
                    glance_public_url = endpoint.publicurl

            # TODO(Lakshmi): Load plugins with plugin framework
            if auth_token and glance_public_url:
                glance_plugin = GlanceImage(
                    glance_public_url,
                    keystone.auth_token
                )
                res = glance_plugin.get_resource(image_id)
                if res:
                    return res
                else:
                    error_str = "Resource not found"
            else:
                error_str = "auth_token and/or endpointid not found"

        res = Response(Resource(), status_code=404, error=error_str)
        return res

    @wsexpose([Resource], six.text_type)
    def get_all(self, query_string=None):
        res_list = self._controller.find_resources(query_string)
        if res_list:
            return res_list.itervalues()

        return []

    @wsexpose(Resource, six.text_type, body=Resource)
    def put(self, resource_id, resource):
        """Modify resource
        :resource param: graffiti.api.model.v1.resource.Resource
        """
        resource_type = resource.type
        if not resource_type:
            resource_type = ResourceController.local_resource_type
        if resource_type.lower() == \
                ResourceController.local_resource_type.lower():
            self._controller.set_resource(
                resource_id,
                resource_definition=resource
            )
        elif resource_type.lower() == \
                ResourceController.glance_resource_type.lower():
            auth_token = pecan.request.headers.get('X-Auth-Token')
            endpoint_id = resource.provider.id
            glance_public_url = None
            keystone = ksclient.Client(
                auth_url=cfg.CONF.keystone.auth_url,
                username=cfg.CONF.keystone.username,
                password=cfg.CONF.keystone.password,
                tenant_name=cfg.CONF.keystone.tenant_name)
            for endpoint in keystone.endpoints.list():
                if endpoint.id == endpoint_id:
                    glance_public_url = endpoint.publicurl

            # TODO(Lakshmi): Load plugins with plugin framework
            if auth_token and glance_public_url:
                glance_plugin = GlanceImage(
                    glance_public_url,
                    keystone.auth_token
                )
                glance_plugin.update_resource(resource)
        return resource

    @wsexpose(Resource, body=Resource)
    def post(self, resource):

        id = resource.id if hasattr(resource, 'id') else None
        self._controller.set_resource(id, resource_definition=resource)

        return resource
