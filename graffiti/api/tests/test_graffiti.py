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
import json

from graffiti.api.tests import pecan_base

TEST_DATA_FILE = "graffiti/api/tests/samples/resource_2014-1.json"


def get_resource_list():
    json_data_file = open(TEST_DATA_FILE)
    json_data = json_data_file.read()
    json_data_file.close()
    resource_list_json = json.loads(json_data)['resource_list']
    return resource_list_json


class TestGraffiti(pecan_base.TestCase):

    def test_get_all_empty(self):
        response = self.get_json('/resource')
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json, [])

    def test_post(self):
        standard_resource_json = get_resource_list()[0]
        response = self.post_json('/resource', params=standard_resource_json)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json, standard_resource_json)

    def test_get_one(self):
        standard_resource_json = get_resource_list()[0]
        self.post_json('/resource', params=standard_resource_json)
        response = self.get_json('/resource/%s' % standard_resource_json['id'])
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json, standard_resource_json)

    def test_put(self):
        standard_resource_json = get_resource_list()[0]
        self.post_json('/resource', params=standard_resource_json)
        standard_resource_json['name'] = 'RENAMED'
        response = self.put_json('/resource/%s' % standard_resource_json['id'],
                                 params=standard_resource_json)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json, standard_resource_json)
