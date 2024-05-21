import unittest
from Tiếp_nhận.POST import process_patient_from_excel

class TestProcessPatientFromExcel(unittest.TestCase):
    def test_process_patient_from_excel(self):
        # Gọi hàm process_patient_from_excel và kiểm tra kết quả
        entry_ids = process_patient_from_excel()

        # Kiểm tra xem entry_ids có phải là một danh sách không rỗng hay không
        self.assertTrue(entry_ids)
        # Kiểm tra xem entry_ids có chứa ít nhất 5 phần tử hay không
        self.assertGreaterEqual(len(entry_ids), 5)

if __name__ == '__main__':
    unittest.main()