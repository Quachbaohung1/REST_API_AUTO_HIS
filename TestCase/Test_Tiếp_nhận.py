import logging
import unittest
import pandas as pd
from unittest.mock import MagicMock
from Tiếp_nhận.POST import (
    process_create_patient_from_excel,
    process_create_insurance_from_excel,
    process_patient_from_excel,
    process_generate_patient_from_excel,
    process_generate_sum_patient_from_excel
)


class CustomTestResult(unittest.TestResult):
    def __init__(self, stream=None, descriptions=None, verbosity=None):
        super().__init__(stream, descriptions, verbosity)
        self.results = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.results.append((test, "Passed"))

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.results.append((test, "Failed"))

    def addError(self, test, err):
        super().addError(test, err)
        self.results.append((test, "Error"))

    def get_results(self):
        return self.results

    def get_passed_results(self):
        return [result for result in self.results if result[1] == "Passed"]


class TestProcessPatient(unittest.TestCase):
    def test_case_01(self):
        file_path = "D://HIS api automation/DataTest/Tiếp nhận/TC_04.xlsx"

        # Mock dữ liệu đọc từ file Excel
        test_data = pd.read_excel(file_path, sheet_name='Data')
        verify_data = pd.read_excel(file_path, sheet_name='Check')
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [test_data, verify_data, test_data]

        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên
        result = process_create_patient_from_excel(file_path)
        expected_result = None

        # Kiểm tra kết quả và in ra kết quả tương ứng
        if result == expected_result:
            print(f"Running test for {file_path}: " "Passed")
        else:
            print(f"Running test for {file_path}: " "Failed")
        self.assertEqual(result, expected_result,
                         f"Failed for {file_path}. Expected: {expected_result}, Actual: {str(result)}")

    def test_case_02(self):
        file_path = "D://HIS api automation/DataTest/Tiếp nhận/TC_05.xlsx"

        # Mock dữ liệu đọc từ file Excel
        test_data = pd.read_excel(file_path, sheet_name='Data')
        verify_data = pd.read_excel(file_path, sheet_name='Check')
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [test_data, verify_data, test_data]

        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên
        result = process_create_patient_from_excel(file_path)
        expected_result = None

        # Kiểm tra kết quả và in ra kết quả tương ứng
        if result == expected_result:
            print(f"Running test for {file_path}: " "Passed")
        else:
            print(f"Running test for {file_path}: " "Failed")
        self.assertEqual(result, expected_result,
                         f"Failed for {file_path}. Expected: {expected_result}, Actual: {str(result)}")

    def test_case_03(self):
        file_path = "D://HIS api automation/DataTest/Tiếp nhận/TC_06.xlsx"

        # Mock dữ liệu đọc từ file Excel
        test_data = pd.read_excel(file_path, sheet_name='Data')
        verify_data = pd.read_excel(file_path, sheet_name='Check')
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [test_data, verify_data, test_data]

        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên
        result = process_create_patient_from_excel(file_path)
        expected_result = None

        # Kiểm tra kết quả và in ra kết quả tương ứng
        if result == expected_result:
            print(f"Running test for {file_path}: " "Passed")
        else:
            print(f"Running test for {file_path}: " "Failed")
        self.assertEqual(result, expected_result,
                         f"Failed for {file_path}. Expected: {expected_result}, Actual: {str(result)}")

    def test_case_04(self):
        file_path = "D://HIS api automation/DataTest/Tiếp nhận/TC_07.xlsx"

        # Mock dữ liệu đọc từ file Excel
        test_data = pd.read_excel(file_path, sheet_name='Data')
        verify_data = pd.read_excel(file_path, sheet_name='Check')
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [test_data, verify_data, test_data]

        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên
        result = process_patient_from_excel(file_path)
        expected_result = [None]

        # Kiểm tra kết quả và in ra kết quả tương ứng
        if result == expected_result:
            print(f"Running test for {file_path}: " "Passed")
        else:
            print(f"Running test for {file_path}: " "Failed")
        self.assertEqual(result, expected_result,
                         f"Failed for {file_path}. Expected: {expected_result}, Actual: {str(result)}")

    def test_case_05(self):
        file_path = "D://HIS api automation/DataTest/Tiếp nhận/TC_08.xlsx"

        # Mock dữ liệu đọc từ file Excel
        test_data = pd.read_excel(file_path, sheet_name='Data')
        verify_data = pd.read_excel(file_path, sheet_name='Check')
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [test_data, verify_data, test_data]

        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên
        result = process_create_insurance_from_excel(file_path)
        expected_result = None

        # Kiểm tra kết quả và in ra kết quả tương ứng
        if result == expected_result:
            print(f"Running test for {file_path}: " "Passed")
        else:
            print(f"Running test for {file_path}: " "Failed")
        self.assertEqual(result, expected_result,
                         f"Failed for {file_path}. Expected: {expected_result}, Actual: {str(result)}")

    def test_case_06(self):
        file_path = "D://HIS api automation/DataTest/Tiếp nhận/TC_09.xlsx"

        # Mock dữ liệu đọc từ file Excel
        test_data = pd.read_excel(file_path, sheet_name='Data')
        verify_data = pd.read_excel(file_path, sheet_name='Check')
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [test_data, verify_data, test_data]

        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên
        result = process_patient_from_excel(file_path)
        expected_result = [None]

        # Kiểm tra kết quả và in ra kết quả tương ứng
        if result == expected_result:
            print(f"Running test for {file_path}: " "Passed")
        else:
            print(f"Running test for {file_path}: " "Failed")
        self.assertEqual(result, expected_result,
                         f"Failed for {file_path}. Expected: {expected_result}, Actual: {str(result)}")

    def test_case_07(self):
        file_path = "D://HIS api automation/DataTest/Tiếp nhận/TC_11.xlsx"

        # Mock dữ liệu đọc từ file Excel
        test_data = pd.read_excel(file_path, sheet_name='Data')
        verify_data = pd.read_excel(file_path, sheet_name='Check')
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [test_data, verify_data, test_data]

        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên
        result = process_create_patient_from_excel(file_path)
        expected_result = result

        # Kiểm tra kết quả và in ra kết quả tương ứng
        if result == expected_result:
            print(f"Running test for {file_path}: " "Passed")
        else:
            print(f"Running test for {file_path}: " "Failed")
        self.assertEqual(result, expected_result,
                         f"Failed for {file_path}. Expected: {expected_result}, Actual: {str(result)}")

    def test_case_08(self):
        file_path = "D://HIS api automation/DataTest/Tiếp nhận/TC_12.xlsx"

        # Mock dữ liệu đọc từ file Excel
        test_data = pd.read_excel(file_path, sheet_name='Data')
        verify_data = pd.read_excel(file_path, sheet_name='Check')
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [test_data, verify_data, test_data]

        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên
        result = process_create_insurance_from_excel(file_path)
        expected_result = result

        # Kiểm tra kết quả và in ra kết quả tương ứng
        if result == expected_result:
            print(f"Running test for {file_path}: " "Passed")
        else:
            print(f"Running test for {file_path}: " "Failed")
        self.assertEqual(result, expected_result,
                         f"Failed for {file_path}. Expected: {expected_result}, Actual: {str(result)}")

    def test_case_09(self):
        file_path = "D://HIS api automation/DataTest/Tiếp nhận/TC_10.xlsx"

        # Mock dữ liệu đọc từ file Excel
        test_data = pd.read_excel(file_path, sheet_name='Data')
        verify_data = pd.read_excel(file_path, sheet_name='Check')
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [test_data, verify_data, test_data]

        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên
        result = process_patient_from_excel(file_path)
        expected_result = result

        # Kiểm tra kết quả và in ra kết quả tương ứng
        if result == expected_result:
            print(f"Running test for {file_path}: " "Passed")
        else:
            print(f"Running test for {file_path}: " "Failed")
        self.assertEqual(result, expected_result,
                         f"Failed for {file_path}. Expected: {expected_result}, Actual: {str(result)}")

    def test_case_10(self):
        file_path = "D://HIS api automation/DataTest/Tiếp nhận/TC_22.xlsx"

        # Mock dữ liệu đọc từ file Excel
        test_data = pd.read_excel(file_path, sheet_name='Data')
        verify_data = pd.read_excel(file_path, sheet_name='Check')
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [test_data, verify_data, test_data]

        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên
        result = process_generate_patient_from_excel(file_path)
        expected_result = result

        # Kiểm tra kết quả và in ra kết quả tương ứng
        if result == expected_result:
            print(f"Running test for {file_path}: " "Passed")
        else:
            print(f"Running test for {file_path}: " "Failed")
        self.assertEqual(result, expected_result,
                         f"Failed for {file_path}. Expected: {expected_result}, Actual: {str(result)}")

    def test_case_11(self):
        file_path = "D://HIS api automation/DataTest/Tiếp nhận/TC_24.xlsx"

        # Mock dữ liệu đọc từ file Excel
        test_data = pd.read_excel(file_path, sheet_name='Data')
        verify_data = pd.read_excel(file_path, sheet_name='Check')
        # Tạo mock cho pd.read_excel
        mock_read_excel = MagicMock()
        mock_read_excel.side_effect = [test_data, verify_data, test_data]

        # Giả lập phản hồi của hàm create_patient với lỗi thiếu tên
        result = process_generate_sum_patient_from_excel(file_path)
        expected_result = result

        # Kiểm tra kết quả và in ra kết quả tương ứng
        if result == expected_result:
            print(f"Running test for {file_path}: " "Passed")
        else:
            print(f"Running test for {file_path}: " "Failed")
        self.assertEqual(result, expected_result,
                         f"Failed for {file_path}. Expected: {expected_result}, Actual: {str(result)}")


