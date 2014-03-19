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
test_controller_v1
----------------------------------

Tests for `graffiti` module.
"""

from graffiti.api.tests import base

from graffiti.api.controllers.root import RootController
from graffiti.api.controllers.versions import V1Controller

from graffiti.api.model.v1.resource_controller_factory \
    import ResourceControllerFactory


class TestControllerV1(base.TestCase):

    def test_v1_exists(self):
        root = RootController()
        self.assertIn(hasattr(root, 'v1'), [True])

    def test_v1_resource_exists(self):
        v1 = V1Controller()
        self.assertIn(hasattr(v1, 'resource'), [True])

    def test_v1_resource_controller_factory__local(self):
        rc = ResourceControllerFactory.create('local')
        self.assertEquals(rc.get_type(), 'LocalResourceController')

    def test_v1_resource_controller_factory__unknown(self):
        rc = ResourceControllerFactory.create('invalid_controller')
        self.assertTrue(rc is None)
