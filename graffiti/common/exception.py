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

from graffiti.openstack.common.gettextutils import _


class GraffitiException(Exception):
    """Base Exception for the project

    To correctly use this class, inherit from it and define
    the 'message' property.
    That message will get printf'd
    with the keyword arguments provided to the constructor.
    """

    message = _("An unknown exception occurred")

    def __str__(self):
        return self.message

    def __init__(self, **kwargs):
        self.kwargs = kwargs

        try:
            message = self.message % kwargs
        except KeyError:
            #TODO(Any): print to log
            pass

        super(GraffitiException, self).__init__(message)


class NotFound(GraffitiException):
    message = _("Object not found")


class DuplicateEntry(GraffitiException):
    message = _("Database object already exists")


class DriverNotFound(NotFound):
    message = _("Failed to load driver %(driver_name)s.")


class DriverLoadError(GraffitiException):
    message = _("Driver %(driver)s could not be loaded. Reason: %(reason)s.")


class MethodNotSupported(GraffitiException):
    message = _("Method %(method)s is not supported by this driver")


class DriverNotFoundForResourceType(NotFound):
    message = _("Cannot find a registered driver for the resource "
                "type %(resource_type)s")
