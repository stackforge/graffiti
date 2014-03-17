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
test_graffiti
----------------------------------

Tests for `graffiti` module.
"""
from graffiti.api.tests import pecan_base


class TestGraffiti(pecan_base.TestCase):

    def test_get_all(self):
        response = self.get_json('/resource')
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, 'application/json')

    def test_post(self):
        resource_json = {
            "name": "Cirros",
            "id": "0000-0000-0000-0000",
            "description": "Some Image",
            "provider": {
                "id": "1111-1111-1111-1111"
            },
            "capabilities": [
                {
                    "capability_type": "MySQL",
                    "capability_type_namespace": "TestNamespace",
                    "properties": [
                        {
                            "name": "CPU",
                            "value": "4"
                        },
                        {
                            "name": "RAM",
                            "value": "4GB"
                        }
                    ]
                }
            ],
            "properties": [
                {
                    "name": "os",
                    "value": "ubuntu"
                },
                {
                    "name": "os_version",
                    "value": "12.04"
                }
            ],
            "requirements": [
                {
                    "capability_type": "Apache",
                    "capability_type_namespace": "TestNamespace",
                    "criterion": "Wayne !SLEEPING"
                }
            ],
            "type": "OS::Image"}

        response = self.post_json('/resource', params=resource_json)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, 'application/json')
