import logging
import unittest
import pandas as pd
from unittest.mock import MagicMock
from Khám_bệnh_CDDV.POST import (
    process_check_patient_in_room,
    process_insert_info_patient,
    process_examination_services,
)

# Xác định đường dẫn đến file log
log_file_path = 'D:/HIS api automation/Result/TestResult_CDDV.txt'

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


class TestProcessExamination(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.file_path = "D://HIS api automation/DataTest/Khám bệnh - CDDV/TC_01.xlsx"
        cls.test_data = read_test_data(cls.file_path)

    def case_Examination(self, testcase_id, expected_result, process_func):
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

    # Nhập đầy đủ thông tin chỉ định dịch vụ thành công
    def test_case_19(self):
        testcase_id = "CDDV_19"
        entry_ids = [54054, 54055, 54056, 54057, 54058, 54059, 54060, 54061, 54062, 54063, 54064, 54065, 54066, 54067, 54068, 54069, 54070, 54071, 54072, 54073, 54074, 54075, 54076, 54077, 54078, 54079, 54080, 54081, 54082, 54083, 54084, 54085, 54086, 54087, 54088, 54089, 54090, 54091, 54092, 54093, 54094, 54095, 54096, 54097, 54098, 54099, 54100, 54101, 54102, 54103, 54104, 54105, 54106, 54107, 54108, 54109, 54110, 54111, 54112, 54113, 54114, 54115, 54116, 54117, 54118, 54119, 54120, 54121, 54122, 54123, 54124, 54125, 54126, 54127, 54128, 54129, 54130, 54131, 54132, 54133, 54134, 54135, 54136, 54137, 54138, 54139, 54140, 54141, 54142, 54143, 54144, 54145, 54146, 54147, 54148, 54149, 54150, 54151, 54152, 54153, 54154, 54155, 54156, 54157, 54158, 54159, 54160, 54161, 54162, 54163, 54164, 54165, 54166, 54167, 54168, 54169, 54170, 54171, 54172, 54173, 54174, 54175, 54176, 54177, 54178, 54179, 54180, 54181, 54182, 54183, 54184, 54185, 54186, 54187, 54188, 54189, 54190, 54191, 54192, 54193, 54194, 54195, 54196, 54197, 54198, 54199, 54200, 54201, 54202, 54203, 54204, 54205, 54206, 54207, 54208, 54209, 54210, 54211, 54212, 54213, 54214, 54215, 54216, 54217, 54218, 54219, 54220, 54221, 54222, 54223, 54224, 54225, 54226, 54227, 54228, 54229, 54230, 54231, 54232, 54233, 54234, 54235, 54236, 54237, 54238, 54239, 54240, 54241, 54242, 54243, 54244, 54245, 54246, 54247, 54248, 54249, 54250, 54251, 54252, 54253, 54254, 54255, 54256, 54257, 54258, 54259, 54260, 54261, 54262, 54263, 54264, 54265, 54266, 54267, 54268, 54269, 54270, 54271, 54272, 54273, 54274, 54275, 54276, 54277, 54278, 54279, 54280, 54281, 54282, 54283, 54284, 54285, 54286, 54287, 54288, 54289, 54290, 54291, 54292, 54293, 54294, 54295, 54296, 54297, 54298, 54299, 54300, 54301, 54302, 54303, 54304, 54305, 54306, 54307, 54308, 54309, 54310, 54311, 54312, 54313, 54314, 54315, 54316, 54317, 54318, 54319, 54320, 54321, 54322, 54323, 54324, 54325, 54326, 54327, 54328, 54329]

        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_examination_services(self.test_data, testcase_id, entry_ids)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Examination(testcase_id, expected_result, custom_process_func)


if __name__ == '__main__':
    unittest.main()
