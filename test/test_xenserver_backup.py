import xenserver_backup.XenBackup as P
import pytest
import os
import logging

import smtplib
from mock import Mock
from mock import patch, call
from mock import MagicMock
from mock import PropertyMock


class Testxenserver_backup:

    def setup(self):
        self.p = P.XenBackup()
