import datetime
import requests
import json


# Base url
base_url = "http://115.79.31.186:1096"
# Auth token
auth_token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IjM4MzkiLCJyb2xlIjoiQWRtaW4iLCJBY2NvdW50TmFtZSI6Imh1bmdxYiIsIkNsaWVudElwQWRkcmVzcyI6Ijo6MSIsIklzTG9jYWxJcCI6IlRydWUiLCJuYmYiOjE3MTUxODQ2NDIsImV4cCI6MTcxNTE4ODI0MiwiaWF0IjoxNzE1MTg0NjQyfQ.CihuC246iqFUos4MNZtNWs2q_SBOtmbXz4NRNuRQ4rg"


# Lấy ngày tháng từ hàm GET ở file Tiếp nhận
def date_formatted():
    from Tiếp_nhận.GET import CurrentServerDateTime
    date = str(CurrentServerDateTime())
    date_value_trimmed = date[:20] + "+" + date[-6:]
    isit_on_value_trimmed = date_value_trimmed.replace('"', '')

    date_datetime = datetime.datetime.strptime(isit_on_value_trimmed, "%Y-%m-%dT%H:%M:%S%z")
    date_fomatted = date_datetime.strftime("%Y%m%d")
    print("Formated_visit_on: ", date_fomatted)
    return date_fomatted

# Lấy thông tin BN có CLS
def get_info_patient():
    print("Hàm check_patient_in_room được gọi")
    date = date_formatted()
    url = f"{base_url}/cis/LabExams/?fromDate={date}&toDate={date}&refNo=&patientCode=&patientName=&wardUnitId=&attribute=0&labExStatus=1&byProviderId=552&labExItemAttr=2&excludedLabExAttr=4&medRcdId=&qmsNo=&fromApproveDate=&toApproveDate=&fromLabDxOn=&toLabDxOn=&isLoadMissEntries=False&isStateForLab=False&isLoadItem=False"
    headers = {"Authorization": auth_token}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response_data = response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        return []

    labEx_ids_and_patient_ids = []

    if isinstance(response_data, list):
        for item in response_data:
            labEx_id = item.get("labExId")
            patient_id = item.get("patientId")
            if labEx_id is not None and patient_id is not None:
                labEx_ids_and_patient_ids.append({"labExId": labEx_id, "patientId": patient_id})
                print(f"labEx_id: {labEx_id}, patient_id: {patient_id}")
    elif isinstance(response_data, dict):
        labEx_id = response_data.get("labExId")
        patient_id = response_data.get("patientId")
        if labEx_id is not None and patient_id is not None:
            labEx_ids_and_patient_ids.append({"labExId": labEx_id, "patientId": patient_id})
            print(f"labEx_id: {labEx_id}, patient_id: {patient_id}")
    else:
        print("Invalid response format")

    print("labEx_ids_and_patient_ids:", labEx_ids_and_patient_ids)
    return labEx_ids_and_patient_ids


# Chọn BN để trả CLS
def choose_patient_to_start():
    from Khám_bệnh_CDDV.POST import process_kb_CDDV
    frVisitEntryIds = process_kb_CDDV()
    entry_ids = []
    for frVisitEntryId in frVisitEntryIds:
        url = f"{base_url}/pms/Visits/EntryId/{frVisitEntryId[0]}"
        headers = {"Authorization": auth_token}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        print("response_data:", response_data)
        # Truy xuất entryId từ trường con entry
        entry = response_data.get("entry")
        if entry and "entryId" in entry:
            entry_ids.append(entry["entryId"])
    return entry_ids


# Chọn BN để trả CLS
def get_information_patient(entry_ids):
    for entry_id in entry_ids:
        url = f"{base_url}/pms/Visits/EntryId/{entry_id}"
        headers = {"Authorization": auth_token}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        print("response_data:", response_data)
    return response_data