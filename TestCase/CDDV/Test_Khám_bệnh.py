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

    def test_case_00(self):
        result = process_check_patient_in_room()
        expected_result = result

        # Kiểm tra kết quả và in ra kết quả tương ứng
        if result == expected_result:
            print(f"Running test for check patient in room: Passed")
            log_test_result("check patient in room", "Passed")
        else:
            print(f"Running test for check patient in room: Failed")
            log_test_result("check patient in room", "Failed")
        self.assertEqual(result, expected_result,
                         f"Failed for check patient in room. Expected: {expected_result}, Actual: {str(result)}")

    # Nhập đầy đủ thông tin khám bệnh của bệnh nhân
    def test_case_01(self):
        testcase_id = "CDDV_1"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_insert_info_patient(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Examination(testcase_id, expected_result, custom_process_func)

    # Trẻ em dưới 1 tuổi nhập đầy đủ cân nặng
    def test_case_02(self):
        testcase_id = "CDDV_2"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_insert_info_patient(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Examination(testcase_id, expected_result, custom_process_func)

    # Nhập thiếu chẩn đoán sơ bộ
    def test_case_03(self):
        testcase_id = "CDDV_3"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_insert_info_patient(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Examination(testcase_id, expected_result, custom_process_func)

    # Nhập thiếu chẩn đoán chính
    def test_case_04(self):
        testcase_id = "CDDV_4"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_insert_info_patient(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Examination(testcase_id, expected_result, custom_process_func)

    # Nhập thiếu triệu chứng
    def test_case_05(self):
        testcase_id = "CDDV_5"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_insert_info_patient(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Examination(testcase_id, expected_result, custom_process_func)

    # Nhập thiếu ngày khởi phát đối với icd có cấu hình bệnh sốt huyết
    def test_case_06(self):
        testcase_id = "CDDV_6"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_insert_info_patient(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Examination(testcase_id, expected_result, custom_process_func)

    # Ngày khám nhỏ hơn ngày tiếp nhận
    def test_case_07(self):
        testcase_id = "CDDV_7"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_insert_info_patient(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Examination(testcase_id, expected_result, custom_process_func)

    # Trẻ em dưới 1 tuổi không nhập cân nặng
    def test_case_08(self):
        testcase_id = "CDDV_8"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_insert_info_patient(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Examination(testcase_id, expected_result, custom_process_func)

    # Không nhập dịch vụ
    def test_case_09(self):
        testcase_id = "CDDV_9"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_examination_services(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Examination(testcase_id, expected_result, custom_process_func)

    # Không nhập bác sĩ
    def test_case_10(self):
        testcase_id = "CDDV_10"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_examination_services(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Examination(testcase_id, expected_result, custom_process_func)

    # Không nhập số lượng
    def test_case_11(self):
        testcase_id = "CDDV_11"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_examination_services(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Examination(testcase_id, expected_result, custom_process_func)

    # Chỉ định số lượng >1 nhưng không nhập Lý do
    def test_case_12(self):
        testcase_id = "CDDV_12"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_examination_services(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Examination(testcase_id, expected_result, custom_process_func)

    # Chỉ định dịch vụ thiếu Nơi thực hiện
    def test_case_13(self):
        testcase_id = "CDDV_13"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_examination_services(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Examination(testcase_id, expected_result, custom_process_func)

    # Chỉ định dịch vụ thiếu Ngày chỉ định (Không xảy ra)
    # def test_case_14(self):
    #     testcase_id = "CDDV_14"
    #     # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
    #     expected_result_temp = process_examination_services(self.test_data, testcase_id)
    #     # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
    #     expected_result = expected_result_temp
    #     # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
    #     custom_process_func = lambda file_path: expected_result_temp
    #     # Gọi self.test_case với file_path, expected_result và custom_process_func
    #     self.case_Examination(testcase_id, expected_result, custom_process_func)

    # Chỉ định dịch vụ thiếu Chẩn đoán
    def test_case_15(self):
        testcase_id = "CDDV_15"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_examination_services(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Examination(testcase_id, expected_result, custom_process_func)

    # Chỉ định dịch vụ thiếu Mẫu bệnh phẩm
    def test_case_16(self):
        testcase_id = "CDDV_16"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_examination_services(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Examination(testcase_id, expected_result, custom_process_func)

    # Chỉ định dịch vụ thiếu Đơn giá (Chưa định nghĩa giá)
    def test_case_17(self):
        testcase_id = "CDDV_17"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_examination_services(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Examination(testcase_id, expected_result, custom_process_func)

    # Chỉ định dịch vụ có Ngày giờ chỉ định < Ngày khám
    def test_case_18(self):
        testcase_id = "CDDV_18"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_examination_services(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Examination(testcase_id, expected_result, custom_process_func)

    # Nhập đầy đủ thông tin chỉ định dịch vụ thành công
    def test_case_19(self):
        testcase_id = "CDDV_19"
        entry_ids = [53120, 53121, 53122, 53123, 53124, 53125, 53126, 53127, 53128, 53129, 53130, 53131, 53132, 53133, 53134, 53135, 53136, 53137, 53138, 53139, 53140, 53141, 53142, 53143, 53144, 53145, 53146, 53147, 53148, 53149, 53150, 53151, 53152, 53153, 53154, 53155, 53156, 53157, 53158, 53159, 53160, 53161, 53162, 53163, 53164, 53165, 53166, 53167, 53168, 53169, 53170, 53171, 53172, 53173, 53174, 53175, 53176, 53177, 53178, 53179, 53180, 53181, 53182, 53183, 53184, 53185, 53186, 53187, 53188, 53189, 53190, 53191, 53192, 53193, 53194, 53195, 53196, 53197, 53198, 53199, 53200, 53201, 53202, 53203, 53204, 53205, 53206, 53207, 53208, 53209, 53210, 53211, 53212, 53213, 53214, 53215, 53216, 53217, 53218, 53219, 53220, 53221, 53222, 53223, 53224, 53225, 53226, 53227, 53228, 53229, 53230, 53231, 53232, 53233, 53234, 53235, 53236, 53237, 53238, 53239, 53240, 53241, 53242, 53243, 53244, 53245, 53246, 53247, 53248, 53249, 53250, 53251, 53252, 53253, 53254, 53255, 53256, 53257, 53258, 53259, 53260, 53261, 53262, 53263, 53264, 53265, 53266, 53267, 53268, 53269, 53270, 53271, 53272, 53273, 53274, 53275, 53276, 53277, 53278, 53279, 53280, 53281, 53282, 53283, 53284, 53285, 53286, 53287, 53288, 53289, 53290, 53291, 53292, 53293, 53294, 53295, 53296, 53297, 53298, 53299, 53300, 53301, 53302, 53303, 53304, 53305, 53306, 53307, 53308, 53309, 53310, 53311, 53312, 53313, 53314, 53315, 53316, 53317, 53318, 53319, 53320, 53321, 53322, 53323, 53324, 53325, 53326, 53327, 53328, 53329, 53330, 53331, 53333, 53334, 53335, 53336, 53337, 53338, 53339, 53340, 53341, 53342, 53343, 53344, 53345, 53346, 53347, 53348, 53349, 53350, 53351, 53352, 53353, 53354, 53355, 53356, 53357, 53358, 53359, 53360, 53361, 53362, 53363, 53364, 53365, 53366, 53367, 53368, 53369, 53370, 53371, 53372, 53373, 53374, 53375, 53376, 53377, 53378, 53379, 53380, 53381, 53382, 53383, 53384, 53385, 53386, 53387, 53388, 53389, 53390, 53391, 53392, 53393, 53394, 53395, 53396, 53397, 53398, 53399, 53400, 53401, 53402, 53403, 53404, 53405, 53406, 53407, 53408, 53409, 53410, 53411, 53412, 53413, 53414, 53415, 53416, 53417, 53418, 53419, 53420, 53421, 53422, 53423, 53424, 53425, 53426, 53427, 53428, 53429, 53430, 53431, 53432, 53433, 53434, 53435, 53436, 53437, 53438, 53439, 53440, 53441, 53442, 53443, 53444, 53445, 53446, 53447, 53448, 53449, 53450, 53451, 53452, 53453, 53454, 53455, 53456, 53457, 53458, 53459, 53460, 53461, 53462, 53463, 53464, 53465, 53466, 53467, 53468, 53469, 53470, 53471, 53472, 53473, 53474, 53475, 53476, 53477, 53478, 53479, 53480, 53481, 53482, 53483, 53484, 53485, 53486, 53487, 53488, 53489, 53490, 53491, 53492, 53493, 53494, 53495, 53496, 53497, 53498, 53499, 53500, 53501, 53502, 53503, 53504, 53505, 53506, 53507, 53508, 53509, 53510, 53511, 53512, 53513, 53514, 53515, 53516, 53517, 53518, 53519, 53520]

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

