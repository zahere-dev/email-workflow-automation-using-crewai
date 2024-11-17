import unittest

from src.agent.tools.db_ops_tool import read_all_records

class TestDBOpsTool(unittest.TestCase):

    def test_read_all_records(self):
        # Test when the database is empty
        records = read_all_records()
        self.assertGreater(len(records), 0)




if __name__ == '__main__':
    unittest.main()