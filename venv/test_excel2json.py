import unittest
import excel2json

class Excel2JsonTest(unittest.TestCase):
    def test_excel_mapping(self):
        ws, heading_map = excel2json.get_sheet_and_map('incoming/Bootcamp case2 rubric.xlsx')
        print(str(heading_map))


if __name__ == "__main__":
    unittest.main()
