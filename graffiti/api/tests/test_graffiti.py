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
import os

import pecan
import pecan.testing

from oslo.config import cfg

from graffiti.api.tests import base


class TestGraffiti(base.TestCase):

    PATH_PREFIX = '/v1'

    def setUp(self):
        super(TestGraffiti, self).setUp()
        self.app = self._make_app()
        cfg.CONF.set_override(name='type', override='Local',
                              group='resource_controller')

    def _make_app(self):
        root_dir = self.path_get()
        self.config = {
            'app': {
                'root': 'graffiti.api.controllers.root.RootController',
                'modules': ['graffiti.api'],
                'template_path': '%s/graffiti/templates' % root_dir,
            },
        }

        return pecan.testing.load_test_app(self.config)

    def tearDown(self):
        super(TestGraffiti, self).tearDown()
        pecan.set_config({}, overwrite=True)

    def path_get(self, project_file=None):
        root = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            '..',
                                            '..', ))
        if project_file:
            return os.path.join(root, project_file)
        else:
            return root

    def get_json(self, path, expect_errors=False, headers=None,
                 extra_environ=None, q=[], **params):
        full_path = self.PATH_PREFIX + path
        query_params = {'q.field': [],
                        'q.value': [],
                        'q.op': [], }
        for query in q:
            for name in ['field', 'op', 'value']:
                query_params['q.%s' % name].append(query.get(name, ''))

        all_params = {}
        all_params.update(params)
        if q:
            all_params.update(query_params)

        response = self.app.get(full_path,
                                params=all_params,
                                headers=headers,
                                extra_environ=extra_environ,
                                expect_errors=expect_errors)

        if not expect_errors:
            response = response

        return response

    def test_get_all(self):
        response = self.get_json('/resource')
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, 'application/json')
