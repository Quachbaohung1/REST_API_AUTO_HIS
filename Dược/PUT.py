import pandas as pd
import requests
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


def data_of_recall_medicine():
    def clean_data(value):
        return str(value) if not pd.isna(value) else None

    recall_data = {
        "Amt": -18168.0,
        "CreateById": 3839,
        "PaymentDate": "2024-06-18T09:58:06.2581436+07:00",
        "Type": 1,
        "Status": 1,
        "IsRefund": True,
        "CancelNotes": "z",
        "VoucherId": 90186,
        "RefundFrPmtId": 62454,
        "RePaidForPmtId": None,
        "Prefix": None,
        "LastDxOn": None,
        "RealRevenue": -18168.0
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


def data_of_update_status_recall():
    def clean_data(value):
        return str(value) if not pd.isna(value) else None

    status_recall_data = {
        "VoucherId": 90186,
        "Description": "Thu hồi và hoàn tiền : 18/06/2024 09:58:08 - hungqb;",
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
