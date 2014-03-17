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

#import json

from pecan.hooks import PecanHook


class CorsHook(PecanHook):
    def after(self, state):
        state.response.headers['Access-Control-Allow-Origin'] = '*'
        state.response.headers['Access-Control-Allow-Methods'] = \
            'GET, PUT, POST, DELETE, OPTIONS'
        state.response.headers['Access-Control-Allow-Headers'] = \
            'origin, authorization, accept, content-type'

        if not state.response.headers['Content-Length']:
            state.response.headers['Content-Length'] = \
                str(len(state.response.body))

        # TODO(lakshmi): this fails in Python 3.3, don't know why
#        if state.response.headers['Content-Type'].find('json') != -1:
            # Sort the Response Body's JSON
#            json_str = json.loads(state.response.body)
#            state.response.body = json.dumps(json_str, sort_keys=True)
