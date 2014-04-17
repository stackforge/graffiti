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

from pecan import make_app

from graffiti.api import model
from graffiti.api.service import prepare_service

from graffiti.api.hooks import CorsHook

from oslo.config import cfg
CONF = cfg.CONF


def setup_app(config):

    if hasattr(config, 'pydevd') and config.pydevd.enabled:
        try:
            print(
                'Remote debug set to true(config.pydevd).  '
                'Attempting connection'
            )
            import pydevd
            pydevd.settrace(
                config.pydevd.bindhost,
                port=config.pydevd.port,
                stdoutToServer=True,
                stderrToServer=True,
                suspend=False)
        except Exception as e:
            print "Debug Connection Error:", e

    model.init_model()
    app_conf = dict(config.app)

    prepare_service()

    app_hooks = [CorsHook()]

    return make_app(
        app_conf.pop('root'),
        logging=getattr(config, 'logging', {}),
        hooks=app_hooks,
        **app_conf
    )
