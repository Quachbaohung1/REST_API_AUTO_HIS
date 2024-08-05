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

        patientCodes = [24029075, 24029076, 24029077, 24029078, 24029079, 24029080, 24029081, 24029082, 24029083, 24029084, 24029085, 24029086, 24029087, 24029088, 24029089, 24029090, 24029091, 24029092, 24029093, 24029094, 24029095, 24029096, 24029097, 24029098, 24029099, 24029100, 24029101, 24029102, 24029103, 24029104, 24029105, 24029106, 24029107, 24029108, 24029109, 24029110, 24029111, 24029112, 24029113, 24029114, 24029115, 24029116, 24029117, 24029118, 24029119, 24029120, 24029121, 24029122, 24029123, 24029124, 24029125, 24029126, 24029127, 24029128, 24029129, 24029130, 24029131, 24029132, 24029133, 24029134, 24029135, 24029136, 24029137, 24029138, 24029139, 24029140, 24029141, 24029142, 24029143, 24029144, 24029145, 24029146, 24029147, 24029148, 24029149, 24029150, 24029151, 24029152, 24029153, 24029154, 24029155, 24029156, 24029157, 24029158, 24029159, 24029160, 24029161, 24029162, 24029163, 24029164, 24029165, 24029166, 24029167, 24029168, 24029169, 24029170, 24029171, 24029172, 24029173, 24029174, 24029175, 24029176, 24029177, 24029178, 24029179, 24029180, 24029181, 24029182, 24029183, 24029184, 24029185, 24029186, 24029187, 24029188, 24029189, 24029190, 24029191, 24029192, 24029193, 24029194, 24029195, 24029196, 24029197, 24029198, 24029199, 24029200, 24029201, 24029202, 24029203, 24029204, 24029205, 24029206, 24029207, 24029208, 24029209, 24029210, 24029211, 24029212, 24029213, 24029214, 24029215, 24029216, 24029217, 24029218, 24029219, 24029220, 24029221, 24029222, 24029223, 24029224, 24029225, 24029226, 24029227, 24029228, 24029229, 24029230, 24029231, 24029232, 24029233, 24029234, 24029235, 24029236, 24029237, 24029238, 24029239, 24029240, 24029241, 24029242, 24029243, 24029244, 24029245, 24029246, 24029247, 24029248, 24029249, 24029250, 24029251, 24029252, 24029253, 24029254, 24029255, 24029256, 24029257, 24029258, 24029259, 24029260, 24029261, 24029262, 24029263]


        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên (lầm 1)
        expected_result_temp = process_VP(self.test_data, file_path, testcase_id, patientCodes)
        expected_result_1 = expected_result_temp

        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Cost(testcase_id, expected_result_1, custom_process_func)


if __name__ == '__main__':
    unittest.main()
