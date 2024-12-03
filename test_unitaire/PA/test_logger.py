import sqlite3
from unittest import TestCase
from lib.logger import *


class TestLogger(TestCase):

    def test_log(self):
        logger = Logger('log', 'export', 'log/log.db', create_file=False)
        logger.filename = 'test.log'

        test_value = ['test', 'test\n', 'test\ntest\n', '']

        for value in test_value:

            with open('log/test.log', 'w') as f:
                pass
            logger.log(value)

            with open('log/test.log', 'r') as f:
                if not f.read() == value:
                    raise AssertionError


    def test_create_table(self):
        logger = Logger('log', 'export', 'log/test_table.db', create_file=False)

        test_value = ['test', 'xyzxyz', 't123456789', 't']

        bad_value = [' ', '1213', 'a a']

        for table in logger.get_tables():
            logger.delete_table(table)

        for value in test_value:
            logger.create_table(table_name=value)

        with self.assertRaises(sqlite3.Error):
            for value in bad_value:
                logger.create_table(table_name=value)

        table = logger.get_tables()
        print(table)
        for value in test_value:
            if not 'table_'+value in table:
                raise AssertionError


    def test_get_tables(self):
        def equality_check(arr1: list[str], arr2: list[str]) -> bool:
            if len(arr1) != len(arr2):
                return False
            for i in range(0, len(arr2)):
                if arr1[i] != arr2[i]:
                    return False
            return True
        logger = Logger('log', 'export', 'log/test_get_table.db', create_file=False)

        if not equality_check(logger.get_tables(), ['table_20241127114545', 'table_20241127115631', 'table_20241203180131']):
            raise AssertionError

    def test_log_db(self):
        logger = Logger('log', 'export', 'log/log_db.db', create_file=False)

        test_value = [('', '', '', '', '', '', ''), ('a', '\n', ' a ', 'azertyuiopqsdfghjklm', 45623, '', '')]

        logger.current_table = 'table_20241203213326'

        for value in test_value:
            logger.log_db(value)

        for x, value in enumerate(test_value):
            if not logger.get_data('table_20241203213326')[x] == value:
                raise AssertionError

    def test_delete_table(self):
        logger = Logger('log', 'export', 'log/delete_db.db', create_file=False)

        test_value = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

        for value in test_value:
            logger.create_table(value)

        for value in test_value:
            logger.delete_table('table_'+value)

        if len(logger.get_tables()) != 0:
            raise AssertionError

    def test_export_data(self):
        pass

    def test_get_data(self):
        pass

    def test_close(self):
        pass
