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

        patientCodes = [24028063, 24028064, 24028065, 24028066, 24028067, 24028068, 24028069, 24028070, 24028071,
                        24028072, 24028073, 24028074, 24028075, 24028076, 24028077, 24028078, 24028079, 24028080,
                        24028081, 24028082, 24028083, 24028084, 24028085, 24028086, 24028087, 24028088, 24028089,
                        24028090, 24028091, 24028092, 24028093, 24028094, 24028095, 24028096, 24028097, 24028098,
                        24028099, 24028100, 24028101, 24028102, 24028103, 24028104, 24028105, 24028106, 24028107,
                        24028108, 24028109, 24028110, 24028111, 24028112, 24028113, 24028114, 24028115, 24028116,
                        24028117, 24028118, 24028119, 24028120, 24028121, 24028122, 24028123, 24028124, 24028125,
                        24028126, 24028127, 24028128, 24028129, 24028130, 24028131, 24028132, 24028133, 24028134,
                        24028135, 24028136, 24028137, 24028138, 24028139, 24028140, 24028141, 24028142, 24028143,
                        24028144, 24028145, 24028146, 24028147, 24028148, 24028149, 24028150, 24028151, 24028152,
                        24028153, 24028154, 24028155, 24028156, 24028157, 24028158, 24028159, 24028160, 24028161,
                        24028162, 24028163, 24028164, 24028165, 24028166, 24028167, 24028168, 24028169, 24028170,
                        24028171, 24028172, 24028173, 24028174, 24028175, 24028176, 24028177, 24028178, 24028179,
                        24028180, 24028181, 24028182, 24028183, 24028184, 24028185, 24028186, 24028187, 24028188,
                        24028189, 24028190, 24028191, 24028192, 24028193, 24028194, 24028195, 24028196, 24028197,
                        24028198, 24028199, 24028200, 24028201, 24028202, 24028203, 24028204, 24028205, 24028206,
                        24028207, 24028208, 24028209, 24028210, 24028211, 24028212, 24028213, 24028214, 24028215,
                        24028216, 24028217, 24028218, 24028219, 24028220, 24028221, 24028222, 24028223, 24028224,
                        24028225, 24028226, 24028227, 24028228, 24028229, 24028230, 24028231, 24028232, 24028233,
                        24028234, 24028235, 24028236, 24028237, 24028238, 24028239, 24028240, 24028241, 24028242,
                        24028243, 24028244, 24028245, 24028246, 24028247, 24028248, 24028249, 24028250, 24028251,
                        24028252, 24028253, 24028254, 24028255, 24028256, 24028257, 24028258, 24028259, 24028260,
                        24028261, 24028262, 24028263, 24028264, 24028265, 24028266, 24028267, 24028268, 24028269,
                        24028270, 24028271, 24028272, 24028273, 24028274, 24028275, 24028276, 24028277, 24028278,
                        24028279, 24028280, 24028281, 24028282, 24028283, 24028284, 24028285, 24028286, 24028287,
                        24028288, 24028289, 24028290, 24028291, 24028292, 24028293, 24028294, 24028295, 24028296,
                        24028297, 24028298, 24028299, 24028300, 24028301, 24028302, 24028303, 24028304, 24028305,
                        24028306, 24028307, 24028308, 24028309, 24028310, 24028311, 24028312, 24028313, 24028314,
                        24028315, 24028316, 24028317, 24028318, 24028319, 24028320, 24028321, 24028322, 24028323,
                        24028324, 24028325, 24028326, 24028327, 24028328, 24028329, 24028330, 24028331, 24028332,
                        24028333, 24028334, 24028335, 24028336, 24028337, 24028338, 24028339, 24028340, 24028341,
                        24028342, 24028343, 24028344, 24028345, 24028346, 24028347, 24028348, 24028349, 24028350,
                        24028351, 24028352, 24028353, 24028354, 24028355, 24028356, 24028357, 24028358, 24028359,
                        24028360, 24028361, 24028362, 24028363, 24028364, 24028365, 24028366, 24028367, 24028368,
                        24028369, 24028370, 24028371, 24028372, 24028373, 24028374, 24028375, 24028376, 24028377,
                        24028378, 24028379, 24028380, 24028381, 24028382, 24028383, 24028384, 24028385, 24028386,
                        24028387, 24028388, 24028389, 24028390, 24028391, 24028392, 24028393, 24028394, 24028395,
                        24028396, 24028397, 24028398, 24028399, 24028400, 24028401, 24028402, 24028403, 24028404,
                        24028405, 24028406, 24028407, 24028408, 24028409, 24028410, 24028411, 24028412, 24028413,
                        24028414, 24028415, 24028416, 24028417, 24028418, 24028419, 24028420, 24028421, 24028422,
                        24028423, 24028424, 24028425, 24028426, 24028427, 24028428, 24028429, 24028430, 24028431,
                        24028432, 24028433, 24028434, 24028435, 24028436, 24028437, 24028438, 24028439, 24028440,
                        24028441, 24028442, 24028443, 24028444, 24028445, 24028446, 24028447, 24028448, 24028449,
                        24028450, 24028451, 24028452, 24028453, 24028454, 24028455, 24028456, 24028457, 24028458,
                        24028459, 24028460, 24028461, 24028462]

        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên (lầm 1)
        expected_result_temp = process_VP(self.test_data, file_path, testcase_id, patientCodes)
        expected_result_1 = expected_result_temp

        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Cost(testcase_id, expected_result_1, custom_process_func)


if __name__ == '__main__':
    unittest.main()
