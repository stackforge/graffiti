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

from datetime import datetime
from glanceclient import Client as glance_client
from os import environ as env
import random
import uuid

import keystoneclient.v2_0.client as keystone_client


class MockGlanceImage(object):

    IMAGE_OS_DISTROS = ['arch', 'centos', 'debian', 'fedora', 'freebsd',
                        'gentoo', 'netbsd', 'openbsd', 'opensuse', 'rhel',
                        'sled', 'ubuntu', 'windows']
    # TODO(wko): Find Versions
    # 'mandrake', 'mandriva', 'mes', 'msdos', 'netware',
    # 'opensolaris',

    ARCH_VERSIONS = ['rolling']

    CENTOS_VERSIONS = ['5.1', '5.2', '5.3', '5.5', '5.6', '6.0', '6.1',
                       '6.2', '6.3', '6.4', '6.5']

    DEBIAN_VERSIONS = ['5', '6', '7']

    FEDORA_VERSIONS = ['17', '18', '19', '20']

    FREEBSD_VERSIONS = ['7.0', '7.1', '7.2', '7.3', '7.4', '8.0', '8.1',
                        '8.2', '8.3', '8.4', '9.0', '9.1', '9.2', '10.0']

    GENTOO_VERSIONS = ['rolling']

    NETBSD_VERSIONS = ['4.0', '5.0', '6.0', '6.1']

    OPENSUSE_VERSIONS = ['11.1', '11.2', '11.3', '11.4', '12.1',
                         '12.2', '12.3', '13.1']

    OPENBSD_VERSIONS = ['4.0', '4.1', '4.2', '4.3', '4.4', '4.5', '4.6',
                        '4.7', '4.8', '4.9', '5.0', '5.1', '5.2', '5.3',
                        '5.4']

    SLED_VERSIONS = ['11 sp1', '11 sp2', '11 sp3']

    RHEL_VERSIONS = ['5.1', '5.2', '5.3', '5.5', '5.6', '6.0', '6.1',
                     '6.2', '6.3', '6.4', '6.5']

    UBUNTU_VERSIONS = ['10.04 LTS', '10.04.1 LTS', '10.04.2 LTS',
                       '10.04.3 LTS', '10.04.4 LTS', '12.04 LTS',
                       '12.04.1 LTS', '12.04.2 LTS', '12.04.3 LTS',
                       '12.04.4 LTS', '12.10', '13.10']

    WINDOWS_VERSIONS = ['Windows Server 2008', 'Windows Server 2008 R2',
                        'Windows Server 2012', 'Windows Server 2012 R2']

    # Image Filter Properties:
    # vm_mode
    # hypervisor_type
    # architecture
    # TODO(wko): correlate valid values based on "other" property values
    #       e.g.,
    VM_MODES = ['hvm', 'xen', 'uml', 'exe']

    HYPERVISOR_TYPES = ['xem', 'qemu', 'kvm', 'lxc', 'uml', 'vmware', 'hyperv']

    IMAGE_ARCHITECTURES = ['i686', 'x86_64']

    # TODO(wko): figure out when these would be appropriate(by os_distro?)
    #    IMAGE_ARCHITECTURES = ['alpha', 'armv71', 'cris', 'i686', 'lm32',
    #                           'm68k', 'microblaze', 'microblazeel', 'mips',
    #                           'mipsel', 'mips64', 'mips64el', 'openrisc',
    #                           'parisc', 'parisc64', 'ppc', 'ppc64',
    #                           'ppcemb', 's390', 's390x', 'sh4', 'sh4eb',
    #                           'sparc', 'sparc64', 'unicore32', 'x86_64',
    #                           'xtensa', 'xtensaeb']

    IMAGE_OS_TYPES = ['linux', 'windows']

    # Image Properties:
    # instance_uuid = uuid of guest instance used to create a snapshot image
    # kernel_id = ID of Glance AMI style image used as kernel when booting.
    # ramdisk_id = ID of Glance image to use as ramdisk during image boot

    # Image Snapshot Properties:
    # instance_uuid = (see Image Properties)
    # image_location = snapshot
    # image_type = snapshot
    # base_image_ref = uuid of the glance image the snapshot was taken on
    '''
    Properties added during horizon snapshot processing:
    -------------------------------------+------------------------------------
    Property 'base_image_ref'            |979c2c87-852b-48a2-9dcf-46e133ef0f47
    Property 'image_location'            |snapshot
    Property 'image_state'               |available
    Property 'image_type'                |snapshot
    Property 'instance_type_ephemeral_gb'|0
    Property 'instance_type_flavorid'    |1
    Property 'instance_type_id'          |2
    Property 'instance_type_memory_mb'   |512
    Property 'instance_type_name'        |m1.tiny
    Property 'instance_type_root_gb'     |1
    Property 'instance_type_rxtx_factor' |1.0
    Property 'instance_type_swap'        |0
    Property 'instance_type_vcpus'       |1
    Property 'instance_uuid'             |660bf546-382f-4394-8ba8-1188889d88f9
    Property 'network_allocated'         |True
    Property 'owner_id'                  |0e5831d3a5cb4469bfb29cc69c8760a8
    Property 'user_id'                   |bb52b834b45d41599bc69cde3be57bd7
    '''

    COMPUTE_DRIVERS = ['VMWareComputeDriver', 'XenComputeDriver',
                       'libvirtDriver']
    # VMWareComputeDriver properties:
    # vmware_adaptertype
    # vmware_ostype
    # vmware_image_version
    # TODO(wko): determine valid vmware value combinations:
    # http://docs.openstack.org/trunk/config-reference/content/vmware.html
    #
    # XenComputeDriver properties:
    # auto_disk_config = true/false
    # os_type = linux/windows
    #
    # libvirtDriver properties:
    # hw_video_model
    HW_VIDEO_MODELS = ['vga', 'cirrus', 'vmvga', 'xen', 'gxl']

    def __init__(self, glance_endpoint=None, auth_token=None,
                 image_name_prefix='mock-image',
                 image_file='/var/tmp/mock-test.iso'):

        self.glance_endpoint = glance_endpoint
        self.auth_token = auth_token
        if glance_endpoint is None or auth_token is None:
            keystone = keystone_client.Client(
                auth_url=env['OS_AUTH_URL'],
                username=env['OS_USERNAME'],
                password=env['OS_PASSWORD'],
                tenant_name=env['OS_TENANT_NAME'])

            if glance_endpoint is None:
                self.glance_endpoint = keystone.service_catalog.url_for(
                    service_type='image')

            if auth_token is None:
                self.auth_token = keystone.auth_token

        self.glance = glance_client('1', endpoint=self.glance_endpoint,
                                    token=self.auth_token)

        self.image_name_prefix = image_name_prefix
        self.image_file = image_file

    def _get_image_distro(self):
        return random.choice(self.IMAGE_OS_DISTROS)

    def _get_os_version(self, os_distro):
        #
        os_version = ''
        if os_distro == 'arch':
            os_version = random.choice(self.ARCH_VERSIONS)
        elif os_distro == 'centos':
            os_version = random.choice(self.CENTOS_VERSIONS)
        elif os_distro == 'debian':
            os_version = random.choice(self.DEBIAN_VERSIONS)
        elif os_distro == 'fedora':
            os_version = random.choice(self.FEDORA_VERSIONS)
        elif os_distro == 'freebsd':
            os_version = random.choice(self.FREEBSD_VERSIONS)
        elif os_distro == 'gentoo':
            os_version = random.choice(self.GENTOO_VERSIONS)
        elif os_distro == 'netbsd':
            os_version = random.choice(self.NETBSD_VERSIONS)
        elif os_distro == 'openbsd':
            os_version = random.choice(self.OPENBSD_VERSIONS)
        elif os_distro == 'opensuse':
            os_version = random.choice(self.OPENSUSE_VERSIONS)
        elif os_distro == 'rhel':
            os_version = random.choice(self.RHEL_VERSIONS)
        elif os_distro == 'sled':
            os_version = random.choice(self.SLED_VERSIONS)
        elif os_distro == 'ubuntu':
            os_version = random.choice(self.UBUNTU_VERSIONS)
        elif os_distro == 'windows':
            os_version = random.choice(self.WINDOWS_VERSIONS)

        return os_version

    def _get_os_type(self, os_distro):
        os_type = 'linux'
        if os_distro == 'windows':
            os_type = 'windows'
        return os_type

    def _get_image_architecture(self):
        return random.choice(self.IMAGE_ARCHITECTURES)

    def _get_compute_driver_properties(self):
        compute_driver = random.choice(self.COMPUTE_DRIVERS)
        properties = {}
        if compute_driver.lower() == 'vmwarecomputedriver':
            properties['vmware_adaptertype'] = 'ide'
            properties['vmware_disktype'] = 'sparse'
            properties['vmware_ostype'] = 'ubuntu64Guest'
            properties['vmware_image_version'] = '1'
        elif compute_driver.lower() == 'xencomputedriver':
            properties['auto_disk_config'] = 'false'
            # properties['os_type'] = self._get_os_type(os_distro)
        elif compute_driver.lower() == 'libvirtdriver':
            properties['hw_video_model'] = random.choice(self.HW_VIDEO_MODELS)

        return properties

    def _get_base_properties(self):
        properties = {}
        os_distro = self._get_image_distro()
        properties['os_distro'] = os_distro
        properties['os_version'] = self._get_os_version(os_distro)
        properties['architecture'] = self._get_image_architecture()
        properties['os_type'] = self._get_os_type(os_distro)
        properties['vm_mode'] = random.choice(self.VM_MODES)
        properties['hypervisor_type'] = random.choice(self.HYPERVISOR_TYPES)
        properties = dict(properties.items() +
                          self._get_compute_driver_properties().items())

        return properties

    def _get_snapshot_properties(self, base_image_ref, owner):
        properties = self._get_base_properties()
        properties['image_type'] = 'snapshot'
        properties['image_location'] = 'snapshot'
        properties['instance_uuid'] = uuid.uuid4()
        properties['base_image_ref'] = base_image_ref

        # Additional Properties added during horizon snapshot
        # TODO(wko): account for these in the GLANCE namespace?
        properties['instance_type_ephemeral_gb'] = '0'
        properties['instance_type_flavorid'] = '2'
        properties['instance_type_id'] = '5'
        properties['instance_type_memory_mb'] = '2048'
        properties['instance_type_name'] = 'm1.small'
        properties['instance_type_root_gb'] = '20'
        properties['instance_type_rxtx_factor'] = '1.0'
        properties['instance_type_swap'] = '0'
        properties['instance_type_vcpus'] = '1'
        properties['network_allocated'] = 'True'
        properties['owner_id'] = owner
        properties['user_id'] = str(uuid.uuid4().hex)

        return properties

    def _get_image_name(self):
        tm = datetime.now()
        stamp = '-%s%s%s.%s.%s' %\
                (tm.year, "{0:0>2}".format(tm.month),
                 "{0:0>2}".format(tm.day),
                 (tm.hour * 3600) + (tm.minute * 60) + tm.second,
                 tm.microsecond / 100)

        return self.image_name_prefix + stamp

    def _create_image(self, image_name):
        image = self.glance.images.create(name=image_name)
        image.update(disk_format='vmdk', container_format='bare')
        image.update(data=open(self.image_file, 'rb'))
        return image

    def _update_image(self, image, image_properties):
        return image.update(properties=image_properties, purge_props=False)

    def create(self, num_base_images=1, num_snapshots_per_base=0,
               dry_run=True):
        # Create num_base_images with num_snapshots_per_base
        # if num_base_images is <= 0 no snapshot images will be created.
        count = 0
        while count < num_base_images:
            base_image_name = self._get_image_name()
            print('base_image_name = %s' % base_image_name)
            print('base_properties = %s' % self._get_base_properties())
            print('snapshot_properties = %s' % self._get_snapshot_properties(
                'not-base-ref-yet', 'no-owner-yet'))
            if dry_run is False:
                image = self._create_image(base_image_name)
                self._update_image(image, self._get_base_properties())
                base_image_ref = image.id
                snapshot_properties = self._get_snapshot_properties(
                    base_image_ref, image.owner)
                snap_count = 1
                while snap_count <= num_snapshots_per_base:
                    snap_image_name =\
                        base_image_name + "-snap-{0:0>3}".format(snap_count)
                    image = self._create_image(snap_image_name)
                    self._update_image(image, snapshot_properties)
                    snap_count += 1
            count += 1


# with open('/tmp/authtoken') as fp:
#    authtoken = fp.readline()

# Supply glance endpoint URL and authtoken or if not passed to
# MockGlanceImage() then these env variables must be set:
#  OS_TENANT_NAME, OS_AUTH_URL, OS_USERNAME and OS_PASSWORD
test = MockGlanceImage()
test.create(num_base_images=1, num_snapshots_per_base=2, dry_run=False)
