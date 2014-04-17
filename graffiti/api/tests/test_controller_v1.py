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

from graffiti.api.controllers.v1.captype_controller_factory \
    import CapTypeControllerFactory
from graffiti.api.controllers.v1.ns_controller_factory \
    import NSControllerFactory
from graffiti.api.model.v1.resource_dao_factory \
    import ResourceDAOFactory


class TestControllerV1(base.TestCase):

    def test_v1_exists(self):
        root = RootController()
        self.assertIn(hasattr(root, 'v1'), [True])

    def test_v1_namespace_exists(self):
        v1 = V1Controller()
        self.assertIn(hasattr(v1, 'namespace'), [True])

    def test_v1_namespace_controller_factory__memory(self):
        rc = NSControllerFactory.create('memory')
        self.assertEquals(rc.get_type(), 'MemNSController')

    # TODO(Lakshmi): Create folder before any tests run
    # def test_v1_namespace_controller_factory__file(self):
    #    rc = NSControllerFactory.create('file')
    #    self.assertEquals(rc.get_type(), 'FileNSController')

    def test_v1_namespace_controller_factory__db(self):
        rc = NSControllerFactory.create('db')
        self.assertEquals(rc.get_type(), 'DBNSController')

    def test_v1_capability_type_exists(self):
        v1 = V1Controller()
        self.assertIn(hasattr(v1, 'capability_type'), [True])

    def test_v1_capability_type_controller_factory__memory(self):
        rc = CapTypeControllerFactory.create('memory')
        self.assertEquals(rc.get_type(), 'MemCapabilityTypeController')

    # TODO(Lakshmi): Create folder before any tests run
    # def test_v1_capability_type_controller_factory__file(self):
    #    rc = CapTypeControllerFactory.create('file')
    #    self.assertEquals(rc.get_type(), 'FileCapabilityTypeController')

    def test_v1_capability_type_controller_factory__db(self):
        rc = CapTypeControllerFactory.create('db')
        self.assertEquals(rc.get_type(), 'DBCapabilityTypeController')

    def test_v1_resource_exists(self):
        v1 = V1Controller()
        self.assertIn(hasattr(v1, 'resource'), [True])

    def test_v1_resource_controller_factory__local(self):
        rc = ResourceDAOFactory.create('local')
        self.assertEquals(rc.get_type(), 'LocalResourceDAO')

    def test_v1_resource_controller_factory__unknown(self):
        rc = ResourceDAOFactory.create('invalid_controller')
        self.assertTrue(rc is None)
