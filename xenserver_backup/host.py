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

class XenHost(object):
    def __init__(self, username, hostname, port=22):
        self.user = username
        self.host = hostname
        self.port = port
        env.host_string = '%s@%s:%s' % (self.user, self.host, self.port)

    def _run(self, cmd):
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
        text = self._run('xe vm-list')
        self.vm = self._parse_vm_uuid(text)
        return self.vm

    def prepare_backup(self, cmd, directory):
        """
            Make sure the mount cmd can be executed and the directory is present
        """
        if cmd != "":
            self._run(cmd)
        with cd(directory):
            self._run('ls')




