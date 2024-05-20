import requests
import pandas as pd


# Base url
base_url = "http://115.79.31.186:1096"

# Auth token
auth_token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IjM4MzkiLCJyb2xlIjoiQWRtaW4iLCJBY2NvdW50TmFtZSI6Imh1bmdxYiIsIkNsaWVudElwQWRkcmVzcyI6Ijo6MSIsIklzTG9jYWxJcCI6IlRydWUiLCJuYmYiOjE3MTUxODQ2NDIsImV4cCI6MTcxNTE4ODI0MiwiaWF0IjoxNzE1MTg0NjQyfQ.CihuC246iqFUos4MNZtNWs2q_SBOtmbXz4NRNuRQ4rg"


# Tạo thông tin dịch vụ
def create_patient_service():
    from Cận_lâm_sàng.GET import get_info_patient
    labEx_ids_and_patient_ids = get_info_patient()
    labEx_ids = [item["labExId"] for item in labEx_ids_and_patient_ids]

    # Kiểm tra xem danh sách labEx_ids có phần tử không
    if not labEx_ids:
        print("No labExId available.")
        return []

    # Tạo URL và headers cho request POST
    url = f"{base_url}/cis/LabExamItems/LabExamIds?ExcludedAttribute=&serviceTypeL0=&isLoadDelete=False"
    headers = {"Authorization": auth_token}

    # Tạo data từ danh sách labEx_ids
    data = labEx_ids

    try:
        # Thực hiện request POST
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()

        # Xử lý response data
        response_data = response.json()
        exItem_ids = []

        if isinstance(response_data, list):
            for item in response_data:
                exItem_id = item.get("exItemId")
                if exItem_id is not None:
                    exItem_ids.append(exItem_id)
                    print(exItem_id)
        elif isinstance(response_data, dict):
            exItem_id = response_data.get("exItemId")
            if exItem_id is not None:
                exItem_ids.append(exItem_id)
                print(exItem_id)
        else:
            print("Invalid response format")

        print("exItem_ids:", exItem_ids)
        return exItem_ids

    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []

# Tạo bill
def create_bill():
    exItem_ids = create_patient_service()
    url = f"{base_url}/finance/BillLabExams/ExItemIds"
    headers = {"Authorization": auth_token}
    data = exItem_ids
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()

def create_information_patient():
    from Cận_lâm_sàng.GET import get_info_patient
    labEx_ids_and_patient_ids = get_info_patient()
    patient_ids = [item["patientId"] for item in labEx_ids_and_patient_ids]

    # Kiểm tra xem danh sách patient_ids có phần tử không
    if not patient_ids:
        print("No patientId available.")
        return []

    # Tạo URL và headers cho request POST
    url = f"{base_url}/pms/Patients/PatientIds"
    headers = {"Authorization": auth_token}
    # Tạo data từ danh sách labEx_ids
    data = patient_ids
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    # Xử lý response data
    response_data = response.json()
    return response_data



def process_test():
    from Cận_lâm_sàng.GET import choose_patient_to_start
    choose_patient_to_start()
    create_bill()
    create_information_patient()


process_test()