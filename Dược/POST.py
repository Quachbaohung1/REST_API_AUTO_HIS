import pandas as pd
import requests
from Cấu_hình.Setup import base_url, auth_token
from datetime import datetime
from dateutil.parser import parse


# Tạo thông tin abc
def create_abc(visit_ids):
    url = f"{base_url}/cis/TxVisits/VisitIds"
    headers = {"Authorization": auth_token}
    data = visit_ids
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    if isinstance(response_data, list):
        for item in response_data:
            txVisitId = item.get("txVisitId", None)
            if txVisitId is not None:
                print("txVisitId:", txVisitId)
    else:
        print("response_data is not a list")
    return response_data, txVisitId


# Tạo thông tin bcd
def create_bcd(txVisitId):
    url = f"{base_url}/cis/Prescriptions/TxVisitIds"
    headers = {"Authorization": auth_token}
    data = [txVisitId]
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    if isinstance(response_data, list):
        for item in response_data:
            pxId = item.get("pxId", None)
            if pxId is not None:
                print("pxId:", pxId)
    else:
        print("response_data is not a list")
    return response_data, pxId


# Tạo thông tin cde
def create_cde(txVisitId):
    url = f"{base_url}/cis/TxVisitMeds/TxVisitIds"
    headers = {"Authorization": auth_token}
    data = [txVisitId]
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    if isinstance(response_data, list) and len(response_data) > 0:
        StoreIds = response_data[0].get("storeId", None)
        ItemIds = response_data[0].get("itemId", None)

    else:
        raise ValueError("Unexpected response format or empty list")
    return response_data, StoreIds, ItemIds


# Kiểm tra tồn
def create_product(data):
    url = f"{base_url}/ims/InvNowInStores/?invNowStatus="
    headers = {"Authorization": auth_token}
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    return response_data


# Data của tạo phiếu xuất
def data_create_product(StoreIds, ItemIds):
    product_data = {
        "StoreIds": [
            StoreIds
        ],
        "ItemIds": [
            ItemIds
        ],
        "LotIds": None
    }
    return product_data


# Tạo phiếu xuất
def create_bills(data):
    url = f"{base_url}/ims/Vouchers/CreateVoucherOut/3?withBy=11"
    headers = {"Authorization": auth_token}
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    # Kiểm tra cấu trúc của response_data
    if "voucher" in response_data:
        voucherid = response_data["voucher"].get("voucherId")
        createOn = response_data["voucher"].get("createOn")
    else:
        raise ValueError("Unexpected response format: 'voucher' key not found")

    if "voucherOuts" in response_data and isinstance(response_data["voucherOuts"], list) and len(
            response_data["voucherOuts"]) > 0:
        id = response_data["voucherOuts"][0].get("id")
    else:
        raise ValueError("Unexpected response format or empty 'voucherOuts' list")
    return response_data, voucherid, id, createOn


# Data của tạo phiếu xuất
def data_create_bills(row, StoreIds, ItemIds, visit_details, patientCode, pxId):
    # Xử lý các giá trị null
    def handle_null(value):
        return value if not pd.isna(value) else None

    for visit_detail in visit_details:
        bill_data = {
            "imsGetInvNowWithBy": handle_null(row['imsGetInvNowWithBy']),
            "Voucher": {
                "Type": int(row['Type']),
                "OnDate": visit_detail.get("createOn"),
                "Description": "",
                "StoreId": StoreIds,
                "TxVisitId": visit_detail.get("visitId"),
                "VisitEntryId": visit_detail.get("entryId"),
                "InvSource": 0,
                "CreateById": visit_detail.get("createById"),
                "CreateOn": visit_detail.get("createOn"),
                "InvStatus": 0,
                "Attribute": 0,
                "InvStatusDescription": handle_null(row['InvStatusDescription']),
                "ProcStatusDescription": handle_null(row['ProcStatusDescription']),
                "CustomerName": handle_null(row['CustomerName']),
                "InvoiceText": handle_null(row['InvoiceText'])
            },
            "voucherOuts": [
                {
                    "PPU": 1,
                    "SaleAmt": 18168.0000000,
                    "Price": 9084.000,
                    "ItemId": ItemIds,
                    "ItemSource": 32,
                    "Qty": 2.0000,
                    "Amt": 18168.0000000
                }
            ],
            "voucherOutInvs": handle_null(row['voucherOutInvs']),
            "InvRequests": [],
            "VoucherExt": {
                "PatientId": visit_detail.get("patientId"),
                "PtNo": str(patientCode),
                "PtName": visit_detail.get("ptName"),
                "PtGender": visit_detail.get("ptGender"),
                "PtDob": visit_detail.get("ptDob"),
                "PtAddress": "5/49 Ntl, Phường 07, Quận Bình Thạnh, Thành phố Hồ Chí Minh",
                "DxICD": visit_detail.get("dxICD"),
                "DxText": visit_detail.get("dxText"),
                "TxNote": visit_detail.get("txNotes"),
                "DoctorName": "Quách Bảo Hưng"
            },
            "VoucherOutExts": [
                {
                    "Dosage": "- Sáng: 1 Viên- Trưa: 1 Viên",
                    "FrPxId": pxId
                }
            ],
            "RequestByInventory": handle_null(row['RequestByInventory'])
        }
        return bill_data


