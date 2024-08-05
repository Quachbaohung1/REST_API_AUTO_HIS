import datetime
import requests
from Cấu_hình.Setup import base_url_2, auth_token_2, base_url_6, auth_token_6, base_url_4, auth_token_4


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
def get_info_patient1(patientCode):
    url = f"{base_url_2}/Visits/PtName/{patientCode}?getIfOnDate=20240528&allStatus=False&isGetWardUnitIds=True&isGetPatientInfo=True"
    headers = {"Authorization": auth_token_2}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    if isinstance(response_data, list):
        for item in response_data:
            visitId = item.get("visitId")
    if isinstance(response_data, list):
        for item in response_data:
                visitCode = item.get("visitCode")

    return visitId, visitCode


# Lấy thông tin CLS(Nếu có cận lầm sàng)
def get_info_CLS(patientCode):
    visitId, visitCode = get_info_patient1(patientCode)
    url = f"{base_url_4}/LabExams/VisitId/{visitId}?labExAttribute=&excludedAttribute="
    headers = {"Authorization": auth_token_4}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    if isinstance(response_data, list):
        for item in response_data:
            labExId = item.get("labExId")
    return labExId


# Check txInstruction
def check_txInstruction(visitId):
    url = f"{base_url_2}/VisitEntries/VisitId/{visitId}"
    headers = {"Authorization": auth_token_2}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response_json = response.json()
        if isinstance(response_json, list):
            for item in response_json:
                txInstruction = item["txInstruction"]
        print("txInstruction:", txInstruction)
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    return txInstruction


# Lấy thông tin các dịch vụ của BN
def get_info_service(visitId):
    labExIds = []
    url = f"{base_url_4}/LabExams/VisitId/{visitId}?labExAttribute=&excludedAttribute="
    headers = {"Authorization": auth_token_4}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    if isinstance(response_data, list):
        for item in response_data:
            labExIds.append(item["labExId"])
    return labExIds


# Kiểm tra Status của BN ở phòng khám
def get_info_status(visitId):
    infos = []
    url = f"{base_url_2}/VisitEntries/VisitId/{visitId}"
    headers = {"Authorization": auth_token_2}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response_json = response.json()
        infos.extend([
            {
                "entryId": item.get("entryId"),
                "createById": item.get("createById"),
                "lastDxOn": item.get("lastDxOn"),
                "visitId": item.get("visitId"),
                "amt": item.get("amt"),
                "status": item.get("status"),
                "exItemId": item.get("exItemId"),
                "insBenefitType": item.get("insBenefitType", 0),
                "priceId": item.get("priceId"),
                "insBenefitRatio": item.get("insBenefitRatio", 0),
                "price": item.get("price"),
                "insPrice": item.get("insPrice"),
                "insPriceRatio": item.get("insPriceRatio"),
                "qty": item.get("qty"),
                "medServiceId": item.get("medServiceId"),
                "wardUnitId": item.get("wardUnitId"),
                "createOn": item.get("createOn"),
                "createByWardUnitId": item.get("createByWardUnitId"),
                "qmsNo": item.get("qmsNo"),
                "ticketId": item.get("ticketId"),
            }
            for item in response_json
        ])
        print("infos:", infos)
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    return infos


# Lấy paymentId
def get_paymentId(visitId):
    paymentIds = []
    url = f"{base_url_6}/AdvancePayments/VisitId/{visitId}"
    headers = {"Authorization": auth_token_6}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response_json = response.json()
        if isinstance(response_json, list):
            for item in response_json:
                paymentIds.append(item["paymentId"])
        print("paymentIds:", paymentIds)
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    return paymentIds


# Hiển thị tất cả chi phí của bệnh nhân ở lưới thông tin
def display_info_of_patient(visitCode):
    url = f"{base_url_6}/AdvancePayments/GetRowDataDetailByVisOrMedRec?visitCode={visitCode}&medRecCode="
    headers = {"Authorization": auth_token_6}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response_json = response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    return response_json


# Lấy row_data
def get_rowdata(visitCode):
    url = f"{base_url_6}/AdvancePayments/GetRowDataDetailByVisOrMedRec?visitCode={visitCode}&medRecCode="
    headers = {"Authorization": auth_token_6}
    all_info = []
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response_json = response.json()
        all_info.extend([
            {
                # "entryId": item.get("entryId"),
                # "visitId": item.get("visitId"),
                "amt": item.get("amt"),
                # "status": item.get("status"),
                "exItemId": item.get("exItemId"),
                "insBenefitType": item.get("insBenefitType", 0),
                "priceId": item.get("priceId"),
                "insBenefitRatio": item.get("insBenefitRatio", 0),
                "price": item.get("price"),
                "insPrice": item.get("insPrice"),
                "insPriceRatio": item.get("insPriceRatio"),
                "qty": item.get("qty"),
                "txVisitMedId": item.get("txVisitMedId"),
                "objType": item.get("objType")
            }
            for item in response_json
        ])
        return all_info
    except requests.RequestException as e:
        print(f"Request failed: {e}")
