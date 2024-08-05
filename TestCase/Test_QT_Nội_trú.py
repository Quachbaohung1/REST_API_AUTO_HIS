import json
import threading
from concurrent.futures import ThreadPoolExecutor
import unittest
import logging
import pandas as pd
from unittest.mock import MagicMock
from Tiếp_nhận.POST import process_generate_patient_from_excel
from Khám_bệnh_CDDV.POST import process_examination_services_NT
from Khám_bệnh_Toa_thuốc.POST import process_prescription_services
from Viện_phí.POST import process_VP
from Khám_bệnh_Nhập_viện.PUT import update_hospitalize_patient_from_excel
from Nội_trú.POST import process_NT, create_ExamFollowups
from Nội_trú.PUT import discharged_hospital, data_of_discharged_hospital

# Xác định đường dẫn đến file log
log_file_path = 'D://HIS api automation/Result/TestResult_Full.txt'

# Xóa file log cũ nếu tồn tại
with open(log_file_path, 'w'):  # Mở file trong chế độ ghi để xóa nội dung
    pass  # Pass đơn giản làm gì để xóa

# Thiết lập logging để ghi vào file mới
logging.basicConfig(filename=log_file_path, level=logging.INFO)

# Semaphore để đồng bộ hóa truy cập vào hàm process_generate_patient_from_excel
api_semaphore = threading.Semaphore(1)


# Ghi lại kết quả của test
def log_test_result(test_name, result, error=None):
    if result == "Failed" and error:
        logging.error(f'Test "{test_name}" - Result: {result} - Error: {error}')
    else:
        logging.info(f'Test "{test_name}" - Result: {result}')


# Đọc toàn bộ sheet Excel một lần
def read_test_data(file_path):
    df = pd.read_excel(file_path, sheet_name='Data')
    return df


