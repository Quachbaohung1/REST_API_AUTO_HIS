import requests
import pandas as pd
import datetime
import re
from copy import deepcopy
from Tiếp_nhận import GET

# Base url
base_url = "http://115.79.31.186:1096"

# Auth token
auth_token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IjM4MzkiLCJyb2xlIjoiQWRtaW4iLCJBY2NvdW50TmFtZSI6Imh1bmdxYiIsIkNsaWVudElwQWRkcmVzcyI6Ijo6MSIsIklzTG9jYWxJcCI6IlRydWUiLCJuYmYiOjE3MTUxODQ2NDIsImV4cCI6MTcxNTE4ODI0MiwiaWF0IjoxNzE1MTg0NjQyfQ.CihuC246iqFUos4MNZtNWs2q_SBOtmbXz4NRNuRQ4rg"

# POST request
def create_patient(data):
    url = f"{base_url}/pms/Patients"
    headers = {"Authorization": auth_token}
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()["patientId"]

def create_insurance(data, dob):
    url = f"{base_url}/pms/PatientInsurances/?dateOfBirth={dob}"
    headers = {"Authorization": auth_token}
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()["patientId"]

def create_visit(data, visit_on):
    url = f"{base_url}/pms/Visits/?visitOn={visit_on}&noSetProcessingPending=False&isPassCreatePaymentTicket=False&isPassVisitOnSameDay=False"
    headers = {"Authorization": auth_token}
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()

def create_patient_from_excel(row):
    full_name = row['LastName'] + " " + str(int(row['FirstName']))
    IdCardNo = "0" + str(int(row['IdCardNo']))
    MobileNo = "0" + str(int(row['MobileNo']))
    RelativePhone = "0" + str(int(row['RelativePhone']))
    # Kiểm tra nếu giá trị của cột TaxCode là NaN
    if pd.isna(row['TaxCode']):
        tax_code = ''  # hoặc tax_code = 'null' nếu bạn muốn lưu giá trị 'null' (dạng chuỗi)
    else:
        tax_code = str(row['TaxCode'])
    Ethnic = "0" + str(int(row['Ethnic']))
    patient_data = {
        "PatientCode": "SimulatedCode",
        "FullPatientCode": "SimulatedCode",
        "FirstName": str(int(row['FirstName'])),
        "LastName": row['LastName'],
        "Dob": str(row['Dob']),
        "Gender": int(row['Gender']),
        "IdCardNo": IdCardNo,
        "MobileNo": MobileNo,
        "Nationality": str(row['Nationality']),
        "Ethnic": Ethnic,
        "Country": str(row['Country']),
        "City": str(int(row['City'])),
        "District": str(int(row['District'])),
        "Ward": str(int(row['Ward'])),
        "Address": str(row['Address']),
        "Occupation": row['Occupation'],
        "EmployerName": str(row['EmployerName']),
        "EmployerAddr": str(row['EmployerAddr']),
        "TaxCode": tax_code,
        "RelativeName": str(row['RelativeName']),
        "RelativeAddr": str(row['RelativeAddr']),
        "RelativePhone": RelativePhone,
        "RelativeType": row['RelativeType'],
        "Status": row['Status'],
        "FullName": full_name,
        "FullAddress": str(row['FullAddress'])
    }
    return create_patient(patient_data)

def create_insurance_from_excel(row, patient_id):
    if pd.isna(row['Provider']):
        provider = ''  # hoặc tax_code = 'null' nếu bạn muốn lưu giá trị 'null' (dạng chuỗi)
    else:
        provider = str(row['Provider'])
    if pd.isna(row['FullInsOn']):
        FullInsOn = ''  # hoặc tax_code = 'null' nếu bạn muốn lưu giá trị 'null' (dạng chuỗi)
    else:
        FullInsOn = str(row['FullInsOn'])
    dob_datetime = datetime.datetime.strptime(row["Dob"], "%Y-%m-%dT%H:%M:%S%z")
    dob = dob_datetime.strftime("%Y%m%d")
    insurance_data = {
        "PatientId": patient_id,
        "InsCardNo": str(row['InsCardNo']),
        "InsName": str(row['InsName']),
        "StartDate": str(row['StartDate']),
        "EndDate": str(row['EndDate']),
        "MedProviderId": int(row['MedProviderId']),
        "Address": str(row['Address']),
        "Country": str(row['Country']),
        "City": str(int(row['City'])),
        "District": str(int(row['District'])),
        "Ward": str(int(row['Ward'])),
        "InsZone": int(row['InsZone']),
        "Status": row['Status'],
        "Attribute": int(row['Attribute']),
        "Provider": provider,
        "IsDisabled": str(row['IsDisabled']),
        "IsTemp": str(row['IsTemp']),
        "FullInsOn": FullInsOn
    }
    create_insurance(insurance_data, dob)

