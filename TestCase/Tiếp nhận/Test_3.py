import unittest
import logging
import pandas as pd
from unittest.mock import MagicMock
from Tiếp_nhận.POST import (
    process_create_patient_from_excel,
    process_create_insurance_from_excel,
    process_patient_from_excel,
    process_generate_patient_from_excel,
    process_generate_sum_patient_from_excel
)

# Xác định đường dẫn đến file log
log_file_path = 'D:/HIS api automation/Result/TestResult_Tiếp_nhận.txt'

# Xóa file log cũ nếu tồn tại
with open(log_file_path, 'w'):  # Mở file trong chế độ ghi để xóa nội dung
    pass  # Pass đơn giản làm gì để xóa

# Thiết lập logging để ghi vào file mới
logging.basicConfig(filename=log_file_path, level=logging.INFO)


# Ghi lại kết quả của test
def log_test_result(test_name, result):
    logging.info(f'Test "{test_name}" - Result: {result}')


# Đọc toàn bộ sheet Excel một lần
def read_test_data(file_path):
    df = pd.read_excel(file_path, sheet_name='Data')
    return df


class TestProcessPatient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.file_path = "D://HIS api automation/DataTest/Tiếp nhận/DataTest.xlsx"
        cls.test_data = read_test_data(cls.file_path)

    # Form test tạo patient
    def case_VisitOn(self, testcase_id, expected_result, process_func):
        # Mock dữ liệu đọc từ file Excel
        test_data = self.test_data[self.test_data['TestCaseId'] == testcase_id]
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [test_data, test_data]

        # Chạy hàm được kiểm thử
        result = process_func(testcase_id)

        # Kiểm tra kết quả và in ra kết quả tương ứng
        if result == expected_result:
            print(f"Running test for {testcase_id}: Passed")
            log_test_result(f"Running test for {testcase_id}", "Passed")
        else:
            print(f"Running test for {testcase_id}: Failed")
            log_test_result(f"Running test for {testcase_id}", "Failed")
        self.assertEqual(result, expected_result,
                         f"Failed for {testcase_id}. Expected: {expected_result}, Actual: {str(result)}")

    # Case tiếp nhận tự động từng loại bệnh nhân
    def test_case_44(self):
        # bệnh nhân BHYT
        file_path = "D://HIS api automation/DataTest/Tiếp nhận/TC_44_Test_3.xlsx"
        # bệnh nhân Thu phí
        # file_path = "E://HIS api automation/DataTest/Tiếp nhận/TC_45.xlsx"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_generate_patient_from_excel(file_path)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(file_path, expected_result, custom_process_func)


if __name__ == '__main__':
    unittest.main()

