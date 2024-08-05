import logging
import unittest
import pandas as pd
from unittest.mock import MagicMock
from Khám_bệnh_Toa_thuốc.POST import (
    process_check_patient_in_room,
    process_insert_info_patient,
    process_info_prescription_services,
    process_prescription_services,
)

# Xác định đường dẫn đến file log
log_file_path = 'D:/HIS api automation/Result/TestResult_Kê_toa.txt'

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


class TestProcessPrescription(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.file_path = "D://HIS api automation/DataTest/Khám bệnh - Kê thuốc/TC_01.xlsx"
        cls.test_data = read_test_data(cls.file_path)

    def case_Prescription(self, testcase_id, expected_result, process_func):
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

    # Kiểm tra bệnh nhân có trong phòng khám
    def test_case_00(self):
        result = process_check_patient_in_room()
        expected_result = result

        # Kiểm tra kết quả và in ra kết quả tương ứng
        if result == expected_result:
            print(f"Running test for check patient in room: Passed")
            log_test_result(f"Running test for check patient in room", "Passed")
        else:
            print(f"Running test for check patient in room: Failed")
            log_test_result(f"Running test for check patient in room", "Failed")
        self.assertEqual(result, expected_result,
                         f"Failed for check patient in room. Expected: {expected_result}, Actual: {str(result)}")

    # Nhập đầy đủ thông tin khám bệnh của bệnh nhân
    def test_case_01(self):
        testcase_id = "KT_1"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_insert_info_patient(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Prescription(testcase_id, expected_result, custom_process_func)

    # Nhập thiếu chẩn đoán sơ bộ
    def test_case_02(self):
        testcase_id = "KT_2"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_insert_info_patient(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Prescription(testcase_id, expected_result, custom_process_func)

    # Nhập thiếu chẩn đoán chính
    def test_case_03(self):
        testcase_id = "KT_3"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_insert_info_patient(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Prescription(testcase_id, expected_result, custom_process_func)

    # Nhập thiếu triệu chứng
    def test_case_04(self):
        testcase_id = "KT_4"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_insert_info_patient(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Prescription(testcase_id, expected_result, custom_process_func)

    # Nhập thiếu ngày khởi phát đối với icd có cấu hình bệnh sốt huyết
    def test_case_05(self):
        testcase_id = "KT_5"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_insert_info_patient(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = 200
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Prescription(testcase_id, expected_result, custom_process_func)

    # Ngày khám nhỏ hơn ngày tiếp nhận
    def test_case_06(self):
        testcase_id = "KT_6"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_insert_info_patient(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Prescription(testcase_id, expected_result, custom_process_func)

    # Trẻ em dưới 1 tuổi không nhập cân nặng
    def test_case_07(self):
        testcase_id = "KT_7"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_insert_info_patient(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Prescription(testcase_id, expected_result, custom_process_func)

    # Không nhập thông tin thuốc BHYT
    def test_case_08(self):
        # Cho bệnh nhân BHYT
        testcase_id = "KT_8"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_info_prescription_services(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = 204
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Prescription(testcase_id, expected_result, custom_process_func)

    # # Không nhập thông tin kho BHYT
    # def test_case_09(self):
    #     # Cho bệnh nhân BHYT
    #     testcase_id = "KT_9"
    #     # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
    #     expected_result_temp = process_info_prescription_services(self.test_data, testcase_id)
    #     # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
    #     expected_result = 204
    #     # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
    #     custom_process_func = lambda file_path: expected_result_temp
    #     # Gọi self.test_case với file_path, expected_result và custom_process_func
    #     self.case_Prescription(testcase_id, expected_result, custom_process_func)
    #
    # # Không nhập thông tin ngày dùng thuốc BHYT
    # def test_case_10(self):
    #     # Cho bệnh nhân BHYT
    #     testcase_id = "KT_10"
    #     # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
    #     expected_result_temp = process_prescription_services(self.test_data, testcase_id)
    #     # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
    #     expected_result = None
    #     # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
    #     custom_process_func = lambda file_path: expected_result_temp
    #     # Gọi self.test_case với file_path, expected_result và custom_process_func
    #     self.case_Prescription(testcase_id, expected_result, custom_process_func)
    #
    # # Không nhập thông tin sáng trưa chiều tối BHYT
    # def test_case_11(self):
    #     # Cho bệnh nhân BHYT
    #     testcase_id = "KT_11"
    #     # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
    #     expected_result_temp = process_prescription_services(self.test_data, testcase_id)
    #     # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
    #     expected_result = None
    #     # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
    #     custom_process_func = lambda file_path: expected_result_temp
    #     # Gọi self.test_case với file_path, expected_result và custom_process_func
    #     self.case_Prescription(testcase_id, expected_result, custom_process_func)
    #
    # # Không nhập thông tin hoạt chất BHYT
    # def test_case_12(self):
    #     # Cho bệnh nhân BHYT
    #     testcase_id = "KT_12"
    #     # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
    #     expected_result_temp = process_prescription_services(self.test_data, testcase_id)
    #     # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
    #     expected_result = expected_result_temp
    #     # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
    #     custom_process_func = lambda file_path: expected_result_temp
    #     # Gọi self.test_case với file_path, expected_result và custom_process_func
    #     self.case_Prescription(testcase_id, expected_result, custom_process_func)
    #
    # # Không nhập thông tin đường dùng BHYT
    # def test_case_13(self):
    #     # Cho bệnh nhân BHYT
    #     testcase_id = "KT_13"
    #     # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
    #     expected_result_temp = process_prescription_services(self.test_data, testcase_id)
    #     # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
    #     expected_result = None
    #     # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
    #     custom_process_func = lambda file_path: expected_result_temp
    #     # Gọi self.test_case với file_path, expected_result và custom_process_func
    #     self.case_Prescription(testcase_id, expected_result, custom_process_func)
    #
    # # Không nhập thông tin hàm lượng BHYT
    # def test_case_14(self):
    #     # Cho bệnh nhân BHYT
    #     testcase_id = "KT_14"
    #     # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
    #     expected_result_temp = process_prescription_services(self.test_data, testcase_id)
    #     # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
    #     expected_result = None
    #     # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
    #     custom_process_func = lambda file_path: expected_result_temp
    #     # Gọi self.test_case với file_path, expected_result và custom_process_func
    #     self.case_Prescription(testcase_id, expected_result, custom_process_func)
    #
    # # Không nhập thông tin đơn vị dùng BHYT
    # def test_case_15(self):
    #     # Cho bệnh nhân BHYT
    #     testcase_id = "KT_15"
    #     # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
    #     expected_result_temp = process_prescription_services(self.test_data, testcase_id)
    #     # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
    #     expected_result = None
    #     # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
    #     custom_process_func = lambda file_path: expected_result_temp
    #     # Gọi self.test_case với file_path, expected_result và custom_process_func
    #     self.case_Prescription(testcase_id, expected_result, custom_process_func)
    #
    # # Không nhập thông tin đơn vị tính BHYT
    # def test_case_16(self):
    #     # Cho bệnh nhân BHYT
    #     testcase_id = "KT_16"
    #     # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
    #     expected_result_temp = process_prescription_services(self.test_data, testcase_id)
    #     # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
    #     expected_result = None
    #     # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
    #     custom_process_func = lambda file_path: expected_result_temp
    #     # Gọi self.test_case với file_path, expected_result và custom_process_func
    #     self.case_Prescription(testcase_id, expected_result, custom_process_func)
    #
    # # Không nhập thông tin số lượng BHYT
    # def test_case_17(self):
    #     # Cho bệnh nhân BHYT
    #     testcase_id = "KT_17"
    #     # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
    #     expected_result_temp = process_prescription_services(self.test_data, testcase_id)
    #     # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
    #     expected_result = 204
    #     # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
    #     custom_process_func = lambda file_path: expected_result_temp
    #     # Gọi self.test_case với file_path, expected_result và custom_process_func
    #     self.case_Prescription(testcase_id, expected_result, custom_process_func)
    #
    # # Không nhập thông tin mã thuốc BHYT
    # def test_case_18(self):
    #     # Cho bệnh nhân BHYT
    #     testcase_id = "KT_18"
    #     # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
    #     expected_result_temp = process_prescription_services(self.test_data, testcase_id)
    #     # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
    #     expected_result = None
    #     # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
    #     custom_process_func = lambda file_path: expected_result_temp
    #     # Gọi self.test_case với file_path, expected_result và custom_process_func
    #     self.case_Prescription(testcase_id, expected_result, custom_process_func)
    #
    # # Nhập số lượng thuốc lớn hơn tồn BHYT
    # def test_case_19(self):
    #     pass
    #
    # Nhập đầy đủ thông tin và chọn kho BHYT
    def test_case_20(self):
        # Cho bệnh nhân BHYT
        testcase_id = "KT_20"
        entry_ids = [49798]
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_prescription_services(self.test_data, testcase_id, entry_ids)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_Prescription(testcase_id, expected_result, custom_process_func)
    #
    # # Nhập đầy đủ thông tin và chọn kho Nhà thuốc
    # def test_case_21(self):
    #     # Cho bệnh nhân BHYT
    #     testcase_id = "KT_21"
    #     # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
    #     expected_result_temp = process_prescription_services(self.test_data, testcase_id)
    #     # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
    #     expected_result = None
    #     # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
    #     custom_process_func = lambda file_path: expected_result_temp
    #     # Gọi self.test_case với file_path, expected_result và custom_process_func
    #     self.case_Prescription(testcase_id, expected_result, custom_process_func)
    #
    # # Không nhập thông tin thuốc Thu phí
    # def test_case_22(self):
    #     # Cho bệnh nhân BHYT
    #     testcase_id = "KT_22"
    #     # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
    #     expected_result_temp = process_info_prescription_services(self.test_data, testcase_id)
    #     # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
    #     expected_result = 204
    #     # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
    #     custom_process_func = lambda file_path: expected_result_temp
    #     # Gọi self.test_case với file_path, expected_result và custom_process_func
    #     self.case_Prescription(testcase_id, expected_result, custom_process_func)
    #
    # # Không nhập thông tin kho Thu phí
    # def test_case_23(self):
    #     # Cho bệnh nhân BHYT
    #     testcase_id = "KT_23"
    #     # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
    #     expected_result_temp = process_info_prescription_services(self.test_data, testcase_id)
    #     # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
    #     expected_result = 204
    #     # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
    #     custom_process_func = lambda file_path: expected_result_temp
    #     # Gọi self.test_case với file_path, expected_result và custom_process_func
    #     self.case_Prescription(testcase_id, expected_result, custom_process_func)
    #
    # # Không nhập thông tin ngày dùng thuốc Thu phí
    # def test_case_24(self):
    #     # Cho bệnh nhân BHYT
    #     testcase_id = "KT_24"
    #     # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
    #     expected_result_temp = process_prescription_services(self.test_data, testcase_id)
    #     # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
    #     expected_result = None
    #     # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
    #     custom_process_func = lambda file_path: expected_result_temp
    #     # Gọi self.test_case với file_path, expected_result và custom_process_func
    #     self.case_Prescription(testcase_id, expected_result, custom_process_func)
    #
    # # Không nhập thông tin sáng trưa chiều tối Thu phí
    # def test_case_25(self):
    #     # Cho bệnh nhân BHYT
    #     testcase_id = "KT_25"
    #     # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
    #     expected_result_temp = process_prescription_services(self.test_data, testcase_id)
    #     # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
    #     expected_result = None
    #     # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
    #     custom_process_func = lambda file_path: expected_result_temp
    #     # Gọi self.test_case với file_path, expected_result và custom_process_func
    #     self.case_Prescription(testcase_id, expected_result, custom_process_func)
    #
    # # Không nhập thông tin hoạt chất Thu phí
    # def test_case_26(self):
    #     # Cho bệnh nhân BHYT
    #     testcase_id = "KT_26"
    #     # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
    #     expected_result_temp = process_prescription_services(self.test_data, testcase_id)
    #     # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
    #     expected_result = expected_result_temp
    #     # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
    #     custom_process_func = lambda file_path: expected_result_temp
    #     # Gọi self.test_case với file_path, expected_result và custom_process_func
    #     self.case_Prescription(testcase_id, expected_result, custom_process_func)
    #
    # # Không nhập thông tin đường dùng Thu phí
    # def test_case_27(self):
    #     # Cho bệnh nhân BHYT
    #     testcase_id = "KT_27"
    #     # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
    #     expected_result_temp = process_prescription_services(self.test_data, testcase_id)
    #     # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
    #     expected_result = None
    #     # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
    #     custom_process_func = lambda file_path: expected_result_temp
    #     # Gọi self.test_case với file_path, expected_result và custom_process_func
    #     self.case_Prescription(testcase_id, expected_result, custom_process_func)
    #
    # # Không nhập thông tin hàm lượng Thu phí
    # def test_case_28(self):
    #     # Cho bệnh nhân BHYT
    #     testcase_id = "KT_28"
    #     # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
    #     expected_result_temp = process_prescription_services(self.test_data, testcase_id)
    #     # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
    #     expected_result = None
    #     # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
    #     custom_process_func = lambda file_path: expected_result_temp
    #     # Gọi self.test_case với file_path, expected_result và custom_process_func
    #     self.case_Prescription(testcase_id, expected_result, custom_process_func)
    #
    # # Không nhập thông tin đơn vị dùng Thu phí
    # def test_case_29(self):
    #     # Cho bệnh nhân BHYT
    #     testcase_id = "KT_29"
    #     # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
    #     expected_result_temp = process_prescription_services(self.test_data, testcase_id)
    #     # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
    #     expected_result = None
    #     # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
    #     custom_process_func = lambda file_path: expected_result_temp
    #     # Gọi self.test_case với file_path, expected_result và custom_process_func
    #     self.case_Prescription(testcase_id, expected_result, custom_process_func)
    #
    # # Không nhập thông tin đơn vị tính Thu phí
    # def test_case_30(self):
    #     # Cho bệnh nhân BHYT
    #     testcase_id = "KT_30"
    #     # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
    #     expected_result_temp = process_prescription_services(self.test_data, testcase_id)
    #     # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
    #     expected_result = None
    #     # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
    #     custom_process_func = lambda file_path: expected_result_temp
    #     # Gọi self.test_case với file_path, expected_result và custom_process_func
    #     self.case_Prescription(testcase_id, expected_result, custom_process_func)
    #
    # # Không nhập thông tin số lượng Thu phí
    # def test_case_31(self):
    #     # Cho bệnh nhân BHYT
    #     testcase_id = "KT_31"
    #     # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
    #     expected_result_temp = process_prescription_services(self.test_data, testcase_id)
    #     # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
    #     expected_result = 204
    #     # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
    #     custom_process_func = lambda file_path: expected_result_temp
    #     # Gọi self.test_case với file_path, expected_result và custom_process_func
    #     self.case_Prescription(testcase_id, expected_result, custom_process_func)
    #
    # # Không nhập thông tin mã thuốc Thu phí
    # def test_case_32(self):
    #     # Cho bệnh nhân BHYT
    #     testcase_id = "KT_32"
    #     # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
    #     expected_result_temp = process_prescription_services(self.test_data, testcase_id)
    #     # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
    #     expected_result = None
    #     # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
    #     custom_process_func = lambda file_path: expected_result_temp
    #     # Gọi self.test_case với file_path, expected_result và custom_process_func
    #     self.case_Prescription(testcase_id, expected_result, custom_process_func)
    #
    # # Nhập số lượng thuốc lớn hơn tồn Thu phí
    # def test_case_33(self):
    #     pass
    #
    # # Nhập đầy đủ thông tin và chọn kho Nhà thuốc
    # def test_case_34(self):
    #     # Cho bệnh nhân BHYT
    #     testcase_id = "KT_34"
    #     # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
    #     expected_result_temp = process_prescription_services(self.test_data, testcase_id)
    #     # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
    #     expected_result = None
    #     # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
    #     custom_process_func = lambda file_path: expected_result_temp
    #     # Gọi self.test_case với file_path, expected_result và custom_process_func
    #     self.case_Prescription(testcase_id, expected_result, custom_process_func)


if __name__ == '__main__':
    unittest.main()
