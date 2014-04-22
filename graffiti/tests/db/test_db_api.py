# Copyright (c) 2014 Mirantis Inc.
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
# limitations under the License.base.py

from graffiti.db import api as db_api
from graffiti.tests import base


class BaseDbTestCase(base.DbTestCase):
    def setUp(self):
        super(BaseDbTestCase, self).setUp()

    def _assert_saved_fields(self, expected, actual):
        for k in expected.keys():
            self.assertEqual(expected[k], actual[k])

    def _test_create(self, ref, save_method):
        saved = save_method(ref)

        self.assertIsNotNone(saved.name)
        self._assert_saved_fields(ref, saved)

    def _test_update_by_name(self, ref, delta, create, update):
        saved = create(ref)
        updated = update(saved.name, delta)

        self.assertEqual(saved.name, updated.name)
        self._assert_saved_fields(delta, updated)

    def _test_update_by_named_namespace(self, ref, delta, create, update):
        saved = create(ref)
        updated = update(saved.name, saved.namespace, delta)

        self.assertEqual(saved.name, updated.name)
        self.assertEqual(saved.namespace, updated.namespace)
        self._assert_saved_fields(delta, updated)


class NamespaceTest(BaseDbTestCase):

    def setUp(self):
        super(NamespaceTest, self).setUp()

        self.namespace_01 = {
            'name': u'OS:Glance',
            'scope': u'cloud',
            'owner': u'an-owner'
        }

        self.capability_type_rel = {
            'name': u'MySQL',
            'namespace': u'OS:Glance',
            'description': u'MySQL Capability Type description'
        }

    def test_create_namespace(self):
        self._test_create(self.namespace_01, db_api.namespace_create)

    def test_update_namespace(self):
        delta = {
            'scope': u'New Scope',
            'owner': u'New Owner'
        }
        self._test_update_by_name(self.namespace_01, delta,
                                  db_api.namespace_create,
                                  db_api.namespace_update)

    def test_delete_namespace(self):
        created = db_api.namespace_create(self.namespace_01)
        self.assertIsNotNone(created, "Could not create a Namespace.")
        db_api.namespace_delete(created.name)
        retrieved = db_api.namespace_get(created.name)
        self.assertIsNone(retrieved, "Created Namespace not deleted.")

    def test_cascade_delete_namespace(self):
        # Test deletion of namespace, cascade deletes related capability_types
        created_ns = db_api.namespace_create(self.namespace_01)
        self.assertIsNotNone(created_ns, "Could not create a Namespace.")

        # Assuming capability_type_##.namespace == namespace.name
        ct_01 = db_api.capability_type_create(self.capability_type_rel)
        self.assertIsNotNone(
            ct_01, "Could not create related capability_type")

        db_api.namespace_delete(created_ns.name)

        retrieved = db_api.namespace_get(created_ns.name)
        self.assertIsNone(retrieved, "Created Namespace not deleted.")

        retrieved = db_api.capability_type_get(ct_01.name, ct_01.namespace)
        self.assertIsNone(
            retrieved, "Associated Capability_Type not deleted.")


class CapabilityTypeTest(BaseDbTestCase):

    def setUp(self):
        super(CapabilityTypeTest, self).setUp()

        self.capability_type_01 = {
            'name': u'MySQL',
            'namespace': u'OS:Glance',
            'description': u'MySQL Capability Type description'
        }

        self.capability_type_02 = {
            'name': u'Apache2',
            'namespace': u'OS:Glance',
            'description': u'Apache2 Capability Type description'
        }

    def test_create_capability_type(self):
        self._test_create(self.capability_type_01,
                          db_api.capability_type_create)

    def test_update_capability_type(self):
        delta = {
            'description': u'New Description'
        }
        self._test_update_by_named_namespace(self.capability_type_01, delta,
                                             db_api.capability_type_create,
                                             db_api.capability_type_update)

    def test_delete_capability_type(self):
        created = db_api.capability_type_create(self.capability_type_01)
        self.assertIsNotNone(created, "Could not create a capability_type.")
        db_api.capability_type_delete(created.name, created.namespace)
        retrieved = db_api.capability_type_get(created.name, created.namespace)
        self.assertIsNone(retrieved, "Created capability_type not deleted.")
