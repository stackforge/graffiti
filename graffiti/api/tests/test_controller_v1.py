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

from graffiti.api.model.v1.dao.captype_dao_factory \
    import CapabilityTypeDAOFactory
from graffiti.api.model.v1.dao.ns_dao_factory \
    import NSDAOFactory
from graffiti.api.model.v1.dao.resource_dao_factory \
    import ResourceDAOFactory


class TestControllerV1(base.TestCase):

    def test_v1_exists(self):
        root = RootController()
        self.assertIn(hasattr(root, 'v1'), [True])

    def test_v1_namespace_exists(self):
        v1 = V1Controller()
        self.assertIn(hasattr(v1, 'namespace'), [True])

    def test_v1_namespace_controller_factory__memory(self):
        rc = NSDAOFactory.create('memory')
        self.assertEquals(rc.get_type(), 'MemNSDAO')

    # TODO(Lakshmi): Create folder before any tests run
    # def test_v1_namespace_controller_factory__file(self):
    #    rc = NSControllerFactory.create('file')
    #    self.assertEquals(rc.get_type(), 'FileNSDAO')

    def test_v1_namespace_controller_factory__db(self):
        rc = NSDAOFactory.create('db')
        self.assertEquals(rc.get_type(), 'DBNSDAO')

    def test_v1_capability_type_exists(self):
        v1 = V1Controller()
        self.assertIn(hasattr(v1, 'capability_type'), [True])

    def test_v1_capability_type_dao_factory__memory(self):
        rc = CapabilityTypeDAOFactory.create('memory')
        self.assertEquals(rc.get_type(), 'MemCapabilityTypeDAO')

    # TODO(Lakshmi): Create folder before any tests run
    # def test_v1_capability_type_dao_factory__file(self):
    #    rc = CapabilityTypeDAOFactory.create('file')
    #    self.assertEquals(rc.get_type(), 'FileCapabilityTypeDAO')

    def test_v1_capability_type_dao_factory__db(self):
        rc = CapabilityTypeDAOFactory.create('db')
        self.assertEquals(rc.get_type(), 'DBCapabilityTypeDAO')

    def test_v1_resource_exists(self):
        v1 = V1Controller()
        self.assertIn(hasattr(v1, 'resource'), [True])

    def test_v1_resource_dao_factory__memory(self):
        rc = ResourceDAOFactory.create('memory')
        self.assertEquals(rc.get_type(), 'MemResourceDAO')

    def test_v1_resource_dao_factory__file(self):
        rc = ResourceDAOFactory.create('file')
        self.assertEquals(rc.get_type(), 'FileResourceDAO')

    def test_v1_resource_dao_factory__db(self):
        rc = ResourceDAOFactory.create('db')
        self.assertEquals(rc.get_type(), 'DBResourceDAO')

    def test_v1_resource_controller_factory__unknown(self):
        rc = ResourceDAOFactory.create('invalid_controller')
        self.assertTrue(rc is None)
