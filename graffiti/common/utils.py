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

import glob
import json
import os

from graffiti.api.model.v1.derived_type import DerivedType


DICTIONARY_DATA_FOLDER = "etc/dictionary"
NAMESPACE_STRING = "Namespace*"
CAPABILITY_TYPE_STRING = "CapabilityType*"

__namespace_resource_type_dict = dict()
__namespace_property_format_dict = dict()

__namespace_dict = dict()
__property_dict = dict()

TAG_IDENTIFIER = "_TAG"


# TODO(travis): need localization strategy
def _(msg):
    return msg


def load_dictionary():
    cur_dir = os.getcwd()
    os.chdir(DICTIONARY_DATA_FOLDER)

    for namespace_file in glob.glob(NAMESPACE_STRING):
        print "Loading Namespace file: %s" % namespace_file
        load_namespace(namespace_file)

    for cap_type_file in glob.glob(CAPABILITY_TYPE_STRING):
        print "Loading Capability type file: %s" % cap_type_file
        load_capability_type(cap_type_file)

    os.chdir(cur_dir)


def load_namespace(namespacefile):
    with open(namespacefile) as json_file:
        json_data = json.load(json_file)
        #print(json_data)

        for namespace in json_data:
            __namespace_resource_type_dict[namespace['namespace']] = \
                namespace['resource_types']
            __namespace_property_format_dict[namespace['namespace']] = \
                namespace['property_format']


def load_capability_type(cap_type_file):
    with open(cap_type_file) as json_file:
        json_data = json.load(json_file)
        for cap_type in json_data['capability_type_list']:
            derived_type = DerivedType()
            derived_type.name = cap_type['name']
            derived_type.namespace = cap_type['namespace']

            key_names = []
            for key in cap_type['properties'].keys():
                property_name = key
                if cap_type['properties'][key]['type'] == "choice":
                    #Property name and item in each choice as key
                    for item in cap_type['properties'][key]['items']:
                        dict_key = property_name + item
                        key_names.append(dict_key)
                else:
                    if 'defaultValue' in cap_type['properties'][key].keys():
                        #Property name and default value as key
                        dict_key = property_name + \
                            str(cap_type['properties'][key]
                                ['defaultValue'])
                        key_names.append(dict_key)
                    else:
                        #Just use the property name as key
                        dict_key = property_name
                        key_names.append(dict_key)

            property_dict = dict()
            if derived_type.namespace in __namespace_dict.keys():
                property_dict = __namespace_dict[derived_type.namespace]

            for key in key_names:
                property_dict[key] = derived_type

            #Add capability itself as property - behaves as a TAG
            tag_name = cap_type['name'] + TAG_IDENTIFIER
            property_dict[tag_name] = derived_type

            __namespace_dict[derived_type.namespace] = property_dict


def get_namespace_resource_type_dict():
    return __namespace_resource_type_dict


def get_namespace_property_format_dict():
    return __namespace_property_format_dict


def get_qualifier(property_name, property_value):
    if property_value:
        key1 = property_name + property_value
        key2 = property_name
    else:
        key1 = property_name

    #First loop. Make sure key1 is not found anywhere
    for namespace in __namespace_dict.keys():
        property_dict = __namespace_dict[namespace]
        if key1 in property_dict.keys():
            return property_dict[key1]

    if property_value:
        #Second loop. If not found first, use key2
        for namespace in __namespace_dict.keys():
            property_dict = __namespace_dict[namespace]
            if key2 in property_dict.keys():
                return property_dict[key2]

    return None
