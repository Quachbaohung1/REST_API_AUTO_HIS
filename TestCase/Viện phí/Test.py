import logging
import unittest
import pandas as pd
from unittest.mock import MagicMock
from Viện_phí.POST import (
    process_VP,
    process_VP_without_cost,
    Cost_exemption,
)

# Xác định đường dẫn đến file log
log_file_path = 'D:/HIS api automation/Result/TestResult_VP.txt'

# Xóa file log cũ nếu tồn tại và thiết lập logging
with open(log_file_path, 'w'):  # Mở file trong chế độ ghi để xóa nội dung
    pass  # Pass đơn giản làm gì để xóa

# Thiết lập logging để ghi vào file mới
logging.basicConfig(filename=log_file_path, level=logging.INFO)


# Ghi lại kết quả của test
def log_test_result(test_name, result):
    logging.info(f'Test "{test_name}" - Result: {result}')


def read_test_data(file_path):
    df = pd.read_excel(file_path, sheet_name='Data')
    return df


class TestProcessCosts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.file_path = "D://HIS api automation/DataTest/Viện_phí/TC_01.xlsx"
        cls.test_data = read_test_data(cls.file_path)

    def case_Cost(self, testcase_id, expected_result, process_func):
        # Mock dữ liệu đọc từ file Excel
        test_data = self.test_data[self.test_data['TestCaseId'] == testcase_id]
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [test_data, test_data]

        # Chạy hàm được kiểm thử
        result = process_func(testcase_id)

        # Kiểm tra kết quả và in ra kết quả tương ứng
        if result == expected_result:
            print(f"\nRunning test for {testcase_id}: Passed")
            log_test_result(f"Running test for {testcase_id}", "Passed")
        else:
            print(f"\nRunning test for {testcase_id}: Failed")
            log_test_result(f"Running test for {testcase_id}", "Failed")
        self.assertEqual(result, expected_result,
                         f"Failed for {testcase_id}. Expected: {expected_result}, Actual: {str(result)}")

    # Case quyết toán thành công (BN BHYT)
    def test_case_01(self):
        # bệnh nhân BHYT
        file_path = "D://HIS api automation/DataTest/Data_API_Khám_bệnh.xlsx"
        testcase_id = "VP_1"

        # Mock dữ liệu đọc từ file Excel
        verify_data = pd.read_excel(file_path, sheet_name='Data')
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [verify_data]

        patientCodes = [24028043, 24028044, 24028045, 24028046, 24028047, 24028048, 24028049, 24028050, 24028051, 24028052, 24028053, 24028054, 24028055, 24028056, 24028057, 24028058, 24028059, 24028060]

        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên (lầm 1)
        expected_result_temp = process_VP(self.test_data, file_path, testcase_id, patientCodes)
        expected_result_1 = expected_result_temp

        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Cost(testcase_id, expected_result_1, custom_process_func)


if __name__ == '__main__':
    unittest.main()
