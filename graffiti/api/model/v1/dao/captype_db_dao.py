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

from graffiti.api.model.v1.capability_type import CapabilityType
from graffiti.api.model.v1.dao.captype_dao import CapabilityTypeDAOBase
from graffiti.api.model.v1.derived_type import DerivedType
from graffiti.api.model.v1.property_type import PropertyType
from graffiti.db import api as dbapi
import json
from wsme.rest.json import fromjson
from wsme.rest.json import tojson


class DBCapabilityTypeDAO(CapabilityTypeDAOBase):

    def __init__(self, **kwargs):
        super(DBCapabilityTypeDAO, self).__init__(**kwargs)
        self._type = "DBCapabilityTypeDAO"

    def get_type(self):
        return self._type

    def _to_model(self, db_captype):
        model_captype = CapabilityType.to_model(db_captype)
        if db_captype.parent_name == 'null':
            model_captype.derived_from = None
        else:
            model_captype.derived_from = DerivedType(
                name=db_captype.parent_name,
                namespace=db_captype.parent_namespace)

        property_types = {}
        db_properties = json.loads(db_captype.properties_text)
        for id in db_properties:
            property_types[id] = fromjson(PropertyType, db_properties[id])
        model_captype.properties = property_types

        return model_captype

    def _to_dict(self, model_captype):
        captype_dict = model_captype.to_dict()

        properties = model_captype.properties
        db_property_types = {}
        if properties:
            for k, v in properties.items():
                json_data = tojson(PropertyType, v)
                db_property_types[k] = json_data
        captype_dict['properties_text'] = json.dumps(db_property_types)

        derived_from = model_captype.derived_from
        if derived_from:
            captype_dict["parent_name"] = model_captype.derived_from.name
            captype_dict["parent_namespace"] =\
                model_captype.derived_from.namespace

        return captype_dict

    def get_capability_type(self, name, namespace):
        db_capability_type = dbapi.capability_type_get(name, namespace)
        if not db_capability_type:
            res = CapabilityType(CapabilityType(), status_code=404,
                                 error="CapabilityType Not Found")
            return res

        return self._to_model(db_capability_type)

    def find_capability_types(self, query_string):
        # TODO(wko): add support for query_string
        db_capability_types = dbapi.capability_type_get_all()
        capability_types = []
        for db_ct in db_capability_types:
            capability_types.append(self._to_model(db_ct))
        return capability_types

    def set_capability_type(self, capability_type=None):
        created_capability_type = dbapi.capability_type_create(
            self._to_dict(capability_type))
        return self._to_model(created_capability_type)

    def put_capability_type(self, name, namespace, capability_type=None):
        # Update a Capability Type
        if capability_type:
            db_capability_type = dbapi.capability_type_update(
                name, namespace, self._to_dict(capability_type))
            return self._to_model(db_capability_type)

    def delete_capability_type(self, name, namespace):
        db_capability_type = dbapi.capability_type_get(name, namespace)
        if db_capability_type:
            dbapi.capability_type_delete(name, namespace)
            return self._to_model(db_capability_type)
