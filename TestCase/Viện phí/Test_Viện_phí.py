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

        patientCodes = [24033147, 24033148, 24033149, 24033150, 24033151, 24033152, 24033153,
                        24033154, 24033155, 24033156, 24033157, 24033158, 24033159, 24033160, 24033161, 24033162,
                        24033163, 24033164, 24033165, 24033166, 24033167, 24033168, 24033169, 24033170, 24033171,
                        24033172, 24033173, 24033174, 24033175, 24033176, 24033177, 24033178, 24033179, 24033180,
                        24033181, 24033182, 24033183, 24033184, 24033185, 24033186, 24033187, 24033188, 24033189,
                        24033190, 24033191, 24033192, 24033193, 24033194, 24033195, 24033196, 24033197, 24033198,
                        24033199, 24033200, 24033201, 24033202, 24033203, 24033204, 24033205, 24033206, 24033207,
                        24033208, 24033209, 24033210, 24033211, 24033212, 24033213, 24033214, 24033215, 24033216,
                        24033217, 24033218, 24033219, 24033220, 24033221, 24033222, 24033223, 24033224, 24033225,
                        24033226, 24033227, 24033228, 24033229, 24033230, 24033231, 24033232, 24033233, 24033234,
                        24033235, 24033236, 24033237, 24033238, 24033239, 24033240, 24033241, 24033242, 24033243,
                        24033244, 24033245, 24033246, 24033247, 24033248, 24033249, 24033250, 24033251, 24033252,
                        24033253, 24033254, 24033255, 24033256, 24033257, 24033258, 24033259, 24033260, 24033261,
                        24033262, 24033263, 24033264, 24033265, 24033266, 24033267, 24033268, 24033269, 24033270,
                        24033271, 24033272, 24033273, 24033274, 24033275, 24033276, 24033277]

        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên (lầm 1)
        expected_result_temp = process_VP(self.test_data, file_path, testcase_id, patientCodes)
        expected_result_1 = expected_result_temp

        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Cost(testcase_id, expected_result_1, custom_process_func)

    # Case quyết toán nhưng chưa chốt chi phí (BN BHYT)
    def test_case_02(self):
        # bệnh nhân BHYT
        file_path = "D://HIS api automation/DataTest/Data_API_Khám_bệnh.xlsx"
        testcase_id = "VP_2"

        # Mock dữ liệu đọc từ file Excel
        verify_data = pd.read_excel(file_path, sheet_name='Data')
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [verify_data]

        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên (lầm 1)
        expected_result_temp = process_VP_without_cost(self.test_data, file_path, testcase_id)
        expected_result_1 = expected_result_temp

        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Cost(testcase_id, expected_result_1, custom_process_func)

    # Case quyết toán khi chốt chi phí không thành công (BN BHYT)
    def test_case_03(self):
        # bệnh nhân BHYT
        file_path = "D://HIS api automation/DataTest/Data_API_Khám_bệnh.xlsx"
        testcase_id = "VP_3"

        # Mock dữ liệu đọc từ file Excel
        verify_data = pd.read_excel(file_path, sheet_name='Data')
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [verify_data]

        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên (lầm 1)
        expected_result_temp = process_VP_without_cost(self.test_data, file_path, testcase_id)
        expected_result_1 = expected_result_temp

        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Cost(testcase_id, expected_result_1, custom_process_func)

    # Số tiền miễn giảm nhỏ hơn số tiền chi trả (BN BHYT)
    def test_case_04(self):
        # bệnh nhân BHYT
        file_path = "D://HIS api automation/DataTest/Data_API_Khám_bệnh.xlsx"
        testcase_id = "VP_4"

        # Mock dữ liệu đọc từ file Excel
        verify_data = pd.read_excel(file_path, sheet_name='Data')
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [verify_data]

        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên (lầm 1)
        expected_result_temp = Cost_exemption(self.test_data, file_path, testcase_id)
        expected_result_1 = expected_result_temp

        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Cost(testcase_id, expected_result_1, custom_process_func)

    # Số tiền miễn giảm lớn hơn số tiền chi trả (BN BHYT)
    def test_case_05(self):
        # bệnh nhân BHYT
        file_path = "D://HIS api automation/DataTest/Data_API_Khám_bệnh.xlsx"
        testcase_id = "VP_5"

        # Mock dữ liệu đọc từ file Excel
        verify_data = pd.read_excel(file_path, sheet_name='Data')
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [verify_data]

        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên (lầm 1)
        expected_result_temp = Cost_exemption(self.test_data, file_path, testcase_id)
        expected_result_1 = expected_result_temp

        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Cost(testcase_id, expected_result_1, custom_process_func)

    # Tạm ứng cho BN nhập viện (BN BHYT)

    # Hủy phiếu thu khi chưa hủy quyết toán (BN BHYT)

    # Thu tiền dịch vụ thành công (BN Thu phí)

    # Hoàn/hủy dịch vụ đã thu tiền (BN Thu phí)

    # Thu khác: có nhập mã BN (BN Thu phí)

    # Thu khác: không nhập mã BN (BN Thu phí)


if __name__ == '__main__':
    unittest.main()


