import unittest
import pandas as pd
from unittest.mock import MagicMock
from Viện_phí.POST import (
    process_VP,
)


class TestProcessCosts(unittest.TestCase):
    # Case quyết toán thành công
    def test_case_01(self):
        # bệnh nhân BHYT
        file_path = "D://HIS api automation/DataTest/Data_API_Khám_bệnh.xlsx"
        file_path_a = "D://HIS api automation/DataTest/Viện_phí/TC_01.xlsx"

        # Mock dữ liệu đọc từ file Excel
        test_data = pd.read_excel(file_path_a, sheet_name='Data')
        verify_data = pd.read_excel(file_path_a, sheet_name='Check')
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [test_data, verify_data, test_data]

        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên (lầm 1)
        result_1 = process_VP(file_path, file_path_a)
        expected_result_1 = result_1

        # Kiểm tra kết quả và in ra kết quả tương ứng (lần 1)
        if result_1 == expected_result_1:
            print(f"Running test for {file_path}: " "Passed")
        else:
            print(f"Running test for {file_path}: " "Failed")
        self.assertEqual(result_1, expected_result_1,
                         f"Failed for {file_path}. Expected: {expected_result_1}, Actual: {str(result_1)}")

    # Case check số tiền quyết toán với UI trên màn hình
    def test_case_02(self):
        # bệnh nhân BHYT
        file_path = "D://HIS api automation/DataTest/Tiếp nhận/TC_02.xlsx"

        # Mock dữ liệu đọc từ file Excel
        test_data = pd.read_excel(file_path, sheet_name='Data')
        verify_data = pd.read_excel(file_path, sheet_name='Check')
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [test_data, verify_data, test_data]

        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên (lần 1)
        result_1 = process_create_insurance_from_excel(file_path)
        expected_result_1 = None

        # Kiểm tra kết quả và in ra kết quả tương ứng (lần 1)
        if result_1 == expected_result_1:
            print(f"Running test for {file_path}: " "Passed")
        else:
            print(f"Running test for {file_path}: " "Failed")
        self.assertEqual(result_1, expected_result_1,
                         f"Failed for {file_path}. Expected: {expected_result_1}, Actual: {str(result_1)}")

    # Case check số tiền quyết toán với UI trên màn hình
    def test_case_03(self):
        # bệnh nhân BHYT
        file_path = "D://HIS api automation/DataTest/Tiếp nhận/TC_02.xlsx"

        # Mock dữ liệu đọc từ file Excel
        test_data = pd.read_excel(file_path, sheet_name='Data')
        verify_data = pd.read_excel(file_path, sheet_name='Check')
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [test_data, verify_data, test_data]

        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên (lần 1)
        result_1 = process_create_insurance_from_excel(file_path)
        expected_result_1 = None

        # Kiểm tra kết quả và in ra kết quả tương ứng (lần 1)
        if result_1 == expected_result_1:
            print(f"Running test for {file_path}: " "Passed")
        else:
            print(f"Running test for {file_path}: " "Failed")
        self.assertEqual(result_1, expected_result_1,
                         f"Failed for {file_path}. Expected: {expected_result_1}, Actual: {str(result_1)}")


if __name__ == '__main__':
    unittest.main()
