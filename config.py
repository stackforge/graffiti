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

from oslo.config import cfg

from graffiti.common import driver_factory
from graffiti.common import utils

# Server Specific Configurations
server = {
    'port': '21075',
    'host': '0.0.0.0'
}

# Pecan Application Configurations
app = {
    'root': 'graffiti.api.controllers.root.RootController',
    'modules': ['graffiti.api'],
    'static_root': '%(confdir)s/public',
    'template_path': '%(confdir)s/graffiti/templates',
    'debug': False,
    'errors': {
        404: '/error/404',
        '__force_dict__': True
    }
}

logging = {
    'loggers': {
        'root': {'level': 'DEBUG', 'handlers': ['console']},
        'graffiti': {'level': 'DEBUG', 'handlers': ['console']},
        'wsme.api': {'level': 'DEBUG', 'handlers': ['console']},
        'py.warnings': {'handlers': ['console']},
        '__force_dict__': True
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'formatters': {
        'simple': {
            'format': ('%(asctime)s %(levelname)-5.5s [%(name)s]'
                       '[%(threadName)s] %(message)s')
        }
    }
}

wsme = {
    'debug': True
}


# Custom Configurations must be in Python dictionary format::
#
# foo = {'bar':'baz'}
#
# All configurations are accessible at::
# pecan.conf

# oslo config
keystone_group = cfg.OptGroup('keystone')
keystone_opts = [
    cfg.StrOpt('auth_url',
               default='http://127.0.0.1:5000/v2.0',
               help='keystone authorization url'),
    cfg.StrOpt('username',
               default='admin',
               help='keystone username'),
    cfg.StrOpt('password',
               default='secretword',
               help='keystone password'),
    cfg.StrOpt('tenant_name',
               default='admin',
               help='keystone tenant name')

]
cfg.CONF.register_group(keystone_group)
cfg.CONF.register_opts(keystone_opts, group=keystone_group)

# DEFAULT group
default_group = cfg.OptGroup('DEFAULT')
default_opts = [
    cfg.StrOpt(
        'persistence_type',
        default="memory",
        help=("persistence options. "
              "values = 'memory' or 'file' or 'db"))
]

cfg.CONF.register_group(default_group)
cfg.CONF.register_opts(default_opts,
                       group=default_group)

# FILE_PERSISTENCE group
file_group = cfg.OptGroup('FILE_PERSISTENCE')
file_opts = [
    cfg.StrOpt(
        'dictionary_folder',
        default="/tmp/graffiti-dictionary/",
        help=("Absolute path of the file for persisting dictionary")
    )
]

cfg.CONF.register_group(file_group)
cfg.CONF.register_opts(file_opts,
                       group=file_group)


# Used for remote debugging, like pychcharms or pydev
#  To enable remote debugging in pycharms, requires that you put the
#  pycharm-debug.egg in the python path. E.g.
#
# Include the pycharm-debug.egg archive.
# e.g. /home/<USERNAME>/pycharm-3.1.1/pycharm-debug.egg
# You can do it in a number of ways, for example:
#   Add the archive to PYTHONPATH.e,g,
#      export PYTHONPATH+=.:/home/<USERNAME>/pycharm-3.1.1/pycharm-debug.egg
#   Append the archive to sys.path. e.g.
#      import sys
#      sys.path.append('/home/<USERNANE>/pycharm-3.1.1/pycharm-debug.egg')
#   Just copy the pydev from the archive to the directory where your remote
#   script resides.
#
# You will need to setup a debug configuration in your pycharms and start the
# debugger BEFORE starting pecan
# This is because the following code connects from here to your pycharms
# (or your pydev)
pydevd = {
    'enabled': False,
    'port': 22075,
    'bindhost': 'localhost'
}


# Discover and load drivers
df = driver_factory.DriverFactory()

# Load Out of the box Dictionary
#specify url kwarg to load from URL.  Or load from file system
utils.load_dictionary(url='http://localhost:21071/1/capability_type/all/')
#utils.load_dictionary()
