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


from graffiti.common import exception

from oslo.config import cfg

from stevedore import dispatch

driver_opts = [
    cfg.ListOpt('enabled_drivers',
                default=['local', 'glance', 'nova'],
                help='List of drivers to enable. Missing drivers, or '
                     'drivers which can not be loaded will be '
                     'treated as a fatal exception.'),
]

CONF = cfg.CONF
CONF.register_opts(driver_opts)


def get_driver(resource_type):
    """Simple method to get a ref to an instance of a driver by the
    supported resource type.

    Driver loading is handled by the DriverFactory class. This method
    conveniently wraps that class and returns the actual driver object.

    :param resource_type: the resource type supported by a driver
    :returns: An instance of a class which implements
              graffiti.drivers.base.BaseResourceDriver
    :raises: DriverNotFound if the requested driver_name could not be
             found in the "graffiti.drivers" namespace.

    """

    try:
        factory = DriverFactory()
        print "resource types", factory.resource_types
        print "resource type", resource_type
        if resource_type in factory.resource_types.keys():
            driver_name = factory.resource_types[resource_type]
            return factory[driver_name].obj
        else:
            raise exception.DriverNotFoundForResourceType(
                resource_type=resource_type
            )

    except KeyError:
        raise exception.DriverNotFound(driver_name=driver_name)


def get_driver_by_name(driver_name):
    """Simple method to get a ref to an instance of a driver by the
    name.

    Driver loading is handled by the DriverFactory class. This method
    conveniently wraps that class and returns the actual driver object.

    :param driver_name: name of the registered driver
    :returns: An instance of a class which implements
              graffiti.drivers.base.BaseResourceDriver
    :raises: DriverNotFound if the requested driver_name could not be
             found in the "graffiti.drivers" namespace.

    """

    try:
        factory = DriverFactory()
        return factory[driver_name].obj
    except KeyError:
        raise exception.DriverNotFound(driver_name=driver_name)


def get_resource_types():
    """Returns a dictionary of resource type and driver name
    :returns:dictionary with resource type as key and driver name
            as its value
    """
    return DriverFactory()._resource_types


class DriverFactory(object):
    """Discover, load and manage the drivers available."""

    _driver_manager = None
    _resource_types = {}

    def __init__(self):
        if not DriverFactory._driver_manager:
            DriverFactory._init_driver_manager()
            print "Loaded drivers:", self.names

    def __getitem__(self, name):
        return self._driver_manager[name]

    @classmethod
    def _init_driver_manager(self):
        if self._driver_manager:
            return

        def _catch_driver_not_found(mgr, ep, exc):
            if (isinstance(exc, exception.DriverLoadError) and
                    ep.name not in CONF.enabled_drivers):
                return
            raise exc

        def _check_func(ext):
            return ext.name in CONF.enabled_drivers

        self._driver_manager = dispatch.NameDispatchExtensionManager(
            'graffiti.drivers',
            _check_func,
            invoke_on_load=True,
            on_load_failure_callback=_catch_driver_not_found
        )

        #Get supported resource types
        for driver_name in self._driver_manager.names():
            driver = self._driver_manager[driver_name].obj
            driver_resource_types = driver.get_resource_types()
            for type in driver_resource_types:
                self._resource_types[type] = driver_name

    @property
    def names(self):
        """The list of driver names available."""
        return self._driver_manager.names()

    @property
    def resource_types(self):
        """Returns all resource types supported by all the drivers
        :returns dictionary with resource type as key and driver name
        as its value
        """
        return self._resource_types
