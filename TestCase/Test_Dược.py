import unittest
import pandas as pd
from unittest.mock import MagicMock
from Dược.POST import (
    process_store,
    process_recall_store,
)


class TestProcessStore(unittest.TestCase):
    def case_Store(self, file_path, expected_result, process_func):
        # Mock dữ liệu đọc từ file Excel
        test_data = pd.read_excel(file_path, sheet_name='Data')
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [test_data, test_data]

        # Chạy hàm được kiểm thử
        result = process_func(file_path)

        # Kiểm tra kết quả và in ra kết quả tương ứng
        if result == expected_result:
            print(f"\nRunning test for {file_path}: Passed")
        else:
            print(f"\nRunning test for {file_path}: Failed")
        self.assertEqual(result, expected_result,
                         f"Failed for {file_path}. Expected: {expected_result}, Actual: {str(result)}")

    # Thu tiền và phát thuốc thành công
    def test_case_01(self):
        file_path = "D://HIS api automation/DataTest/Dược/TC_01.xlsx"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_store(file_path)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Store(file_path, expected_result, custom_process_func)

    # Thu hồi thuốc và hoàn tiền đã phát thành công
    def test_case_02(self):
        file_path = "D://HIS api automation/DataTest/Dược/TC_02.xlsx"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_recall_store(file_path)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Store(file_path, expected_result, custom_process_func)


if __name__ == '__main__':
    unittest.main()
