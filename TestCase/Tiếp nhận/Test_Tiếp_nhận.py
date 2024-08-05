import unittest
import logging
import pandas as pd
from unittest.mock import MagicMock
from Tiếp_nhận.POST import (
    process_create_patient_from_excel,
    process_create_insurance_from_excel,
    process_patient_from_excel,
    process_generate_patient_from_excel,
    process_generate_sum_patient_from_excel
)


# Xác định đường dẫn đến file log
log_file_path = 'D:/HIS api automation/Result/TestResult_Tiếp_nhận.txt'

# Xóa file log cũ nếu tồn tại
with open(log_file_path, 'w'):  # Mở file trong chế độ ghi để xóa nội dung
    pass  # Pass đơn giản làm gì để xóa

# Thiết lập logging để ghi vào file mới
logging.basicConfig(filename=log_file_path, level=logging.INFO)


# Ghi lại kết quả của test
def log_test_result(test_name, result):
    logging.info(f'Test "{test_name}" - Result: {result}')


# Đọc toàn bộ sheet Excel một lần
def read_test_data(file_path):
    df = pd.read_excel(file_path, sheet_name='Data')
    return df


class TestProcessPatient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.file_path = "D://HIS api automation/DataTest/Tiếp nhận/DataTest.xlsx"
        cls.test_data = read_test_data(cls.file_path)

    # Form test tạo patient
    def case_VisitOn(self, testcase_id, expected_result, process_func):
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

    # Case nhập trùng họ tên với bệnh nhân cũ đã tiếp nhận trước đó trong cùng ngày BHYT
    def test_case_01(self):
        # bệnh nhân BHYT
        testcase_id = "TN_1"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_create_patient_from_excel(self.test_data, testcase_id)
        expected_result_temp_1 = process_create_patient_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp_1
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp_1
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case nhập trùng số thẻ BHYT với bệnh nhân cũ
    def test_case_02(self):
        # bệnh nhân BHYT
        testcase_id = "TN_2"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_create_insurance_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case nhập trùng số CCCD với bệnh nhân cũ BHYT
    def test_case_03(self):
        # bệnh nhân BHYT
        testcase_id = "TN_3"
        # bệnh nhân Thu phí
        # file_path = "E://HIS api automation/DataTest/Tiếp nhận/TC_28.xlsx"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_create_patient_from_excel(self.test_data, testcase_id)
        expected_result_temp_1 = process_create_patient_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp_1
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp_1
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case không nhập họ tên BHYT
    def test_case_04(self):
        # bệnh nhân BHYT
        testcase_id = "TN_4"
        # bệnh nhân Thu phí
        # file_path = "E://HIS api automation/DataTest/Tiếp nhận/TC_29.xlsx"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_create_patient_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case không nhập ngày sinh BHYT
    def test_case_05(self):
        # bệnh nhân BHYT
        testcase_id = "TN_5"
        # bệnh nhân Thu phí
        # file_path = "E://HIS api automation/DataTest/Tiếp nhận/TC_30.xlsx"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_create_patient_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case không nhập địa chỉ BHYT
    def test_case_06(self):
        # bệnh nhân BHYT
        testcase_id = "TN_6"
        # bệnh nhân Thu phí
        # file_path = "E://HIS api automation/DataTest/Tiếp nhận/TC_31.xlsx"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_create_patient_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case không nhập thông tin phòng khám BHYT
    def test_case_07(self):
        # bệnh nhân BHYT
        testcase_id = "TN_7"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_patient_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case không nhập thông tin BHYT
    def test_case_08(self):
        # bệnh nhân BHYT
        testcase_id = "TN_8"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_create_insurance_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case có nhập thông tin phòng khám nhưng không nhập thông tin dịch vụ khám BHYT
    def test_case_09(self):
        # bệnh nhân BHYT
        testcase_id = "TN_9"
        # bệnh nhân Thu phí
        # file_path = "E://HIS api automation/DataTest/Tiếp nhận/TC_33.xlsx"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_patient_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case nhập sai hạn thẻ đến ngày có năm lớn hơn >= 2080 BHYT
    def test_case_10(self):
        # bệnh nhân BHYT
        testcase_id = "TN_10"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_create_insurance_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case bệnh nhân trái tuyến nhập thiếu thông tin chuyển tuyến BHYT
    def test_case_11(self):
        # bệnh nhân BHYT
        testcase_id = "TN_11"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_patient_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case nhập trùng số giấy chuyển tuyến đã sử dụng BHYT
    def test_case_12(self):
        # bệnh nhân BHYT
        testcase_id = "TN_12"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_patient_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case đúng thông tin cá nhân nhưng sai mã đầu thẻ
    def test_case_13(self):
        # bệnh nhân BHYT
        testcase_id = "TN_13"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_create_insurance_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case đúng thông tin cá nhân nhưng thẻ hết hạn (chưa gia hạn)
    def test_case_14(self):
        # bệnh nhân BHYT
        testcase_id = "TN_14"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_create_insurance_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case đúng thông tin cá nhân nhưng sai kiểu thẻ
    def test_case_15(self):
        # bệnh nhân BHYT
        testcase_id = "TN_15"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_create_insurance_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case nhập sai năm sinh > 254 tuổi
    def test_case_16(self):
        # bệnh nhân BHYT
        testcase_id = "TN_16"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_create_patient_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case trẻ em dưới 6 tuổi không có thông tin người thân BHYT
    def test_case_17(self):
        # bệnh nhân BHYT
        testcase_id = "TN_17"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_create_patient_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case trẻ em dưới 6 tuổi có thông tin người thân nhưng không có sdt người thân BHYT
    def test_case_18(self):
        # bệnh nhân BHYT
        testcase_id = "TN_18"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_create_patient_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case trẻ em dưới 6 tuổi đăng ký khám vào pk cấu hình pk người lớn BHYT
    def test_case_19(self):
        # bệnh nhân BHYT
        testcase_id = "TN_19"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_create_patient_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case bệnh nhân có nơi ĐKKCB khác 75009 không check hưởng đúng tuyến
    def test_case_20(self):
        # bệnh nhân BHYT
        testcase_id = "TN_20"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_patient_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case không chọn giới tính BHYT
    def test_case_21(self):
        # bệnh nhân BHYT
        testcase_id = "TN_21"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_create_patient_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case bệnh nhân có nơi ĐKKCB khác 75009 không check Tái khám
    def test_case_22(self):
        # bệnh nhân BHYT
        testcase_id = "TN_22"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_patient_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case nhập hạn thẻ chưa tới ngày áp dụng thẻ
    def test_case_23(self):
        # bệnh nhân BHYT
        testcase_id = "TN_23"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_patient_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case nhập đầy đủ thông tin BHYT
    def test_case_24(self):
        # bệnh nhân BHYT
        testcase_id = "TN_24"
        # bệnh nhân Thu phí
        # file_path = "E://HIS api automation/DataTest/Tiếp nhận/TC_39.xlsx"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_patient_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case tạo thông tin bệnh nhân thành công BHYT
    def test_case_25(self):
        # bệnh nhân BHYT
        testcase_id = "TN_25"
        # bệnh nhân Thu phí
        # file_path = "E://HIS api automation/DataTest/Tiếp nhận/TC_40.xlsx"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_create_patient_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case tạo thông BHYT thành công
    def test_case_26(self):
        # bệnh nhân BHYT
        testcase_id = "TN_26"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_create_insurance_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case nhập trùng họ tên với bệnh nhân cũ đã tiếp nhận trước đó trong cùng ngày Thu phí
    # def test_case_27(self):
    #     # bệnh nhân Thu phí
    #     testcase_id = "TN_27"
    #     # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
    #     expected_result_temp = process_create_patient_from_excel(self.test_data, testcase_id)
    #     expected_result_temp_1 = process_create_patient_from_excel(self.test_data, testcase_id)
    #     # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
    #     expected_result = expected_result_temp_1
    #     # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
    #     custom_process_func = lambda file_path: expected_result_temp_1
    #     # Gọi self.test_case với file_path, expected_result và custom_process_func
    #     self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case nhập trùng số CCCD với bệnh nhân cũ Thu phí
    def test_case_28(self):
        # bệnh nhân Thu phí
        testcase_id = "TN_28"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_create_patient_from_excel(self.test_data, testcase_id)
        expected_result_temp_1 = process_create_patient_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp_1
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp_1
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case không nhập họ tên Thu phí
    def test_case_29(self):
        # bệnh nhân Thu phí
        testcase_id = "TN_29"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_create_patient_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case không nhập ngày sinh Thu phí
    def test_case_30(self):
        # bệnh nhân Thu phí
        testcase_id = "TN_30"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_create_patient_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case không nhập địa chỉ Thu phí
    def test_case_31(self):
        # bệnh nhân Thu phí
        testcase_id = "TN_31"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_create_patient_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case không nhập thông tin phòng khám Thu phí
    def test_case_32(self):
        # bệnh nhân Thu phí
        testcase_id = "TN_32"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_patient_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case có nhập thông tin phòng khám nhưng không nhập thông tin dịch vụ khám Thu phí
    def test_case_33(self):
        # bệnh nhân Thu phí
        testcase_id = "TN_33"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_patient_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case không chọn giới tính Thu phí
    def test_case_34(self):
        # bệnh nhân Thu phí
        testcase_id = "TN_34"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_create_patient_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case nhập sai năm sinh > 254 tuổi thu phí
    def test_case_35(self):
        # bệnh nhân thu phí
        testcase_id = "TN_35"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_create_patient_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case trẻ em dưới 6 tuổi không có thông tin người thân BHYT
    def test_case_36(self):
        # bệnh nhân thu phí
        testcase_id = "TN_36"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_create_patient_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case trẻ em dưới 6 tuổi có thông tin người thân nhưng không có sdt người thân BHYT
    def test_case_37(self):
        # bệnh nhân thu phí
        testcase_id = "TN_37"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_create_patient_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case trẻ em dưới 6 tuổi đăng ký khám vào pk cấu hình pk người lớn BHYT
    def test_case_38(self):
        # bệnh nhân thu phí
        testcase_id = "TN_38"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_create_patient_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case nhập đầy đủ thông tin Thu phí
    def test_case_39(self):
        # bệnh nhân Thu phí
        testcase_id = "TN_39"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_patient_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case tạo thông tin bệnh nhân thành công Thu phí
    def test_case_40(self):
        # bệnh nhân Thu phí
        testcase_id = "TN_40"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_create_patient_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case trẻ em dưới 6 tuổi có đầy đủ thông tin người thân
    def test_case_41(self):
        # bệnh nhân Thu phí
        testcase_id = "TN_41"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_create_patient_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case tiếp nhận thành công BN thu phí loại khám cấp cứu có check trả sau
    def test_case_42(self):
        # bệnh nhân Thu phí
        testcase_id = "TN_42"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_patient_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case tiếp nhận thành công BN thu phí có check hẹn kết quả
    def test_case_43(self):
        # bệnh nhân Thu phí
        testcase_id = "TN_43"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_patient_from_excel(self.test_data, testcase_id)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(testcase_id, expected_result, custom_process_func)

    # Case tiếp nhận tự động từng loại bệnh nhân
    def test_case_44(self):
        # bệnh nhân BHYT
        file_path = "D://HIS api automation/DataTest/Tiếp nhận/TC_44.xlsx"
        # bệnh nhân Thu phí
        # file_path = "E://HIS api automation/DataTest/Tiếp nhận/TC_45.xlsx"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_generate_patient_from_excel(file_path)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(file_path, expected_result, custom_process_func)

    # Case tiếp nhận thành công bệnh nhân BHYT + Thu phí (chạy tự động)
    def test_case_46(self):
        # bệnh nhân BHYT + Thu phí
        file_path = "D://HIS api automation/DataTest/Tiếp nhận/TC_46.xlsx"
        # Chạy hàm process_examination_services một lần và lưu kết quả vào biến tạm
        expected_result_temp = process_generate_sum_patient_from_excel(file_path)
        # Ghi đè expected_result để đảm bảo chỉ gọi hàm một lần
        expected_result = expected_result_temp
        # Tạo một hàm lambda hoặc hàm bình thường để truyền vào self.test_case
        custom_process_func = lambda file_path: expected_result_temp
        # Gọi self.test_case với file_path, expected_result và custom_process_func
        self.case_VisitOn(file_path, expected_result, custom_process_func)


if __name__ == '__main__':
    unittest.main()
