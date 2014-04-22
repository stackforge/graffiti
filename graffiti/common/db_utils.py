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

# look at heat/openstack/common/gettextutils.py when we actually need
# to implement this method


from wsme import types as wtypes


class DbTransformer():

    @classmethod
    def to_model(model, db_entity):
        # Transform a db_entity to model object
        db_items = db_entity.as_dict().items()
        items = dict((key, value) for key, value in db_items)
        return model(**items)

    def to_dict(self):
        # Return the wsme_attributes names:values as a dict
        names = []
        for attribute in self._wsme_attributes:
            names.append(attribute.name)

        values = {}
        for name in names:
            value = getattr(self, name)
            if value == wtypes.Unset:
                value = None
            values.update({name: value})
        return values
