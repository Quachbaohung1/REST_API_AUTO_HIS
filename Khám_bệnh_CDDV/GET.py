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


# Kiểm tra danh sách bệnh nhân ở Phòng khám
def check_patient_in_room():
    print("Hàm check_patient_in_room được gọi")
    date = date_formatted()
    url = f"{base_url}/pms/Visits/VisitFullEntries/149?fromDate={date}&TxEntryStatus=1&ExcludedVisitAttr=Empty"
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

    patient_ids = []

    if isinstance(response_data, list):
        for item in response_data:
            patient_id = item.get("patientId")
            if patient_id is not None:
                patient_ids.append(patient_id)
                print(patient_id)
    elif isinstance(response_data, dict):
        patient_id = response_data.get("patientId")
        if patient_id is not None:
            patient_ids.append(patient_id)
            print(patient_id)
    else:
        print("Invalid response format")

    print("patient_ids", patient_ids)
    return patient_ids


# Hiển thị entry_visit
def check_visit_enty():
    from Tiếp_nhận.POST import process_patient_from_excel
    entry_ids = process_patient_from_excel()  # Lấy danh sách entry_id từ file Excel
    visit_ids = []
    for entry_id in entry_ids:
        url = f"{base_url}/pms/VisitEntries/{entry_id}"
        headers = {"Authorization": auth_token}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        visit_id = response.json()["visitId"]
        visit_ids.append(visit_id)
    print("visit_ids", visit_ids)
    return visit_ids


# Lấy thông tin bệnh nhân GetDeleted
def check_information_patient_initial():
    visit_ids = check_visit_enty()
    visit_idas = []
    for visit_id in visit_ids:
        url = f"{base_url}/pms/Visits/Id/{visit_id}?isGetDeleted=False"
        headers = {"Authorization": auth_token}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            visit_json = response.json()
            visit_id = visit_json["visitId"]
            insBenefitType = int(visit_json.get("insBenefitType", 0))
            if insBenefitType != 2:
                print(f"Visit with visit_id {visit_id} does not have insBenefitType equal to 2.")
                continue
            visit_idas.append(visit_id)
        except requests.RequestException as e:
            print(f"Request failed: {e}")
    print("visit_ids", visit_idas)
    return visit_idas


def check_information_patient_subsequent():
    visit_info_list = []  # Khởi tạo danh sách để lưu thông tin các lượt thăm
    visitIds = get_to_update_initial()
    if visitIds:
        # Duyệt qua các visit_id trong danh sách thông tin
        for visit_id in visitIds:
            url = f"{base_url}/pms/Visits/Id/{visit_id}?isGetDeleted=False"
            headers = {"Authorization": auth_token}

            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                response_json = response.json()
                print("response_json: ", response_json)

                # Kiểm tra xem response_json có phải là một danh sách JSON hay không
                if isinstance(response_json, list):
                    # Duyệt qua các phần tử trong response_json và tạo visit_info_dict
                    for item in response_json:
                        visit_info = {
                            "visitId": int(item.get("visitId", 0)),
                            "patient_id": int(item.get("patientId", 0)),
                            "insBenefitType": int(item.get("insBenefitType", 0)),
                            "insBenefitRatio": int(item.get("insBenefitRatio", 0)),
                            "insCardId": int(item.get("insCardId", 0)) if item.get("insCardId") else None
                        }
                        visit_info_list.append(visit_info)  # Thêm thông tin vào danh sách
                        print("visit_info_dict:", visit_info_list)
                else:
                    # Nếu response_json không phải là một danh sách JSON, thêm nó vào danh sách
                    visit_info = {
                        "visitId": int(response_json.get("visitId", 0)),
                        "patient_id": int(response_json.get("patientId", 0)),
                        "insBenefitType": int(response_json.get("insBenefitType", 0)),
                        "insBenefitRatio": int(response_json.get("insBenefitRatio", 0)),
                        "insCardId": int(response_json.get("insCardId", 0)) if response_json.get("insCardId") else None
                    }
                    visit_info_list.append(visit_info)  # Thêm thông tin vào danh sách
                    print("visit_info_dict:", visit_info_list)

            except requests.RequestException as e:
                print(f"Request failed: {e}")
    else:
        print("Danh sách visitIds rỗng.")

    # Trả về danh sách thông tin các lượt thăm dưới dạng JSON
    return visit_info_list


