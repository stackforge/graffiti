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

import sys

from oslo.config import cfg


def prepare_service(argv=None):
    if argv is None:
        argv = sys.argv

    # when running unit tests, argv is inaccessible for some unknown
    # reason; need to revisit this logic again running under Apache2
    # TODO(lakshmi): figure this out
    try:
        cfg.CONF(argv[3:], project='graffiti')
    except BaseException:
        pass
