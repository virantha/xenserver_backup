#!/usr/bin/env python2.7
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
"""Xenserver Backup.

Usage:
    xenserver_backup.py [options] <servername> <config>


Options:
    -u <username>   Xenserver Host Username [default: root].
    -p <port>       Xenserver ssh port [default: 22].
    -h --help       Show this screen.
    --version       Show version.
    -v --verbose    Verbose logging
    -d --debug      Debug logging
    


"""

import sys, os
import logging
import shutil

from version import __version__
import yaml
from docopt import docopt
from fabric.api import local, run, env, cd

from host import XenHost


"""
   
.. automodule:: xenserver_backup
    :private-members:
"""

class XenBackup(object):
    """
        The main clas.  Performs the following functions:

    """

    def __init__ (self):
        """ 
        """
        self.config = None

    def _get_config_file(self, config_file):
        """
           Read in the yaml config file

           :param config_file: Configuration file (YAML format)
           :type config_file: file
           :returns: dict of yaml file
           :rtype: dict
        """
        with config_file:
            myconfig = yaml.load(config_file)
        return myconfig


    def get_options(self, argv):
        """
            Parse the command-line options and set the following object properties:

            :param argv: usually just sys.argv[1:]
            :returns: Nothing

            :ivar debug: Enable logging debug statements
            :ivar verbose: Enable verbose logging
            :ivar config: Dict of the config file

        """
        self.args = argv

        if argv['--verbose']:
            logging.basicConfig(level=logging.INFO, format='%(message)s')
        if argv['--debug']:
            logging.basicConfig(level=logging.DEBUG, format='%(message)s')                
        config_filename = self.args['<config>']
        assert os.path.exists(config_filename), "Oops, cannot find config file"
        with open(self.args['<config>']) as f:
            self.config = yaml.load(f)

        
    
    def go(self, argv):
        """ 
            The main entry point into XenBackup

            #. Do something
            #. Do something else
        """
        # Read the command line options
        self.get_options(argv)
        
        self.host = XenHost(self.args['-u'], self.args['<servername>'], self.args['-p'])
        out = self.host.get_vm_list()
        print (out)
        print(self.config)
        self.host.prepare_backup(self.config['backup_location']['command'],
                            self.config['backup_location']['dir'],
                            )



def main():
    args = docopt(__doc__, version='Xenserver Backup %s' % __version__ )
    print (args)
    script = XenBackup()
    script.go(args)

if __name__ == '__main__':
    main()

