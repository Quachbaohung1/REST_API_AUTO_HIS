import requests
import pandas as pd
import datetime
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
    create_visit(visit_data, Formated_visit_on)

def process_patient_from_excel():
    file_path = "D://HIS api automation/DataTest/Data_API_Tiếp_nhận.xlsx"
    excel_data = pd.read_excel(file_path, sheet_name="Sheet1")
    for index, row in excel_data.iterrows():
        patient_id = create_patient_from_excel(row)
        if int(row["InsBenefitType"]) == 2:
            create_insurance_from_excel(row, patient_id)
        create_visit_from_excel(row, patient_id)

