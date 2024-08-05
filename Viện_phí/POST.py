import requests
import pandas as pd
from Cấu_hình.Setup import base_url_4, auth_token_4, base_url_6, auth_token_6


# Khởi tạo thông tin
def create_info(patientCode):
    from Viện_phí.GET import get_info_CLS
    labExId = get_info_CLS(patientCode)
    url = f"{base_url_4}/LabExamItems/LabExamIds?ExcludedAttribute=&serviceTypeL0=&isLoadDelete=False"
    headers = {"Authorization": auth_token_4}
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
    url = f"{base_url_6}/StmMedServicePrices/Ids?benefitType="
    headers = {"Authorization": auth_token_6}
    data = [priceId]
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    return response_data


# def create_service(visitId):
#     from Viện_phí.GET import get_info_service
#     all_info = []
#     labExIds = get_info_service(visitId)
#     url = f"{base_url_4}/LabExamItems/LabExamIds?ExcludedAttribute=&serviceTypeL0=&isLoadDelete=False"
#     headers = {"Authorization": auth_token_4}
#     data = labExIds
#     response = requests.post(url, json=data, headers=headers)
#     response.raise_for_status()
#     response_data = response.json()
#     all_info.extend([
#         {
#             # "entryId": item.get("entryId"),
#             # "visitId": item.get("visitId"),
#             "amt": item.get("amt"),
#             "status": item.get("status"),
#             "exItemId": item.get("exItemId"),
#             "insBenefitType": item.get("insBenefitType", 0),
#             "priceId": item.get("priceId"),
#             "insBenefitRatio": item.get("insBenefitRatio", 0),
#             "price": item.get("price"),
#             "insPrice": item.get("insPrice"),
#             "insPriceRatio": item.get("insPriceRatio"),
#             "qty": item.get("qty"),
#         }
#         for item in response_data
#     ])
#     print("all_info:", all_info)
#     return all_info


def create_service_designation(data):
    url = f"{base_url_6}/AdvancePayments/Finalize?viewCase=1"
    headers = {"Authorization": auth_token_6}
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
    return response_data, payment_ids


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
    # ins_benefit_ratio = 100 if total_price <= 270000 else int(row["InsBenefitRatio"])

    # Tạo danh sách PaymentData với cấu trúc yêu cầu
    payment_items = []

    # Thu thập giá trị insPriceRatio từ all_info
    ins_price_ratios = [item.get('insPriceRatio') for item in all_info]

    # Kiểm tra xem tất cả các giá trị insPriceRatio có giống nhau không
    if all(x == ins_price_ratios[0] for x in ins_price_ratios):
        ins_price_ratio = ins_price_ratios[0]
    else:
        ins_price_ratio = ins_price_ratios

    # Trường hợp có miễn giảm
    if int(row["RealRevenue"]) != 0:
        total_ins_price = sum(item.get('price') for item in all_info)
        percent = int(row["DiscAmt"]) / ((total_ins_price/ins_price_ratio) * 100) if ins_price_ratio else 0

    # Tạo danh sách PaymentData với cấu trúc yêu cầu
    for item in all_info:
        if int(row["RealRevenue"]) != 0:
            DiscAmt = round(percent * item.get('price'))
        else:
            DiscAmt = None
        payment_item = {
            "PaymentItemId": item.get('txVisitMedId') if item.get('objType') == 'Thuoc' else item.get('exItemId', None),
            "ItemType": 2 if item.get('objType') == 'Thuoc' else 1,
            "PayType": int(row["PayType"]),
            "InsBenefitType": item.get('insBenefitType'),
            "PriceId": item.get('priceId'),
            "InsBenefitRatio": 0 if item.get('insBenefitType') == 3 else item.get('insBenefitRatio'),
            "Price": item.get('price'),
            "InsPrice": item.get('insPrice'),
            "InsPriceRatio": item.get('insPriceRatio'),
            "Qty": item.get('qty'),
            "DiscAmt": DiscAmt
        }
        payment_items.append(payment_item)

    for item in infos:
        discount_type = int(row["DiscountType"]) if not pd.isna(row["DiscountType"]) else handle_null(
            row["DiscountType"])
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
            "RealRevenue": int(row["RealRevenue"]),
            "DiscReason": str(row["DiscReason"]),
            "DiscountType": discount_type

        }

        # Adjust Amt and RealRevenue if InsBenefitType is 3
        if any(pi["InsBenefitType"] == 3 for pi in payment_items):
            service_data["Amt"] = sum(pi["Price"] for pi in payment_items if pi["InsBenefitType"] == 3)
            service_data["RealRevenue"] = sum(pi["Price"] for pi in payment_items if pi["InsBenefitType"] == 3)

        return service_data


def create_advancePayments(visitId):
    url = f"{base_url_6}/AdvancePayments/LoadByVisitIds?isFull=True"
    headers = {"Authorization": auth_token_6}
    data = [visitId]
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()


# Tạo hóa đơn
def create_bill(visitId):
    from Viện_phí.GET import get_paymentId
    paymentId = get_paymentId(visitId)
    url = f"{base_url_6}/BillLabExams/AdvPmtIds"
    headers = {"Authorization": auth_token_6}
    data = paymentId
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    return response_data


