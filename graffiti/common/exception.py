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


class GraffitiException(Exception):
    """Base Exception for the project

    To correctly use this class, inherit from it and define
    the 'message' property.
    """

    message = "An unknown exception occurred"

    def __str__(self):
        return self.message

    def __init__(self):
        super(GraffitiException, self).__init__(self.message)


class NotFound(GraffitiException):
    message = "Object not found"

    def __init__(self, message=None):
        if message:
            self.message = message


class DuplicateEntry(GraffitiException):
    message = "Database object already exists"

    def __init__(self, message=None):
        if message:
            self.message = message
