import requests
import pandas as pd
from copy import deepcopy


# Base url
base_url = "http://115.79.31.186:1096"

# Auth token
auth_token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IjM4MzkiLCJyb2xlIjoiQWRtaW4iLCJBY2NvdW50TmFtZSI6Imh1bmdxYiIsIkNsaWVudElwQWRkcmVzcyI6Ijo6MSIsIklzTG9jYWxJcCI6IlRydWUiLCJuYmYiOjE3MTUxODQ2NDIsImV4cCI6MTcxNTE4ODI0MiwiaWF0IjoxNzE1MTg0NjQyfQ.CihuC246iqFUos4MNZtNWs2q_SBOtmbXz4NRNuRQ4rg"


# Lấy thông tin tất cả các bệnh nhân
def create_information_patient():
    from Khám_bệnh_CDDV.GET import check_patient_in_room
    patient_ids = check_patient_in_room()
    url = f"{base_url}/pms/Patients/PatientIds"
    headers = {"Authorization": auth_token}
    data = patient_ids
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()


# Chọn bệnh nhân
def choose_patient():
    from Khám_bệnh_CDDV.GET import check_visit_enty
    visit_ids = check_visit_enty()
    visit_idas = []
    for visit_id in visit_ids:
        url = f"{base_url}/pms/VisitEntries/VisitIds"
        headers = {"Authorization": auth_token}
        data = [visit_id]
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        # Lặp qua danh sách các đối tượng JSON trong response.json()
        for item in response.json():
            visit_ida = item["visitId"]  # Trích xuất visitId từ mỗi đối tượng
            visit_idas.append(visit_ida)
    print("visit_idas", visit_idas)
    return visit_idas

# Chọn thuốc
def choose_medicine(data):
    url = f"{base_url}/ims/InvNowAvailables/GetInventoriesForBooking/?isInsurrance=True&name=&medAI=&fullName=&LengthLimit=20&fullNameOrCode=False&attribute=&isNoLoadItems=False"
    headers = {"Authorization": auth_token}
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_json = response.json()
    return response_json

# Data thuốc
def data_medicine(row):
    def handle_null(value, default=None, to_type=int):
        return to_type(value) if not pd.isna(value) else default

    # Chuyển đổi giá trị "IgnoreStoreId", "IgnoreLotId", "IgnoreInvSource" sang kiểu boolean
    IgnoreStoreId = False if str(row['IgnoreStoreId']).lower() == 'false' else True
    IgnoreLotId = False if str(row['IgnoreLotId']).lower() == 'false' else True
    IgnoreInvSource = False if str(row['IgnoreInvSource']).lower() == 'false' else True

    medicine_data = {
        "StoreIds": [
            handle_null(row['StoreIds'])
        ],
        "InvSources": handle_null(row['InvSources'], default=None, to_type=int),
        "LotIds": handle_null(row['LotIds'], default=None, to_type=int),
        "ItemIds": [
            handle_null(row['ItemIds'])
        ],
        "IgnoreItemIds": handle_null(row['IgnoreItemIds'], default=None, to_type=int),
        "VouStatus": handle_null(row['VouStatus'], default=None, to_type=int),
        "IgnoreStoreId": IgnoreStoreId,
        "IgnoreLotId": IgnoreLotId,
        "IgnoreInvSource": IgnoreInvSource,
        "ItemCatIds": handle_null(row['ItemCatIds'], default=None, to_type=int),
        "ItemTypes": handle_null(row['ItemTypes'], default=None, to_type=int),
        "BidIds": handle_null(row['BidIds'], default=None, to_type=int),
        "ProviderIds": handle_null(row['ProviderIds'], default=None, to_type=int),
        "IgnoreItemCatIds": handle_null(row['IgnoreItemCatIds'], default=None, to_type=int),
        "TakeOnlyGroupInStoreHospital": handle_null(row['TakeOnlyGroupInStoreHospital'], default=None, to_type=int),
        "TakeOnlyItemIns": handle_null(row['TakeOnlyItemIns'], default=None, to_type=int)
    }

    medicine = choose_medicine(medicine_data)
    return medicine

def generate_additional_data(original_data, num_records):
    new_data = []

    for _ in range(num_records):
        for _, row in original_data.iterrows():
            new_row = deepcopy(row)

            new_data.append(new_row)

    return pd.DataFrame(new_data)

def write_data_to_excel(file_path, sheet_name, data):
    # Ghi dữ liệu vào tệp Excel và ghi đè lên dữ liệu hiện có
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
        data.to_excel(writer, sheet_name=sheet_name, index=False)

# Call
def process_test():
    from Khám_bệnh_Toa_thuốc.PUT import update_medicine_patient_from_excel
    # from Khám_bệnh.GET import get_information_patient
    file_path = "D://HIS api automation/DataTest/Data_API_Thuốc.xlsx"
    sheet_name = "Sheet1"

    # Đọc dữ liệu gốc từ tệp Excel
    excel_data = pd.read_excel(file_path, sheet_name=sheet_name)

    # Tạo dữ liệu bổ sung và ghi vào file Excel
    num_records_to_add = 2  # Số dòng dữ liệu bổ sung
    additional_data = generate_additional_data(excel_data.tail(1), num_records_to_add)
    write_data_to_excel(file_path, sheet_name, additional_data)

    # Đọc lại dữ liệu đã ghi vào file
    additional_data = pd.read_excel(file_path, sheet_name=sheet_name)

    # Thông tin cần thiết cho get_information_patient
    for index, row in additional_data.iterrows():
        update_medicine_patient_from_excel(row)

process_test()