# InsertCongKhamVaoLei
def InsertCongKhamVaoLei(visitCode):
    url = f"{base_url_6}/AdvancePayments/InsertCongKhamVaoLei?visitCode={visitCode}&medRecCode="
    headers = {"Authorization": auth_token_6}
    data = None
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    return response_data


# InsertRowDataDetail
def InsertRowDataDetail(visitCode):
    url = f"{base_url_6}/AdvancePayments/InsertRowDataDetail?visitCode={visitCode}&medRecCode="
    headers = {"Authorization": auth_token_6}
    data = []
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    return response_data


# InsertRowDataHeader
def InsertRowDataHeader(visitCode):
    url = f"{base_url_6}/AdvancePayments/InsertRowDataHeader?visitCode={visitCode}&medRecCode="
    headers = {"Authorization": auth_token_6}
    data = []
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    return response_data


# Quyết toán có chốt chi phí
def process_VP(test_data, file_path, testcase_id, patientCodes):
    from Viện_phí.GET import get_info_patient1, get_info_status, check_txInstruction, get_info_service, display_info_of_patient, get_rowdata
    from Viện_phí.PUT import prepare_information_data, update_information_patient, closing_costs, UpdateBenefitRatio

    test_data = test_data[test_data['TestCaseId'] == testcase_id]
    sheet_name_a = "Data"
    # Đọc dữ liệu gốc từ tệp Excel

    excel_data = test_data
    excel_data_a = pd.read_excel(file_path, sheet_name=sheet_name_a)
    num_records_to_add = 1
    # Nhập mã bệnh nhân

    # patientCodes = [24015832]
    # Duyệt qua từng mã bệnh nhân trong danh sách patientCodes
    for patientCode in patientCodes:

        # Duyệt qua từng bản ghi trong filtered_data
        for index, row in excel_data.iterrows():

            # Lấy thông tin về visitId và visitCode
            visitId, visitCode = get_info_patient1(patientCode)

            # Chốt chi phí
            closing_costs(visitId)
            InsertCongKhamVaoLei(visitCode)
            UpdateBenefitRatio(visitCode)
            InsertRowDataDetail(visitCode)
            InsertRowDataHeader(visitCode)

            # Tạo thông tin thanh toán cho mã bệnh nhân
            response_data = create_info_payment(patientCode)
            print("response_data:", response_data)

            # Kiểm tra txInstruction
            txInstruction = check_txInstruction(visitId)
            if txInstruction == 2:
                # Nếu txInstruction là 3, hoặc là 2, thực hiện thanh toán và các thao tác liên quan
                print("Được thực hiện thanh toán")
                display_info_of_patient(visitCode)
                create_advancePayments(visitId)
                # all_info = create_service(visitId)
                all_info = get_rowdata(visitCode)
                infos = get_info_status(visitId)

                # Duyệt qua từng bản ghi trong excel_data để tạo dữ liệu dịch vụ
                for index_a, row_a in excel_data.iterrows():
                    service_data = data_of_create_service_designation(row_a, all_info, infos)
                    response_data, payment_ids = create_service_designation(service_data)
                    get_info_service(visitId)
                    create_advancePayments(visitId)
                    response_data = create_bill(visitId)
            else:
                # Nếu txInstruction không phải là 3, cập nhật thông tin bệnh nhân và thực hiện các thao tác khác
                print("Còn tồn tại hướng xử trí tại phòng khám! Vui lòng cập nhật lại hướng xử trí!")
                response_json = get_info_status(visitId)

                # Duyệt qua từng bản ghi trong excel_data_a để chuẩn bị dữ liệu thông tin
                for index, row in excel_data_a.iterrows():
                    data, entryId, visitId = prepare_information_data(row, response_json)

                # Cập nhật thông tin bệnh nhân
                update_information_patient(entryId, data)
                closing_costs(visitId)
                InsertCongKhamVaoLei(visitCode)
                UpdateBenefitRatio(visitCode)
                InsertRowDataDetail(visitCode)
                InsertRowDataHeader(visitCode)
                display_info_of_patient(visitCode)
                create_advancePayments(visitId)
                all_info = get_rowdata(visitCode)
                infos = get_info_status(visitId)

                # Duyệt qua từng bản ghi trong excel_data để tạo dữ liệu dịch vụ
                for index_a, row_a in excel_data.iterrows():
                    service_data = data_of_create_service_designation(row_a, all_info, infos)
                    response_data, payment_ids = create_service_designation(service_data)
                    get_info_service(visitId)
                    create_advancePayments(visitId)
                    response_data = create_bill(visitId)

    return response_data


