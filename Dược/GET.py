import datetime
import requests
import json
from Cấu_hình.Setup import base_url, auth_token


def date_formatted():
    from Tiếp_nhận.GET import CurrentServerDateTime
    date = str(CurrentServerDateTime())
    date_value_trimmed = date[:20] + "+" + date[-6:]
    isit_on_value_trimmed = date_value_trimmed.replace('"', '')

    date_datetime = datetime.datetime.strptime(isit_on_value_trimmed, "%Y-%m-%dT%H:%M:%S%z")
    date_fomatted = date_datetime.strftime("%Y%m%d")
    print("Formated_visit_on: ", date_fomatted)
    return date_fomatted


# Lấy thông tin bệnh nhân
def get_info_patient(patientCode):
    try:
        url = f"{base_url}/pms/Patients/Code/{patientCode}"
        headers = {"Authorization": auth_token}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        patient_id = response.json()["patientId"]
        return response_data, patient_id
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        return []


# Lấy thông tin visit của bệnh nhân
def get_info_visit(patient_id):
    try:
        url = f"{base_url}/pms/Visits/VisitHistory/{patient_id}"
        headers = {"Authorization": auth_token}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response_data = response.json()

        visit_ids = []
        visit_details = []
        if isinstance(response_data, list):
            for item in response_data:
                visit_id = item.get("visitId", None)
                createOn = item.get("createOn", None)
                entry = item.get("entry", None)
                entryId = entry.get("entryId", None)
                createById = item.get("createById", None)
                patientId = item.get("patientId", None)
                ptName = item.get("ptName", None)
                ptGender = item.get("ptGender", None)
                ptDob = item.get("ptDob", None)
                dxICD = entry.get("dxICD", None)
                dxText = entry.get("dxText", None)
                txNotes = entry.get("txNotes", None)

                if visit_id is not None:
                    visit_ids.append(visit_id)
                    visit_details.append({
                        "createOn": createOn,
                        "entryId": entryId,
                        "createById": createById,
                        "patientId": patientId,
                        "ptName": ptName,
                        "ptGender": ptGender,
                        "ptDob": ptDob,
                        "dxICD": dxICD,
                        "dxText": dxText,
                        "txNotes": txNotes
                    })
        else:
            print("response_data is not a list")
        return response_data, visit_ids, visit_details
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return [], [], []
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        return [], [], []


# Lấy check tồn kho
def get_store(itemIds):
    try:
        item_ids_str = "%2C".join(map(str, itemIds))
        url = f"{base_url}/ims/InvNowAvailables/36?invSource=&itemIds={item_ids_str}"
        headers = {"Authorization": auth_token}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        first_prices = []
        invSources = []
        for item in response_data:
            first_price = item.get("firstPrice", None)
            invSource = item.get("invSource", None)
            if first_price is not None:
                first_prices.append(first_price)
            if invSource is not None:
                invSources.append(invSource)
        return response_data, first_prices, invSources
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        return []


# Chọn phiếu để thu hồi
def choose_recall(voucherNo):
    try:
        url = f"{base_url}/ims/Vouchers/VoucherNo/{voucherNo}"
        headers = {"Authorization": auth_token}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        StoreIds = []
        voucherIds = []
        recall_details = []
        if isinstance(response_data, list):
            for item in response_data:
                voucherId = item.get("voucherId", None)
                txVisitId = item.get("txVisitId", None)
                InvSource = item.get("InvSource", None)
                createById = item.get("createById", None)
                storeId = item.get("storeId", None)

                if voucherId is not None:
                    voucherIds.append(voucherId)
                    StoreIds.append(storeId)
                    recall_details.append({
                        "txVisitId": txVisitId,
                        "InvSource": InvSource,
                        "createById": createById,
                    })
        else:
            print("response_data is not a list")
        return response_data, voucherIds, recall_details, StoreIds
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        return []


# Chọn thuốc để đề nghị ( kho chẵn thuốc là 24)
def choose_medicine_to_recommend(item_ids):
    try:
        item_ids_str = "%2C".join(map(str, item_ids))
        url = f"{base_url}/ims/InvNowAvailables/24?invSource=&itemIds={item_ids_str}"
        headers = {"Authorization": auth_token}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        StoreIds = []
        if isinstance(response_data, list):
            for item in response_data:
                storeId = item.get("storeId", None)
                if storeId is not None:
                    StoreIds.append(storeId)
        else:
            print("response_data is not a list")
        return response_data, StoreIds
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        return []


# Lấy thông tin voucher
def Vouchers(voucherId):
    try:
        url = f"{base_url}/ims/Vouchers/id/{voucherId}"
        headers = {"Authorization": auth_token}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        return response_data
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        return []


# Lấy mã xuất khác (xuất thanh lý)
def liquidation_export():
    try:
        url = f"{base_url}/ims/Vouchers/code/NT.OSY.24.07.XXXX"
        headers = {"Authorization": auth_token}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        return response_data
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        return []