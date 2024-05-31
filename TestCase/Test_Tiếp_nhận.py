import unittest
import pandas as pd
from Tiếp_nhận.POST import process_patient_from_excel, generate_additional_data, write_data_to_excel, \
    create_patient_from_excel, create_insurance_from_excel, create_visit_from_excel


class TestProcessPatientFromExcel(unittest.TestCase):
    def test_process_patient_from_excel(self):
        file_path = "D://HIS api automation/DataTest/Data_API_Tiếp_nhận.xlsx"
        sheet_name = "Sheet1"

        # Đọc dữ liệu gốc từ tệp Excel
        excel_data = pd.read_excel(file_path, sheet_name=sheet_name)

        # Tạo dữ liệu bổ sung và ghi vào file Excel
        num_records_to_add = 2  # Số dòng dữ liệu bổ sung
        additional_data = generate_additional_data(excel_data.tail(1), num_records_to_add)
        write_data_to_excel(file_path, sheet_name, additional_data)

        # Đọc lại dữ liệu đã ghi vào file
        additional_data = pd.read_excel(file_path, sheet_name=sheet_name)

        entry_ids = []  # Danh sách để lưu các entry_id
        for index, row in additional_data.iterrows():
            patient_id = create_patient_from_excel(row)
            if int(row["InsBenefitType"]) == 2:
                create_insurance_from_excel(row, patient_id)
            entry_id = create_visit_from_excel(row, patient_id)
            entry_ids.append(entry_id)  # Lưu entry_id vào danh sách

        print("entry_ids", entry_ids)
        return entry_ids  # Trả về danh sách các entry_id


if __name__ == '__main__':
    unittest.main()