class TestProcessPatient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.file_paths = [
            "D://HIS api automation/DataTest/Tiếp nhận/TC_44_Test.xlsx",
            # "D://HIS api automation/DataTest/Tiếp nhận/TC_44_Test_1.xlsx",
            # "D://HIS api automation/DataTest/Tiếp nhận/TC_44_Test_2.xlsx",
            # "D://HIS api automation/DataTest/Tiếp nhận/TC_44_Test_3.xlsx",
        ]
        cls.results = {}  # Dictionary để lưu kết quả của từng file
        cls.entry_ids = {}  # Dictionary để lưu entryId của từng file
        cls.patientCodes = {}   # Dictionary để lưu patientCode của từng file
        cls.frVisitEntryIds = {}
        cls.result_apis_KT = {}
        cls.VPDatas = {}
        cls.result_apis_NV = {}

    def process_file(self, file_path):
        # Đọc dữ liệu từ file Excel
        test_data = read_test_data(file_path)

        # Định nghĩa testcase_id từ test_data hoặc một cách thích hợp
        testcase_CDDV = "CDDV_19"
        # testcase_KT = "KT_20"
        testcase_VP = "VP_1"
        testcase_NV = "NV_01"
        testcase_NT = "NT_01"

        # Mock đối tượng pd.read_excel
        mock_read_excel = MagicMock(return_value=test_data)

        # Chạy hàm được kiểm thử với Semaphore
        with api_semaphore:
            # Hàm tiếp nhận bệnh nhân
            entry_ids, patientCodes, response_data = process_generate_patient_from_excel(file_path)
            # Đọc dữ liệu từ file riêng cho hospitalize_services
            hospitalize_data_file = "D://HIS api automation/DataTest/Nhập viện/TC_01.xlsx"
            hospitalize_data = read_test_data(hospitalize_data_file)
            # Hàm nhập viện
            result_apis_NV = update_hospitalize_patient_from_excel(hospitalize_data, testcase_NV, entry_ids)
            # Đọc dữ liệu từ file riêng cho Nội trú
            NT_data_file = "D://HIS api automation/DataTest/Nội trú/TC_01.xlsx"
            NT_data = read_test_data(NT_data_file)
            # Hàm Nội trú
            txVisitIds, wardAdmIds, medRcdIds, Medrecords_jsons = process_NT(NT_data, testcase_NT, entry_ids)
            # Đọc dữ liệu từ file riêng cho process_examination_services
            examination_data_file = "D://HIS api automation/DataTest/Khám bệnh - CDDV/TC_01.xlsx"
            examination_data = read_test_data(examination_data_file)
            # Hàm chỉ định dịch vụ
            frVisitEntryIds, all_datas = process_examination_services_NT(examination_data, testcase_CDDV, entry_ids, txVisitIds, wardAdmIds)
            # Hàm trả kết quả CLS

            # Hàm trả kết quả thủ thuật

            # # Đọc dữ liệu từ file riêng cho process_prescription_services
            # prescription_data_file = "../DataTest/Khám bệnh - Kê thuốc/TC_01.xlsx"
            # prescription_data = read_test_data(prescription_data_file)
            # # Hàm kê thuốc (Có thể là thuốc BHYT or Nhà thuốc)
            # result_apis_KT = process_prescription_services(prescription_data, testcase_KT, entry_ids)

            # Hàm thanh toán và phát thuốc Nhà thuốc

            # Hàm xuất viện
            Discharged_hospital_data = data_of_discharged_hospital(Medrecords_jsons)

            # for Discharged_hospital_data_a in Discharged_hospital_data:
            #     Discharged_hospital_datas = json.dumps(Discharged_hospital_data_a)
            discharged_hospital(Discharged_hospital_data)

            create_ExamFollowups(medRcdIds)
            # Đọc dữ liệu từ file riêng cho process_VP
            VP_data_file = "D://HIS api automation/DataTest/Viện_phí/TC_01.xlsx"
            VP_data = read_test_data(VP_data_file)
            file_path_VP = "D://HIS api automation/DataTest/Data_API_Khám_bệnh.xlsx"
            # file_path_VP = read_test_data(file_path_VP_file)

            # Hàm viện phí
            VPDatas = process_VP(VP_data, file_path_VP, testcase_VP, patientCodes)
            # Hàm phát thuốc BHYT

        # Kiểm tra kết quả và lưu entryId và patientCode vào dictionary
        if patientCodes and entry_ids and frVisitEntryIds and VPDatas and result_apis_NV:  # Kiểm tra nếu patientCodes và entry_ids không trống
            self.entry_ids[file_path] = entry_ids
            self.result_apis_NV[file_path] = result_apis_NV
            self.patientCodes[file_path] = patientCodes
            self.frVisitEntryIds[file_path] = frVisitEntryIds
            # self.result_apis_KT[file_path] = result_apis
            self.VPDatas[file_path] = VPDatas
            self.results[file_path] = True
        else:
            self.results[file_path] = False

    def test_run_multiple_tests(self):
        # Chạy từng test case và lưu kết quả
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(self.process_file, file_path): file_path for file_path in self.file_paths}

            for future in futures:
                file_path = futures[future]
                try:
                    future.result()
                except Exception as e:
                    print(f"Exception for {file_path}: {e}")
                    self.results[file_path] = False
                    log_test_result(f"Running test for {file_path}", "Failed", error=str(e))

        # So sánh kết quả mong đợi sau khi chạy hết các test case
        expected_results = {file_path: True for file_path in self.file_paths}  # Giả sử kết quả mong đợi là True cho mỗi file
        for file_path, result in self.results.items():
            if result == expected_results[file_path]:
                print(f"Test for {file_path}: Passed")
                log_test_result(f"Running test for {file_path}", "Passed")
            else:
                print(f"Test for {file_path}: Failed")
                log_test_result(f"Running test for {file_path}", "Failed", error="Mismatched results")
            self.assertEqual(result, expected_results[file_path],
                             f"Failed for {file_path}. Expected: {expected_results[file_path]}, Actual: {str(result)}")

        # In ra toàn bộ entryId sau khi đã chạy xong hết các test case
        print("\nEntryIds:")
        if self.entry_ids:  # Kiểm tra nếu self.entry_ids không trống
            for file_path, entry_id_list in self.entry_ids.items():
                print(f"{file_path}: {entry_id_list}")
        else:
            print("No entry IDs were captured.")

        # In ra toàn bộ patientCode sau khi đã chạy xong hết các test case
        print("\nPatientCodes:")
        if self.patientCodes:  # Kiểm tra nếu self.patientCodes không trống
            for file_path, patientCode_list in self.patientCodes.items():
                print(f"{file_path}: {patientCode_list}")
        else:
            print("No patient codes were captured.")

        # In ra toàn bộ frVisitEntryId sau khi đã chạy xong hết các test case
        print("\nFrVisitEntryIds:")
        if self.frVisitEntryIds:  # Kiểm tra nếu self.patientCodes không trống
            for file_path, frVisitEntryId_list in self.frVisitEntryIds.items():
                print(f"{file_path}: {frVisitEntryId_list}")
        else:
            print("No frVisitEntryIds were captured.")


if __name__ == '__main__':
    unittest.main()
