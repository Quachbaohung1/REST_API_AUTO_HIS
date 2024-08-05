import datetime
import requests
import json
from Cấu_hình.Setup import base_url_4, auth_token_4, base_url_2, auth_token_2, base_url_3, auth_token_3


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
    date = date_formatted()
    url = f"{base_url_4}/LabExams/?fromDate={date}&toDate={date}&refNo=&patientCode=&patientName=&wardUnitId=&attribute=0&labExStatus=1&byProviderId=552&labExItemAttr=2&excludedLabExAttr=4&medRcdId=&qmsNo=&fromApproveDate=&toApproveDate=&fromLabDxOn=&toLabDxOn=&isLoadMissEntries=False&isStateForLab=False&isLoadItem=False"
    headers = {"Authorization": auth_token_4}
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

    labEx_ids = []
    patient_ids = []
    entry_ids = []

    if isinstance(response_data, list):
        for item in response_data:
            labEx_id = item.get("labExId")
            patient_id = item.get("patientId")
            if labEx_id is not None and patient_id is not None:
                labEx_ids.append(labEx_id)
                patient_ids.append(patient_id)
    elif isinstance(response_data, dict):
        labEx_id = response_data.get("labExId")
        patient_id = response_data.get("patientId")
        if labEx_id is not None and patient_id is not None:
            labEx_ids.append(labEx_id)
            patient_ids.append(patient_id)
    else:
        print("Invalid response format")

    return response_data, labEx_ids, patient_ids


# Chọn BN để trả CLS
def choose_patient_to_start(entry_ids):
    entry_ids_1 = []
    for entryId in entry_ids:
        url = f"{base_url_2}/Visits/EntryId/{entryId}"
        headers = {"Authorization": auth_token_2}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        print("response_data:", response_data)
        if "entry" in response_data:
            entry = response_data["entry"]
            # Kiểm tra xem "entryId" có tồn tại trong "entry" hay không
            if "entryId" in entry:
                entryId = entry["entryId"]
                entry_ids_1.append(entryId)  # Thêm entryId vào danh sách entryIds
            else:
                print(f"Không tìm thấy entryId")
        else:
            print(f"Không tìm thấy entry")

    return response_data, entry_ids_1


def load_report(patientId):
    url = f"{base_url_4}/LabExams/LoadLabExByPatientId/{patientId}?isLoadEntry=True"
    headers = {"Authorization": auth_token_4}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    print("response_data_report:", response_data)
    return response_data


# Chọn loại phiếu để trả kết quả CLS
def choose_ticket_of_CLS():
    url = f"{base_url_3}/Abbreviations/AbbrService"
    headers = {"Authorization": auth_token_3}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    print("response_data_report:", response_data)
    return response_data