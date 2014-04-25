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


from graffiti.api.model.v1.dao.resource_dao import ResourceDAOBase


#TODO(Lakshmi): Implement db persistence for resource
class DBResourceDAO(ResourceDAOBase):

    def __init__(self, **kwargs):
        super(DBResourceDAO, self).__init__(**kwargs)
        self._type = "DBResourceDAO"

    def get_type(self):
        return self._type

    def get_resource(self, id):
        pass

    def find_resources(self, query_string):
        pass

    def set_resource(self, id=None, resource_definition=None):
        pass

    def delete_resource(self, id):
        pass