# Thực hiện tính tiền
def create_info_charge(voucherId):
    url = f"{base_url}/ims/VoucherOuts/VoucherIds"
    headers = {"Authorization": auth_token}
    data = voucherId
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    if isinstance(response_data, list) and len(response_data) > 0:
        voucherout_id = response_data[0].get("id", None)
        itemId = response_data[0].get("itemId", None)
    else:
        raise ValueError("Unexpected response format or empty list")
    recall_medicine_details = []
    if isinstance(response_data, list):
        for item in response_data:
            amt = item.get("amt", None)
            voucherId = item.get("voucherId", None)

            recall_medicine_details.append({
                "amt": amt,
                "voucherId": voucherId,
            })
    else:
        print("response_data is not a list")
    return response_data, voucherout_id, itemId, recall_medicine_details


def create_charge(voucherout_id):
    url = f"{base_url}/ims/VoucherOutInvs/VouOutIds"
    headers = {"Authorization": auth_token}
    data = [voucherout_id]
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    charge_details = []
    if isinstance(response_data, list):
        for item in response_data:
            id = item.get("id", None)
            vouInId = item.get("vouInId", None)
            price = item.get("price", None)
            insPrice = item.get("insPrice", None)
            lotId = item.get("lotId", None)
            qty = item.get("qty", None)

            charge_details.append({
                "id": id,
                "vouInId": vouInId,
                "price": price,
                "insPrice": insPrice,
                "lotId": lotId,
                "qty": qty
            })
    else:
        print("response_data is not a list")
    return response_data, charge_details


def charge_success(data):
    url = f"{base_url}/finance/AdvancePayments/RetailPayment"
    headers = {"Authorization": auth_token}
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    return response_data


def data_of_charge_success(row, VoucherId, id, createOn):
    # Xử lý các giá trị null
    def handle_null(value):
        return value if not pd.isna(value) else None

    charge_data = {
        "Amt": 18168.000000,
        "CreateById": 3839,
        "PaymentDate": createOn,
        "Status": int(row['Status']),
        "PaymentMethod": int(row['PaymentMethod']),
        "VoucherId": VoucherId,
        "RePaidForPmtId": handle_null(row['RePaidForPmtId']),
        "PaymentData": [
            {
                "PaymentItemId": id,
                "ItemType": 2,
                "PayType": 0,
                "InsBenefitType": 0,
                "InsBenefitRatio": 0,
                "Price": 9084.000,
                "InsPrice": 8490.000,
                "Qty": 2.000,
                "DiscAmt": 0.0
            }
        ],
        "Prefix": str(row['Prefix']),
        "LastDxOn": handle_null(row['LastDxOn']),
        "RealRevenue": 18168.000000
    }
    return charge_data


# Tạo phiếu thu hồi
def create_recall(data):
    url = f"{base_url}/ims/Vouchers/CreateVoucherInRevocation/3"
    headers = {"Authorization": auth_token}
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    return response_data


