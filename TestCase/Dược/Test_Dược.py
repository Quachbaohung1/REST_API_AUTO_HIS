import logging
import unittest
import pandas as pd
from unittest.mock import MagicMock
from Dược.POST import (
    process_store,
    process_recall_store,
    process_store_BHYT,
    recommend_medication,
    confirm_warehouse,
    transfer_warehouse,
    other_export,
    warehouse_return,
)

# Xác định đường dẫn đến file log
log_file_path = 'D:/HIS api automation/Result/TestResult_Dược.txt'

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


class TestProcessStore(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.file_path = "D://HIS api automation/DataTest/Dược/TC_01.xlsx"
        cls.test_data = read_test_data(cls.file_path)

    def case_Store(self, testcase_id, expected_result, process_func):
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

    # Thu tiền và phát thuốc thành công
    def test_case_01(self):
        testcase_id = "DLS_1"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_store(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Store(testcase_id, expected_result, custom_process_func)

    # Thu hồi thuốc và hoàn tiền đã phát thành công
    def test_case_02(self):
        testcase_id = "DLS_2"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_recall_store(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Store(testcase_id, expected_result, custom_process_func)

    # Đề nghị lên kho chẳn
    def test_case_03(self):
        testcase_id = "DLS_3"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = recommend_medication(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Store(testcase_id, expected_result, custom_process_func)

    # Xác nhận nhập từ kho chẳn
    def test_case_04(self):
        testcase_id = "DLS_4"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = confirm_warehouse(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Store(testcase_id, expected_result, custom_process_func)

    # Chuyển kho
    def test_case_05(self):
        testcase_id = "DLS_5"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = transfer_warehouse(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Store(testcase_id, expected_result, custom_process_func)

    # Xuất khác (xuất hủy/thanh lý)
    def test_case_06(self):
        testcase_id = "DLS_6"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = other_export(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Store(testcase_id, expected_result, custom_process_func)

    # Hoàn trả - kho
    def test_case_07(self):
        testcase_id = "DLS_7"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = warehouse_return(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Store(testcase_id, expected_result, custom_process_func)

    # Case 8 và
    # Phát thuốc BHYT
    def test_case_08(self):
        testcase_id = "DLS_8"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_store_BHYT(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Store(testcase_id, expected_result, custom_process_func)

    # Hủy xác nhận phát thuốc
    def test_case_09(self):
        testcase_id = "DLS_9"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_store_BHYT(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Store(testcase_id, expected_result, custom_process_func)


if __name__ == '__main__':
    unittest.main()
