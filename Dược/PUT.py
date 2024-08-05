import pandas as pd
import requests
from datetime import datetime
import pytz
from Cấu_hình.Setup import base_url, auth_token


def update_status(data, voucherid):
    headers = {"Authorization": auth_token}
    try:
        url = f"{base_url}/ims/Vouchers/{voucherid}"
        response = requests.put(url, json=data, headers=headers)
        response.raise_for_status()
        result_api = response.status_code
        return result_api
    except requests.exceptions.RequestException as e:
        # Log the error for debugging purposes
        print(f"\nAn error occurred during patient creation: {e}")


def data_of_update_status(voucherid):
    def clean_data(value):
        return str(value) if not pd.isna(value) else None

    status_data = {
        "VoucherId": voucherid,
        "TxVisitId": None,
        "VisitEntryId": None,
        "ProcStatus": 4,
        "InvStatusDescription": None,
        "ProcStatusDescription": "Đã giao hàng",
        "CustomerName": None,
        "InvoiceText": None
    }
    return status_data


# Thực hiện thu hồi thuốc
def recall_medicine(data):
    headers = {"Authorization": auth_token}
    try:
        url = f"{base_url}/finance/AdvancePayments/Refund"
        response = requests.put(url, json=data, headers=headers)
        response.raise_for_status()
        result_api = response.status_code
        return result_api
    except requests.exceptions.RequestException as e:
        # Log the error for debugging purposes
        print(f"\nAn error occurred during patient creation: {e}")


def data_of_recall_medicine(row, Voucher_data):
    def clean_data(value):
        return str(value) if not pd.isna(value) else None

    for Voucher in Voucher_data:
        amt = Voucher.get("amt")
        recall_data = {
            "Amt": "-" + str(amt),
            "CreateById": Voucher.get("createById"),
            "PaymentDate": Voucher.get("paymentDate"),
            "Type": Voucher.get("type"),
            "Status": int(row['Status']),
            "IsRefund": True,
            "CancelNotes": str(row['CancelNotes']),
            "VoucherId": Voucher.get("VoucherId"),
            "RefundFrPmtId": Voucher.get("paymentId"),
            "RePaidForPmtId": clean_data(row['RePaidForPmtId']),
            "Prefix": None,
            "LastDxOn": clean_data(row['LastDxOn']),
            "RealRevenue": "-" + str(amt)
        }
    return recall_data


# Thực hiện update trạng thái
def update_status_recall(data, VoucherId):
    headers = {"Authorization": auth_token}
    try:
        url = f"{base_url}/ims/Vouchers/{VoucherId}"
        response = requests.put(url, json=data, headers=headers)
        response.raise_for_status()
        result_api = response.status_code
        return result_api
    except requests.exceptions.RequestException as e:
        # Log the error for debugging purposes
        print(f"\nAn error occurred during patient creation: {e}")


def data_of_update_status_recall(Voucher_data):
    from Tiếp_nhận.GET import CurrentServerDateTime
    date = CurrentServerDateTime()
    date = date.strip('"')
    # Chuyển đổi chuỗi thành đối tượng datetime
    date_obj = datetime.fromisoformat(date)

    # Chuyển đổi múi giờ nếu cần thiết (ở đây ta chuyển sang múi giờ UTC)
    date_obj = date_obj.astimezone(pytz.utc)

    for Voucher in Voucher_data:
        formatted_date_str = date_obj.strftime("%d/%m/%Y %H:%M:%S")

        status_recall_data = {
            "VoucherId": Voucher.get("voucherId"),
            "Description": f"Thu hồi và hoàn tiền : {formatted_date_str} - hungqb;",
            "TxVisitId": None,
            "VisitEntryId": None,
            "ProcStatus": 12,
            "Attribute": 5,
            "InvStatusDescription": None,
            "ProcStatusDescription": "Đã thu hồi",
            "CustomerName": None,
            "InvoiceText": None
        }
    return status_recall_data


# Duyệt phiếu đề nghị
def update_Statements(stmId):
    headers = {"Authorization": auth_token}
    try:
        url = f"{base_url}/ims/Statements/update/{stmId}"
        data = {
            "StmId": stmId,
            "Status": 4
        }
        response = requests.put(url, json=data, headers=headers)
        response.raise_for_status()
        result_api = response.status_code
        return result_api
    except requests.exceptions.RequestException as e:
        # Log the error for debugging purposes
        print(f"\nAn error occurred during patient creation: {e}")


# Click btn xác nhận nhập khoa
def update_confirmed_warehouse(data):
    headers = {"Authorization": auth_token}
    try:
        url = f"{base_url}/ims/Vouchers/ApproveVouIn/3"
        response = requests.put(url, json=data, headers=headers)
        response.raise_for_status()
        result_api = response.status_code
        return result_api
    except requests.exceptions.RequestException as e:
        # Log the error for debugging purposes
        print(f"\nAn error occurred during patient creation: {e}")


def data_of_update_confirmed_warehouse(response_data):
    confirmed_warehouse_data = {
        "VoucherId": response_data.get("voucherId"),
        "VoucherNo": response_data.get("voucherNo"),
        "Type": response_data.get("type"),
        "OnDate": response_data.get("onDate"),
        "Description": response_data.get("description"),
        "StoreId": response_data.get("storeId"),
        "StmId": response_data.get("stmId"),
        "TxVisitId": response_data.get("txVisitId"),
        "VisitEntryId": response_data.get("visitEntryId"),
        "RefVoucherId": response_data.get("refVoucherId"),
        "RefStoreId": response_data.get("refStoreId"),
        "InvSource": response_data.get("invSource"),
        "InvoiceNo": response_data.get("invoiceNo"),
        "InvoiceCode": response_data.get("invoiceCode"),
        "DeliverName": response_data.get("deliverName"),
        "DeliverPhone": response_data.get("deliverPhone"),
        "CreateById": response_data.get("createById"),
        "CreateOn": response_data.get("createOn"),
        "InvStatus": 2,
        "InvStatusDescription": "Đã cập nhật tồn kho",
        "ProcStatusDescription": None,
        "CustomerName": None,
        "InvoiceText": ""
    }
    return confirmed_warehouse_data