def data_of_create_recall(row, StoreIds, ItemIds, recall_details, charge_details):
    from Tiếp_nhận.GET import CurrentServerDateTime
    date = CurrentServerDateTime()
    if date:
        # Loại bỏ dấu ngoặc kép nếu có
        date = date.strip('"')
        # Loại bỏ phần múi giờ bằng cách tách chuỗi trước dấu "+"
        if '+' in date:
            date = date.split('+')[0]
        elif '-' in date:  # Nếu múi giờ có dấu trừ (cho các múi giờ âm)
            date = date.split('-')[0]
    else:
        date = None

    # Xử lý các giá trị null
    def handle_null(value):
        return value if not pd.isna(value) else None

    for recall_detail in recall_details:
        for charge_detail in charge_details:
            for StoreId in StoreIds:
                create_recall_data = {
                    "Voucher": {
                        "Type": int(row["Type"]),
                        "OnDate": date,
                        "StoreId": StoreId,
                        "TxVisitId": recall_detail.get("TxVisitId"),
                        "VisitEntryId": recall_detail.get("TxVisitId"),
                        "RefVoucherId": recall_detail.get("RefVoucherId"),
                        "InvSource": recall_detail.get("InvSource"),
                        "CreateById": recall_detail.get("createById"),
                        "CreateOn": date,
                        "InvStatus": recall_detail.get("InvStatus"),
                        "InvStatusDescription": handle_null(row["InvStatusDescription"]),
                        "ProcStatusDescription": handle_null(row["ProcStatusDescription"]),
                        "CustomerName": handle_null(row["CustomerName"]),
                        "InvoiceText": handle_null(row["InvoiceText"])
                    },
                    "VoucherIns": [],
                    "ItemLots": [],
                    "ItemPrices": [],
                    "RevocationVoucherIns": [
                        {
                            "VouInvId": charge_detail.get("vouInId"),
                            "Price": charge_detail.get("price"),
                            "RefVouOutInvId": charge_detail.get("id"),
                            "PriceCost": charge_detail.get("insPrice"),
                            "LotId": charge_detail.get("lotId"),
                            "ItemId": ItemIds,
                            "ItemSource": 32,
                            "Qty": charge_detail.get("qty")
                        }
                    ]
                }
                return create_recall_data


# Case xuôi
def process_store(file_path):
    from Dược.GET import get_info_patient, get_info_visit, get_store
    from Dược.PUT import data_of_update_status, update_status

    patientCodes = [24011977]

    sheet_name = "Data"

    # Đọc dữ liệu gốc từ tệp Excel
    excel_data = pd.read_excel(file_path, sheet_name=sheet_name)

    # Sử dụng một vòng lặp để xử lý từng hàng với từng entry_id tương ứng
    for patientCode, (index, row) in zip(patientCodes, excel_data.iterrows()):

        response_data, patient_id = get_info_patient(patientCode)

        response_data, visit_ids, visit_details = get_info_visit(patient_id)

        response_data = get_store()

        response_data, txVisitId = create_abc(visit_ids)

        response_data, pxId = create_bcd(txVisitId)

        response_data, StoreIds, ItemIds = create_cde(txVisitId)

        product_data = data_create_product(StoreIds, ItemIds)

        create_product(product_data)

        bill_data = data_create_bills(row, StoreIds, ItemIds, visit_details, patientCode, pxId)

        response_data, voucherid, id, createOn = create_bills(bill_data)

        response_data, voucherout_id = create_info_charge(voucherid)

        create_charge(voucherout_id)

        charge_data = data_of_charge_success(row, voucherid, id, createOn)

        response_data = charge_success(charge_data)

        status_data = data_of_update_status(voucherid)

        result_api = update_status(status_data, voucherid)

        return result_api


# Case ngược
def process_recall_store(file_path):
    from Dược.GET import choose_recall
    from Dược.PUT import data_of_recall_medicine, recall_medicine

    voucherNo = ["NT.RSL.24.06.0082"]

    sheet_name = "Data"

    # Đọc dữ liệu gốc từ tệp Excel
    excel_data = pd.read_excel(file_path, sheet_name=sheet_name)

    # Sử dụng một vòng lặp để xử lý từng hàng với từng entry_id tương ứng
    for voucherNo, (index, row) in zip(voucherNo, excel_data.iterrows()):
        response_data, voucherIds, recall_details, StoreIds = choose_recall(voucherNo)

        response_data, voucherout_id, itemId = create_info_charge(voucherIds)

        response_data, charge_details = create_charge(voucherout_id)

        recall_data = data_of_recall_medicine()

        recall_medicine(recall_data)

        create_recall_data = data_of_create_recall(row, StoreIds, itemId, recall_details, charge_details)

        response_data = create_recall(create_recall_data)

        return response_data