# Quyết toán không chốt chi phí
def process_VP_without_cost(test_data, file_path, testcase_id):
    from Viện_phí.GET import get_info_patient1, get_info_status, check_txInstruction, get_info_service, \
        display_info_of_patient, get_rowdata
    from Viện_phí.PUT import prepare_information_data, update_information_patient, closing_costs, UpdateBenefitRatio

    test_data = test_data[test_data['TestCaseId'] == testcase_id]
    sheet_name_a = "Data"
    # Đọc dữ liệu gốc từ tệp Excel

    excel_data = test_data
    excel_data_a = pd.read_excel(file_path, sheet_name=sheet_name_a)
    num_records_to_add = 1
    # Nhập mã bệnh nhân
    patientCode = 24013742
    for _ in range(num_records_to_add):
        for index, row in excel_data.iterrows():
            response_data = create_info_payment(patientCode)
            print("response_data:", response_data)
            visitId, visitCode = get_info_patient1(patientCode)
            txInstruction = check_txInstruction(visitId)
            if txInstruction == 3:
                InsertCongKhamVaoLei(visitCode)
                UpdateBenefitRatio(visitCode)
                InsertRowDataDetail(visitCode)
                InsertRowDataHeader(visitCode)
                print("Được thực hiện thanh toán")
                display_info_of_patient(visitCode)
                create_advancePayments(visitId)
                all_info = get_rowdata(visitCode)
                infos = get_info_status(visitId)
                for index_a, row_a in excel_data.iterrows():
                    service_data = data_of_create_service_designation(row_a, all_info, infos)
                response_data, payment_ids = create_service_designation(service_data)
                get_info_service(visitId)

                create_advancePayments(visitId)
                response_data = create_bill(visitId)
                return response_data
            else:
                print("Còn tồn tại hướng xử trí tại phòng khám! Vui lòng cập nhật lại hướng xử trí!")
                response_json = get_info_status(visitId)
                for index, row in excel_data_a.iterrows():
                    data, entryId, visitId = prepare_information_data(row, response_json)
                update_information_patient(entryId, data)
                InsertCongKhamVaoLei(visitCode)
                UpdateBenefitRatio(visitCode)
                InsertRowDataDetail(visitCode)
                InsertRowDataHeader(visitCode)
                display_info_of_patient(visitCode)
                create_advancePayments(visitId)
                all_info = get_rowdata(visitCode)
                infos = get_info_status(visitId)
                for index_a, row_a in excel_data.iterrows():
                    service_data = data_of_create_service_designation(row_a, all_info, infos)
                response_data, payment_ids = create_service_designation(service_data)
                get_info_service(visitId)
                create_advancePayments(visitId)
                response_data = create_bill(visitId)
                return response_data


# Có miễn giảm chi phí
def Cost_exemption(test_data, file_path, testcase_id):
    from Viện_phí.GET import get_info_patient1, get_info_status, check_txInstruction, get_info_service, \
        display_info_of_patient, get_rowdata
    from Viện_phí.PUT import prepare_information_data, update_information_patient, closing_costs, UpdateBenefitRatio

    test_data = test_data[test_data['TestCaseId'] == testcase_id]
    sheet_name_a = "Data"
    # Đọc dữ liệu gốc từ tệp Excel

    excel_data = test_data
    excel_data_a = pd.read_excel(file_path, sheet_name=sheet_name_a)
    num_records_to_add = 1
    # Nhập mã bệnh nhân
    patientCode = 24013742

    for _ in range(num_records_to_add):
        for index, row in excel_data.iterrows():
            response_data = create_info_payment(patientCode)
            print("response_data:", response_data)
            visitId, visitCode = get_info_patient1(patientCode)
            txInstruction = check_txInstruction(visitId)
            if txInstruction == 3:
                closing_costs(visitId)
                InsertCongKhamVaoLei(visitCode)
                UpdateBenefitRatio(visitCode)
                InsertRowDataDetail(visitCode)
                InsertRowDataHeader(visitCode)
                print("Được thực hiện thanh toán")
                display_info_of_patient(visitCode)
                create_advancePayments(visitId)
                all_info = get_rowdata(visitCode)
                infos = get_info_status(visitId)
                for index_a, row_a in excel_data.iterrows():
                    service_data = data_of_create_service_designation(row_a, all_info, infos)
                response_data, payment_ids = create_service_designation(service_data)
                get_info_service(visitId)

                create_advancePayments(visitId)
                response_data = create_bill(visitId)
                return response_data
            else:
                print("Còn tồn tại hướng xử trí tại phòng khám! Vui lòng cập nhật lại hướng xử trí!")
                response_json = get_info_status(visitId)
                for index, row in excel_data_a.iterrows():
                    data, entryId, visitId = prepare_information_data(row, response_json)
                update_information_patient(entryId, data)
                closing_costs(visitId)
                InsertCongKhamVaoLei(visitCode)
                UpdateBenefitRatio(visitCode)
                InsertRowDataDetail(visitCode)
                InsertRowDataHeader(visitCode)
                display_info_of_patient(visitCode)
                create_advancePayments(visitId)
                all_info = get_rowdata(visitCode)
                infos = get_info_status(visitId)
                for index_a, row_a in excel_data.iterrows():
                    service_data = data_of_create_service_designation(row_a, all_info, infos)
                response_data, payment_ids = create_service_designation(service_data)
                get_info_service(visitId)
                create_advancePayments(visitId)
                response_data = create_bill(visitId)
                return response_data