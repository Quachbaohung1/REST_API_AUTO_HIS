import requests
import pandas as pd
from Cấu_hình.Setup import base_url, auth_token


# Khởi tạo thông tin
def create_info(patientCode):
    from Viện_phí.GET import get_info_CLS
    labExId = get_info_CLS(patientCode)
    url = f"{base_url}/cis/LabExamItems/LabExamIds?ExcludedAttribute=&serviceTypeL0=&isLoadDelete=False"
    headers = {"Authorization": auth_token}
    data = [labExId]
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    if isinstance(response_data, list):
        for item in response_data:
            priceId = item.get("priceId")
    return priceId


# Tạo payment
def create_info_payment(patientCode):
    priceId = create_info(patientCode)
    url = f"{base_url}/finance/StmMedServicePrices/Ids?benefitType="
    headers = {"Authorization": auth_token}
    data = [priceId]
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    return response_data


def create_service(visitId):
    from Viện_phí.GET import get_info_service
    all_info = []
    labExIds = get_info_service(visitId)
    url = f"{base_url}/cis/LabExamItems/LabExamIds?ExcludedAttribute=&serviceTypeL0=&isLoadDelete=False"
    headers = {"Authorization": auth_token}
    data = labExIds
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    all_info.extend([
        {
            # "entryId": item.get("entryId"),
            # "visitId": item.get("visitId"),
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
        }
        for item in response_data
    ])
    print("all_info:", all_info)
    return all_info


def create_service_designation(data):
    url = f"{base_url}/finance/AdvancePayments/Finalize?viewCase=1"
    headers = {"Authorization": auth_token}
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    if isinstance(response_data, list):
        payment_ids = [item["paymentId"] for item in response_data if "paymentId" in item]
    elif isinstance(response_data, dict):
        payment_ids = [response_data["paymentId"]] if "paymentId" in response_data else []
    else:
        payment_ids = []

    print("Payment IDs:", payment_ids)
    return payment_ids


# Dữ liệu của chỉ định dịch vụ
def data_of_create_service_designation(row, all_info, infos):
    from Tiếp_nhận.GET import CurrentServerDateTime

    pay_date = str(CurrentServerDateTime())
    Formated_date_payment = pay_date.replace('"', '')

    # Xử lý các giá trị null
    def handle_null(value):
        return str(value) if not pd.isna(value) else None

    # Tính tổng giá trị Price
    total_price = sum(item.get('price') for item in all_info) + row["Price"]
    # Xác định InsBenefitRatio dựa trên điều kiện tổng giá trị Price
    ins_benefit_ratio = 100 if total_price <= 270000 else int(row["InsBenefitRatio"])

    # Tạo danh sách PaymentData với cấu trúc yêu cầu
    payment_items = []

    # Tạo danh sách PaymentData với cấu trúc yêu cầu
    for item in all_info:
        payment_item = {
            "PaymentItemId": item.get('exItemId', None),
            "ItemType": int(row["ItemType"]) + 1,
            "PayType": int(row["PayType"]),
            "InsBenefitType": item.get('insBenefitType'),
            "PriceId": item.get('priceId'),
            "InsBenefitRatio": ins_benefit_ratio,
            "Price": item.get('price'),
            "InsPrice": item.get('insPrice'),
            "InsPriceRatio": item.get('insPriceRatio'),
            "Qty": int(row["Qty"]),
            "DiscAmt": 0
        }
        payment_items.append(payment_item)

    for item in infos:
        service_data = {
            "VisitId": item.get('visitId'),
            "Amt": int(row["Amt"]),
            "CreateById": item.get("createById"),
            "PaymentDate": Formated_date_payment,
            "Status": int(row["Status"]),
            "PaymentMethod": int(row["PaymentMethod"]),
            "DiscAmt": int(row["DiscAmt"]),
            "RePaidForPmtId": handle_null(row["RePaidForPmtId"]),
            "PaymentData": payment_items,
            "Prefix": handle_null(row["RePaidForPmtId"]),
            "LastDxOn": item.get("lastDxOn"),
            "RealRevenue": int(row["RealRevenue"])
        }
        return service_data


def create_advancePayments(visitId):
    url = f"{base_url}/finance/AdvancePayments/LoadByVisitIds?isFull=True"
    headers = {"Authorization": auth_token}
    data = [visitId]
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()


# Tạo hóa đơn
def create_bill(visitId):
    from Viện_phí.GET import get_paymentId
    paymentId = get_paymentId(visitId)
    url = f"{base_url}/finance/BillLabExams/AdvPmtIds"
    headers = {"Authorization": auth_token}
    data = paymentId
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    return response_data


def process_VP(file_path, file_path_a):
    from Viện_phí.GET import get_info_patient, get_info_status, check_txInstruction, get_info_service
    from Viện_phí.PUT import prepare_information_data, update_information_patient, closing_costs

    sheet_name = "Data"
    sheet_name_a = "Sheet1"
    # Đọc dữ liệu gốc từ tệp Excel
    excel_data = pd.read_excel(file_path, sheet_name=sheet_name)
    excel_data_a = pd.read_excel(file_path_a, sheet_name=sheet_name_a)
    num_records_to_add = 1
    # Nhập mã bệnh nhân
    patientCode = 24011788
    for _ in range(num_records_to_add):
        for index, row in excel_data.iterrows():
            response_data = create_info_payment(patientCode)
            print("response_data:", response_data)
            visitId = get_info_patient(patientCode)
            txInstruction = check_txInstruction(visitId)
            if txInstruction == 3:
                closing_costs(visitId)
                print("Được thực hiện thanh toán")
                create_advancePayments(visitId)
                all_info = create_service(visitId)
                infos = get_info_status(visitId)
                for index_a, row_a in excel_data_a.iterrows():
                    service_data = data_of_create_service_designation(row_a, all_info, infos)
                create_service_designation(service_data)
                get_info_service(visitId)
                create_advancePayments(visitId)
                response_data = create_bill(visitId)
                return response_data
            else:
                print("Còn tồn tại hướng xử trí tại phòng khám! Vui lòng cập nhật lại hướng xử trí!")
                response_json = get_info_status(visitId)
                data, entryId, visitId = prepare_information_data(row, response_json)
                update_information_patient(entryId, data)
                closing_costs(visitId)