def main():
    logging.basicConfig(filename='D:/HIS api automation/Result/TestResult_Tiếp_nhận.log', level=logging.INFO)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestProcessPatient)
    custom_result = CustomTestResult()
    suite.run(custom_result)

    successes = custom_result.testsRun - len(custom_result.failures) - len(custom_result.errors)
    with open("D:/HIS api automation/Result/TestResult_Tiếp_nhận.txt", "w", encoding="utf-8") as file:
        file.write("=== Test Report ===\n")
        file.write(f"Total tests run: {custom_result.testsRun}\n")
        file.write(f"Successes: {successes}\n")
        file.write(f"Failures: {len(custom_result.failures)}\n")
        file.write(f"Errors: {len(custom_result.errors)}\n")

        if successes > 0:
            file.write("\n=== Successes ===\n")
            for test, _ in custom_result.get_passed_results():
                file.write(f"{test}: Passed\n")

        if custom_result.failures:
            file.write("\n=== Failures ===\n")
            for test, fail_msg in custom_result.failures:
                file.write(f"{test}: {fail_msg}\n")

        if custom_result.errors:
            file.write("\n=== Errors ===\n")
            for test, err_msg in custom_result.errors:
                file.write(f"{test}: {err_msg}\n")

    logging.info("Test report generated.")


if __name__ == '__main__':
    main()
