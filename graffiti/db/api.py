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

# import copy
from oslo.config import cfg

from graffiti.api.model.v1.derived_type import DerivedType
from graffiti.common import exception as exc
from graffiti.db import models
from graffiti.openstack.common.db import exception as db_exc
from graffiti.openstack.common.db.sqlalchemy import session as db_session

CONF = cfg.CONF
CONF.import_group("database", "graffiti.openstack.common.db.options")
_FACADE = None

BASE = models.Base


def setup_db():
    try:
        engine = get_engine()
        BASE.metadata.create_all(engine)
    except Exception:
        return False
    return True


def drop_db():
    try:
        BASE.metadata.drop_all(get_engine())
    except Exception:
        return False
    return True


def _get_facade_instance():
    """Generate an instance of the DB Facade.
    """
    global _FACADE
    if _FACADE is None:
        if CONF.database.connection is None:
            print("Warning: [database] connection not configured.")
        _FACADE = db_session.EngineFacade(
            CONF.database.connection,
            **dict(CONF.database.iteritems()))
    return _FACADE


def _destroy_facade_instance():
    """Destroys the db facade instance currently in use.
    """
    global _FACADE
    _FACADE = None


def get_engine():
    """Returns the global instance of our database engine.
    """
    facade = _get_facade_instance()
    return facade.get_engine()


def get_session(autocommit=True, expire_on_commit=False):
    """Returns a database session from our facade.
    """
    facade = _get_facade_instance()
    return facade.get_session(autocommit=autocommit,
                              expire_on_commit=expire_on_commit)


def cleanup():
    """Manually clean up our database engine.
    """
    _destroy_facade_instance()


def model_query(model, session=None):
    """Query helper.

    :param model: base model to query
    """
    session = session or get_session()
    query = session.query(model)
    return query


def __entity_get_by_name(kls, entity_name, session):
    query = model_query(kls, session)
    return query.filter_by(name=entity_name).first()


def __entity_get_by_name_namespace(kls, entity_name, entity_namespace,
                                   session):
    query = model_query(kls, session)
    return query.filter_by(name=entity_name,
                           namespace=entity_namespace).first()


def _entity_get_all(kls, **kwargs):
    kwargs = dict((k, v) for k, v in kwargs.iteritems() if v)

    query = model_query(kls)
    entities = query.filter_by(**kwargs).all()

    return entities


def named_entity_update(kls, entity_name, values):
    session = get_session()

    with session.begin():
        entity = __entity_get_by_name(kls, entity_name, session)
        if entity is None:
            raise exc.NotFound("%s %s not found" % (kls.__name__, entity_name))

        entity.update(values.copy())
        session.add(entity)

    return entity


def named_namespace_entity_update(kls, entity_name, entity_namespace, values):
    session = get_session()

    with session.begin():
        entity = __entity_get_by_name_namespace(kls, entity_name,
                                                entity_namespace, session)
        if entity is None:
            raise exc.NotFound(
                "%s %s %s not found" % (kls.__name__, entity_namespace,
                                        entity_name))

        entity.update(values.copy())
        session.add(entity)

    return entity


# BEGIN Namespace
def namespace_get(name):
    query = model_query(models.Namespace, get_session())
    return query.filter_by(name=name).first()


def namespace_get_all():
    return _entity_get_all(models.Namespace)


def namespace_create(values):
    namespace = models.Namespace()
    namespace.update(values.copy())

    session = get_session()
    with session.begin():
        try:
            namespace.save(session=session)
        except db_exc.DBDuplicateEntry as e:
            raise exc.DuplicateEntry("Duplicate entry for Namespace: %s"
                                     % e.columns)

    return namespace


def namespace_update(name, values):
    return named_entity_update(models.Namespace, name, values)


def namespace_delete(name):
    namespace = namespace_get(name)

    if namespace:
        session = get_session()
        with session.begin():
            session.delete(namespace)


# BEGIN CapabilityType
def capability_type_get(name, namespace):
    query = model_query(models.CapabilityType, get_session())
    return query.filter_by(name=name, namespace=namespace).first()


def capability_type_get_with_derived_properties(name, namespace):
    cap_type_prop_dict = dict()
    db_capability_type = capability_type_get(name, namespace)
    if db_capability_type.parent_name and db_capability_type.parent_namespace:
        property_dict = dict()
        property_dict = __get_derived_properties(
            db_capability_type.parent_name,
            db_capability_type.parent_namespace,
            property_dict
        )
        cap_type_prop_dict['derived_properties'] = property_dict

    cap_type_prop_dict['cap_type'] = db_capability_type
    return cap_type_prop_dict


def __get_derived_properties(name, namespace, property_dict):
    db_capability_type = capability_type_get(name, namespace)
    properties_text = db_capability_type.properties_text
    if properties_text:
        derived_type = DerivedType()
        derived_type.name = name
        derived_type.namespace = namespace
        property_dict[derived_type] = properties_text

    if db_capability_type.parent_name and db_capability_type.parent_namespace:
        __get_derived_properties(
            db_capability_type.parent_name,
            db_capability_type.parent_namespace,
            property_dict
        )

    return property_dict


def capability_type_get_all():
    return _entity_get_all(models.CapabilityType)


def capability_type_create(values):
    capability_type = models.CapabilityType()
    capability_type.update(values.copy())

    session = get_session()
    with session.begin():
        try:
            capability_type.save(session=session)
        except db_exc.DBDuplicateEntry as e:
            raise exc.DuplicateEntry("Duplicate entry for CapabilityType: %s"
                                     % e.columns)

    return capability_type


def capability_type_update(name, namespace, values):
    return named_namespace_entity_update(models.CapabilityType,
                                         name, namespace, values)


def capability_type_delete(name, namespace):
    capability_type = capability_type_get(name, namespace)

    if capability_type:
        session = get_session()
        with session.begin():
            session.delete(capability_type)
