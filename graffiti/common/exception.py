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

from graffiti.openstack.common.gettextutils import _
from graffiti.openstack.common.log import logging

_FATAL_EXCEPTION_FORMAT_ERRORS = False

logger = logging.getLogger(__name__)


class GraffitiException(Exception):
    """Base Graffiti Exception

    To correctly use this class, inherit from it and define
    a 'msg_fmt' property. That msg_fmt will get printf'd
    with the keyword arguments provided to the constructor.

    """
    message = _("An unknown exception occurred.")

    def __str__(self):
        return self.message

    def __init__(self, **kwargs):
        self.kwargs = kwargs

        try:
            self.message = self.msg_fmt % kwargs
        except KeyError:
            exc_info = sys.exc_info()
            #kwargs doesn't match a variable in the message
            #log the issue and the kwargs
            logger.exception(_('Exception in string format operation'))
            for name, value in kwargs.iteritems():
                logger.error("%s: %s" % (name, value))

            if _FATAL_EXCEPTION_FORMAT_ERRORS:
                raise exc_info[0], exc_info[1], exc_info[2]

    #def __str__(self):
    #    return unicode(self.message).encode('UTF-8')

    def __unicode__(self):
        return unicode(self.message)

    def __deepcopy__(self, memo):
        return self.__class__(**self.kwargs)


class NotFound(GraffitiException):
    msg_fmt = _("Object not found")


class DuplicateEntry(GraffitiException):
    msg_fmt = _("Database object already exists")


class DriverNotFound(NotFound):
    msg_fmt = _("Failed to load driver %(driver_name)s.")


class DriverLoadError(GraffitiException):
    msg_fmt = _("Driver %(driver)s could not be loaded. Reason: %(reason)s.")


class MethodNotSupported(GraffitiException):
    msg_fmt = _("Method %(method)s is not supported by this driver")


class DriverNotFoundForResourceType(NotFound):
    msg_fmt = _("Cannot find a registered driver for the resource "
                "type %(resource_type)s")