def create_visit_from_excel(row, patient_id):
    full_name = row['LastName'] + " " + str(int(row['FirstName']))
    Ethnic = "0" + str(int(row['Ethnic']))

    visit_on = str(GET.CurrentServerDateTime())
    visit_on_value_trimmed1 = visit_on.replace('"', '')
    visit_on_value_trimmed = visit_on[:20] + "+" + visit_on[-6:]
    isit_on_value_trimmed = visit_on_value_trimmed.replace('"', '')

    visit_on_datetime = datetime.datetime.strptime(isit_on_value_trimmed, "%Y-%m-%dT%H:%M:%S%z")
    Formated_visit_on = visit_on_datetime.strftime("%Y%m%d%H%M%S")
    if pd.isna(row['InsCheckedStatus']):
        InsCheckedStatus = ''
    else:
        InsCheckedStatus = int(row['InsCheckedStatus'])
    visit_on = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    visit_data = {
        "ReceiveType": int(row['ReceiveType']),
        "RcvState": int(row['RcvState']),
        "RxTypeIn": int(row['RxTypeIn']),
        "VisitOn": visit_on_value_trimmed1,
        "PatientId": patient_id,
        "PtName": full_name,
        "PtAge": int(row['PtAge']),
        "PtGender": int(row['Gender']),
        "PtDob": str(row['Dob']),
        "PtAddress": str(row['Address']),
        "PtDistrict": str(int(row['District'])),
        "PtWard": str(int(row['Ward'])),
        "PtEthnic": Ethnic,
        "PtNationality": str(row['Nationality']),
        "PtOccupation": row['Occupation'],
        "InsCardNo": str(row['InsCardNo']),
        "InsBenefitType": int(row['InsBenefitType']),
        "InsBenefitRatio": int(row['InsBenefitRatio']),
        "Attribute": int(row['Attribute']),
        "FileStoreNo": "",
        "CreateById": int(row['CreateById']),
        "Status": row['Status'],
        "InsCheckedMessage": str(row['InsCheckedMessage']),
        "InsCheckedStatus": InsCheckedStatus,
        "Entry": {
            "MedServiceId": int(row['MedServiceId']),
            "WardUnitId": int(row['WardUnitId']),
            "OnDate": visit_on_value_trimmed1,
            "CreateById": int(row['CreateById']),
            "Status": row['Status'],
            "InsBenefitType": int(row['InsBenefitType']),
            "InsBenefitRatio": int(row['InsBenefitRatio']),
            "PriceId": int(row['PriceId']),
            "CreateByWardUnitId": int(row['CreateByWardUnitId']),
            "Service": None,
            "LabExams": None,
            "CreatedBy": None,
            "ContentHash": row['ContentHash']
        },
        "FullPatientCode": None,
        "InsBenefitTypeName": None,
        "WardUnitNames": None,
        "CreateByStaffName": None,
        "ContentHash": row['ContentHash1'],
        "LastUpdateByStaffName": None,
        "ModifiedOn": None
    }
    # Kiểm tra xem loại bảo hiểm có phải là BHYT hay không
    if int(row["InsBenefitType"]) == 2:
        # Nếu là BHYT, hiển thị "InsCheckedMessage" và "InsCheckedStatus"
        InsCheckedStatus = int(row['InsCheckedStatus']) if not pd.isna(row['InsCheckedStatus']) else None
        visit_data["InsCheckedMessage"] = str(row['InsCheckedMessage'])
        visit_data["InsCheckedStatus"] = InsCheckedStatus
    else:
        # Nếu không phải là BHYT, loại bỏ các trường "InsCheckedMessage" và "InsCheckedStatus"
        del visit_data["InsCheckedMessage"]
        del visit_data["InsCheckedStatus"]
        del visit_data["InsCardNo"]
    response_json = create_visit(visit_data, Formated_visit_on)
    # Kiểm tra và trích xuất entryId từ phản hồi JSON
    entry_id = None
    if response_json and "entry" in response_json and "entryId" in response_json["entry"]:
        entry_id = response_json["entry"]["entryId"]

    # In giá trị
    print("entryId:", entry_id)

    # Return các giá trị
    return entry_id


def extract_numeric_suffix(s):
    """Extracts the numeric suffix from a string, if any."""
    match = re.search(r'(\d+)$', s)
    return int(match.group(1)) if match else 0

def increment_string(prefix, counter):
    """Generates a new string by incrementing the counter."""
    return f"{prefix}{counter}"

def generate_additional_data(original_data, num_records):
    new_data = []

    # Tạo các biến lưu trữ giá trị ban đầu cho mỗi cột
    max_first_name = original_data["FirstName"].max() if not original_data.empty else 0
    max_id_card_no = original_data["IdCardNo"].max() if not original_data.empty else 0
    ins_card_no_prefix = re.sub(r'\d+$', '', original_data["InsCardNo"].iloc[0]) if not original_data.empty else ""
    max_ins_card_no = original_data["InsCardNo"].apply(extract_numeric_suffix).max() if not original_data.empty else 0

    for _ in range(num_records):
        for _, row in original_data.iterrows():
            new_row = deepcopy(row)

            # Sử dụng các giá trị hiện tại cho mỗi dòng dữ liệu mới
            new_row["FirstName"] = max_first_name + 1
            new_row["IdCardNo"] = max_id_card_no + 1
            new_row["InsCardNo"] = increment_string(ins_card_no_prefix, max_ins_card_no + 1)

            new_data.append(new_row)

        # Cập nhật giá trị mới nhất của các biến
        max_first_name += 1
        max_id_card_no += 1
        max_ins_card_no += 1

    return pd.DataFrame(new_data)

def write_data_to_excel(file_path, sheet_name, data):
    # Ghi dữ liệu vào tệp Excel và ghi đè lên dữ liệu hiện có
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
        data.to_excel(writer, sheet_name=sheet_name, index=False)

def process_patient_from_excel():
    file_path = "D://HIS api automation/DataTest/Data_API_Tiếp_nhận.xlsx"
    sheet_name = "Sheet1"

    # Đọc dữ liệu gốc từ tệp Excel
    excel_data = pd.read_excel(file_path, sheet_name=sheet_name)

    # Xóa hết dữ liệu trong tệp Excel
    # clear_excel_sheet(file_path, sheet_name)

    # Tạo dữ liệu bổ sung và ghi vào file Excel
    num_records_to_add = 5  # Số dòng dữ liệu bổ sung
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

process_patient_from_excel()