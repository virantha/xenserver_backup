# Copyright 2014 Virantha Ekanayake All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
    Class to represent a Xenserver host (Dom0)
"""
import logging
from fabric.api import run, env, cd
from fabric.contrib import files

from vm import XenVM

class XenHost(object):
    def __init__(self, username, hostname, port=22):
        self.user = username
        self.host = hostname
        self.port = port
        env.host_string = '%s@%s:%s' % (self.user, self.host, self.port)
        self.vms = {}

    def run(self, cmd):
        out = run(cmd)
        return out

    def _parse_vm_uuid(self, text):
        vm = {}
        for line in text.splitlines():
            line = line.strip()
            if line.startswith('uuid'):
                # Take the string after the first colon
                uuid = line.split(':', 1)[1].strip()
            if line.startswith('name-label'):
                # Take the string after the first colon (allows for colons in names)
                name = line.split(':', 1)[1].strip()
                vm[name] = uuid
        return vm

    def get_vm_list(self):
        """ Return a dict of vm-name to uuid
        """
        text = self.run('xe vm-list')
        self.vm_names = self._parse_vm_uuid(text)
        return self.vm_names

    def before_backup(self, cmds, directory):
        """
            Make sure the mount cmd can be executed and the directory is present
        """
        if cmds:
            for cmd in cmds:
                self.run(cmd)
        self.backup_dir = directory
        return files.exists(directory)

    def after_backup(self, cmds):
        if cmds:
            for cmd in cmds:
                self.run(cmd)

    def iter_vm(self, vm_name_list=[]):
        if len(vm_name_list)==0:
            vm_name_list = self.vm_names.keys()
        for vm_name in vm_name_list:
            # Make sure this vm name is valid and present
            assert vm_name in self.vm_names.keys()
            uuid = self.vm_names[vm_name]
            yield self.vms.setdefault(uuid, XenVM(self, uuid, vm_name))