# Lấy thông tin bệnh nhân để update
first_initialization = True
visit_idas_first = None
def get_to_update_initial():
    global first_initialization, patient_id, ins_card_id, all_info, visit_idas_first, patient_ids, ins_card_ids

    # Khởi tạo danh sách patient_ids và ins_card_ids
    visitIds = []

    if first_initialization and visit_idas_first is None:
        all_info = []  # Tạo một danh sách để lưu trữ thông tin từ mỗi lượt thăm
        visit_idas_first = check_information_patient_initial()  # Gán giá trị cho visit_idas_first

    # Sử dụng visit_idas_first cho lần lặp đầu tiên hoặc sử dụng giá trị được gán từ lần trước
    visit_idas = visit_idas_first if first_initialization else visit_idas_first

    for visit_idb in visit_idas:
        url = f"{base_url}/pms/VisitEntries/VisitId/{visit_idb}"
        headers = {"Authorization": auth_token}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response_json = response.json()

            if first_initialization:
                # Tạo danh sách thông tin từ từng lượt thăm và gộp vào danh sách all_info
                all_info.extend([
                    {
                        "entryId": int(item.get("entryId")),
                        "visitId": int(item.get("visitId")),
                        "medServiceId": int(item.get("medServiceId")),
                        "wardUnitId": int(item.get("wardUnitId")),
                        "createOn": item.get("createOn"),
                        "createById": int(item.get("createById")),
                        "status": int(item.get("status")),
                        "insBenefitType": int(item.get("insBenefitType", 0)),
                        "insBenefitRatio": int(item.get("insBenefitRatio", 0)),
                        "priceId": int(item.get("priceId")),
                        "qmsNo": item.get("qmsNo"),
                        "ticketId": int(item.get("ticketId")),
                        "createByWardUnitId": int(item.get("createByWardUnitId")),
                        "dxByStaffId": item.get("dxByStaffId"),
                        "dxICD": item.get("dxICD"),
                        "dxText": item.get("dxText"),
                        "patient_id": int(item.get("patientId", 0)),
                        "insCardId": int(item.get("insCardId", 0))
                    }
                    for item in response_json
                ])
            else:
                # Chỉ lấy patientId từ lần gọi thứ hai
                for item in response_json:
                    visitId = int(item.get("visitId", 0))
                    # Thêm patient_id vào danh sách patient_ids
                    visitIds.append(visitId)
                    print("visitIds:", visitIds)

        except requests.RequestException as e:
            print(f"Lỗi khi thực hiện yêu cầu: {e}")

    if first_initialization:
        first_initialization = False  # Đánh dấu lần khởi tạo đầu tiên đã hoàn thành
        return all_info
    else:
        return visitIds

#
def get_data_by_entry_id(entryId):
    entryIds = []
    url = f"{base_url}/cis/TxVisits/{entryId}?attribute=2"
    headers = {"Authorization": auth_token}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    response_json = response.json()
    print("response_json:", response_json)
    # Lặp qua danh sách các đối tượng JSON trong response.json()
    entryIdb = response.json()["visitEntryId"]
    entryIds.append(entryIdb)
    print("entryIds:", entryIds)
    return entryIds

# isLoadItem=True
def set_true(PatientId):
    url = f"{base_url}/cis/LabExams/LoadAllByPatientId/{PatientId}?isLoadItem=True"
    headers = {"Authorization": auth_token}
    response = requests.get(url, headers=headers)
    response.raise_for_status()


