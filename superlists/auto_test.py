

import os
import unittest


class RUN_ALL_TEST(unittest.TestCase):

    def test_run_all(self):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "superlists.settings")
        argv  = ['/home/yang/Desktop/battle_ship/superlists/manage.py', 'test', 'lists']
        from django.core.management import execute_from_command_line
        execute_from_command_line(argv)
