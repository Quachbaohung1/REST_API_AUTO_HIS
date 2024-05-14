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
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    patient_ids = []  # Tạo danh sách

    # Kiểm tra xem phản hồi là một danh sách hay một từ điển
    response_data = response.json()
    if isinstance(response_data, list):
        # Nếu là danh sách, lặp qua từng phần tử và truy cập vào thông tin cần thiết
        for item in response_data:
            patient_id = item.get("patientId")  # Sử dụng get để tránh lỗi nếu "patientId" không tồn tại
            if patient_id is not None:  # Kiểm tra xem patient_id có tồn tại không
                patient_ids.append(patient_id)
                print(patient_id)
    elif isinstance(response_data, dict):
        # Nếu là từ điển, truy cập trực tiếp vào thông tin cần thiết
        patient_id = response_data.get("patientId")
        if patient_id is not None:  # Kiểm tra xem patient_id có tồn tại không
            patient_ids.append(patient_id)
            print(patient_id)
    else:
        # Xử lý trường hợp phản hồi không phải là danh sách hoặc từ điển
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
def check_information_patient():
    from Khám_bệnh.POST import choose_patient
    date_formatted()
    visit_idas = choose_patient()
    visit_idbs = []  # Tạo một danh sách để lưu trữ thông tin từ mỗi lượt thăm
    for visit_ida in visit_idas:
        url = f"{base_url}/pms/Visits/Id/{visit_ida}?isGetDeleted=False"
        headers = {"Authorization": auth_token}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        # Lặp qua danh sách các đối tượng JSON trong response.json()
        visit_idb = response.json()["visitId"]  # Trích xuất visitId từ mỗi đối tượng
        visit_idbs.append(visit_idb)

    print("visit_idbs", visit_idbs)
    return visit_idbs

# Lấy thông tin bệnh nhân để update
def get_to_update():
    visit_idbs = check_information_patient()
    all_info = []  # Tạo một danh sách để lưu trữ thông tin từ mỗi lượt thăm
    for visit_idb in visit_idbs:
        url = f"{base_url}/pms/VisitEntries/VisitId/{visit_idb}"
        headers = {"Authorization": auth_token}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response_json = response.json()
        # In phản hồi JSON để kiểm tra cấu trúc
        print("Response JSON:", response_json)

        # Kiểm tra xem phản hồi có phải là một từ điển hay một danh sách
        if isinstance(response_json, dict):
            response_list = [response_json]  # Đóng gói vào một danh sách để xử lý thống nhất
        elif isinstance(response_json, list):
            response_list = response_json
        else:
            print("Unexpected response format:", response_json)
            continue

        # Lặp qua các phần tử trong danh sách để trích xuất thông tin
        for item in response_list:
            info = {
                "entryId": int(item["entryId"]),
                "visitId": int(item["visitId"]),
                "MedServiceId": int(item["medServiceId"]),
                "WardUnitId": int(item["wardUnitId"]),
                "CreateOn": item["createOn"],
                "CreateById": int(item["createById"]),
                "Status": int(item["status"]),
                "InsBenefitType": int(item["insBenefitType"]),
                "InsBenefitRatio": int(item["insBenefitRatio"]),
                "PriceId": int(item["priceId"]),
                "QmsNo": item["qmsNo"],
                "TicketId": int(item["ticketId"]),
                "CreateByWardUnitId": int(item["createByWardUnitId"])
            }
            all_info.append(info)  # Thêm thông tin vào danh sách all_info

            # In giá trị (có thể bỏ qua hoặc giữ lại cho mục đích debug)
            print("entryId:", info["entryId"])
            print("visitId:", info["visitId"])
            print("medServiceId:", info["MedServiceId"])
            print("wardUnitId:", info["WardUnitId"])
            print("createById:", info["CreateById"])
            print("status:", info["Status"])
            print("createOn:", info["CreateOn"])
            print("insBenefitType:", info["InsBenefitType"])
            print("insBenefitRatio:", info["InsBenefitRatio"])
            print("priceId:", info["PriceId"])
            print("qmsNo:", info["QmsNo"])
            print("ticketId:", info["TicketId"])
            print("createByWardUnitId:", info["CreateByWardUnitId"])

    return all_info



# Lấy thông tin txVisit
def get_information_txvisit():
    # Gọi hàm để lấy tất cả thông tin của bệnh nhân
    all_patient_info = check_information_patient()
    # Rút trích entryId từ kết quả trả về của hàm check_information_patient()
    visitId = all_patient_info[1]  # Ví dụ: Giả sử entryId là phần tử đầu tiên trong tuple
    url = f"{base_url}/pms/Visits/Id/{visitId}?isGetDeleted=False"
    headers = {"Authorization": auth_token}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    # Chỉ lấy các giá trị quan trọng từ phản hồi JSON
    response_json = response.json()
    InsBenefitType = response_json.get("InsBenefitType")
    InsBenefitRatio = response_json.get("InsBenefitRatio")
    InsCardId = response_json.get("InsCardId")
    # In giá trị
    print("InsBenefitType:", InsBenefitType)
    print("InsBenefitRatio:", InsBenefitRatio)
    print("InsCardId:", InsCardId)
    return (InsBenefitType, InsBenefitRatio, InsCardId)

