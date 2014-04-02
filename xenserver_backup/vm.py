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
    Class to represent a Xenserver vm (DomU)
"""
import logging
import time
import os

class XenVM(object):
    def __init__(self, host, uuid, name):
        self.host = host
        self.uuid = uuid
        self.name = name

    def _get_timestamp(self):
        timestamp = time.strftime("%Y-%m-%d_%H%M", time.gmtime())
        return timestamp

    def backup(self):
        timestamp = self._get_timestamp()
        print("Now backing up VM %s (%s) with timestamp %s" % (self.name, self.uuid, timestamp))
        cmd = "xe vm-snapshot uuid=" + self.uuid + " new-name-label=" + timestamp
        snapshot_uuid = self.host.run(cmd)
        print("Backup uuid = %s" % snapshot_uuid)

        cmd = "xe template-param-set is-a-template=false ha-always-run=false uuid=" + snapshot_uuid
        out = self.host.run(cmd)
        print("Set template to false: %s" % out)

        filename = os.path.join(self.host.backup_dir, timestamp+'-'+self.name+'.uva') 
        # Replace any spaces/colons in filename with underscore
        filename = filename.replace(' ', '_')
        filename = filename.replace(':', '_')

        cmd = "xe vm-export nossl=true compress=true vm=" + snapshot_uuid + " filename=" + filename
        print("Running export to %s" % filename)
        self.host.run(cmd)

        cmd = "xe vm-uninstall uuid=" + snapshot_uuid + " force=true"
        print("Deleting snapshot")
        self.host.run(cmd)
        print("Done")

