import requests
import pandas as pd


# Base url
base_url = "http://115.79.31.186:1096"

# Auth token
auth_token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IjM4MzkiLCJyb2xlIjoiQWRtaW4iLCJBY2NvdW50TmFtZSI6Imh1bmdxYiIsIkNsaWVudElwQWRkcmVzcyI6Ijo6MSIsIklzTG9jYWxJcCI6IlRydWUiLCJuYmYiOjE3MTUxODQ2NDIsImV4cCI6MTcxNTE4ODI0MiwiaWF0IjoxNzE1MTg0NjQyfQ.CihuC246iqFUos4MNZtNWs2q_SBOtmbXz4NRNuRQ4rg"


# Lấy thông tin tất cả các bệnh nhân
def create_information_patient():
    from Khám_bệnh.GET import check_patient_in_room
    patient_ids = check_patient_in_room()
    url = f"{base_url}/pms/Patients/PatientIds"
    headers = {"Authorization": auth_token}
    data = patient_ids
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()


# Chọn bệnh nhân
def choose_patient():
    from Khám_bệnh.GET import check_visit_enty
    visit_ids = check_visit_enty()
    visit_idas = []
    for visit_id in visit_ids:
        url = f"{base_url}/pms/VisitEntries/VisitIds"
        headers = {"Authorization": auth_token}
        data = [visit_id]
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        # Lặp qua danh sách các đối tượng JSON trong response.json()
        for item in response.json():
            visit_ida = item["visitId"]  # Trích xuất visitId từ mỗi đối tượng
            visit_idas.append(visit_ida)
    print("visit_idas", visit_idas)
    return visit_idas


# Mở màn hình chỉ định dịch vụ
def start_service_designation():
    from Khám_bệnh.GET import check_information_patient
    url = f"{base_url}/pms/VisitEntries/Ids?wardUnitId="
    headers = {"Authorization": auth_token}
    all_patient_info = check_information_patient()
    entryId = all_patient_info[0]
    data = [entryId]
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()


# Chỉ định dịch vụ
def create_service_designation(data):
    url = f"{base_url}/cis/LabExams/AddWithItems?ptFullAddress=5%2F49+Ntl%2C+Ph%C6%B0%E1%BB%9Dng+07%2C+Qu%E1%BA%ADn+B%C3%ACnh+Th%E1%BA%A1nh%2C+Th%C3%A0nh+ph%E1%BB%91+H%E1%BB%93+Ch%C3%AD+Minh"
    headers = {"Authorization": auth_token}
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()["labExId"]


# Dữ liệu của chỉ định dịch vụ
def data_of_create_service_designation(row):
    # Xử lý các giá trị null
    def handle_null(value):
        return str(value) if not pd.isna(value) else ''

    (onDate, dxByStaffId, dxICD, dxText, entryId, wardUnitId) = start_service_designation()
    (InsBenefitType, InsBenefitRatio, InsCardId) = KB_GET.get_information_txvisit()

    service_data = {
        "PatientId": handle_null(row['PatientId']),
        "RefNo": handle_null(row['RefNo']),
        "OnDate": onDate,
        "LabReqById": dxByStaffId,
        "LabReqNotes": handle_null(row['LabReqNotes']),
        "DxICD": dxICD,
        "DxText": dxText,
        "Attribute": int(row['Attribute']),
        "FrVisitEntryId": entryId,
        "CreateOn": KB_GET.date_formatted(),
        "CreateById": dxByStaffId,
        "Status": int(row['Status']),
        "WardUnitId": wardUnitId,
        "ServiceName": handle_null(row['ServiceName']),
        "LabExamItems": [
            {
                "LabExId": int(row['LabExId']),
                "MedServiceId": int(row['MedServiceId']),
                "PriceId": int(row['PriceId']),
                "InsBenefitType": InsBenefitType,
                "InsBenefitRatio": InsBenefitRatio,
                "InsCardId": InsCardId,
                "Qty": float(row['Qty']),
                "Price": float(row['Price']),
                "InsPrice": float(row['InsPrice']),
                "InsPriceRatio": int(row['InsPriceRatio']),
                "Amt": float(row['InsPrice']),
                "Attribute": int(row['Attribute']),
                "ByProviderId": int(row['ByProviderId']),
                "DiscAmtSeq": int(row['DiscAmtSeq']),
                "MedServiceTypeL0": int(row['MedServiceTypeL0']),
                "MedServiceTypeL2": int(row['MedServiceTypeL2']),
                "MedServiceTypeL3": int(row['MedServiceTypeL3']),
                "NonSubclinical": handle_null(row['NonSubclinical']),
                "TypeL0Code": handle_null(row['TypeL0Code']),
                "ByProviderCode": handle_null(row['ByProviderCode']),
                "ByProviderName": handle_null(row['ByProviderName']),
                "ServiceGroupName": handle_null(row['ServiceGroupName']),
                "ServiceTypeL3Name": handle_null(row['ServiceTypeL3Name']),
                "ServiceCode": handle_null(row['ServiceCode']),
                "ServiceName": handle_null(row['ServiceName']),
                "InsBenefitTypeName": handle_null(row['InsBenefitTypeName']),
                "ReqDate": handle_null(row['ReqDate']),
                "AttrString": handle_null(row['AttrString']),
                "PaidAttrString": handle_null(row['PaidAttrString']),
                "ServiceTypeOrderIndex": int(row['ServiceTypeOrderIndex']),
                "MedItemType": int(row['MedItemType']),
                "MedItem": handle_null(row['MedItem']),
                "Checked": handle_null(row['Checked']),
                "OnDate": onDate,
                "TotalInvoiceAmtRound": handle_null(row['TotalInvoiceAmtRound']),
                "TotalReceiptAmtRound": handle_null(row['TotalReceiptAmtRound']),
                "PtAmt": float(row['PtAmt']),
                "PtAmtRound": float(row['PtAmtRound']),
                "PtAmtPaid": float(row['PtAmtPaid']),
                "PtCoPayAmt": float(row['PtCoPayAmt']),
                "PtCoPayAmtRound": float(row['PtCoPayAmtRound']),
                "InsAmt": float(row['InsAmt']),
                "InsAmtRound": float(row['InsAmtRound']),
                "DiscAmt": float(row['DiscAmt']),
                "ReqBy": handle_null(row['ReqBy'])
            }
        ],
        "ItemI0": {
            "LabExId": int(row['LabExId']),
            "MedServiceId": int(row['MedServiceId']),
            "PriceId": int(row['PriceId']),
            "InsBenefitType": InsBenefitType,
            "InsBenefitRatio": InsBenefitRatio,
            "InsCardId": InsCardId,
            "Qty": float(row['Qty']),
            "Price": float(row['Price']),
            "InsPrice": float(row['InsPrice']),
            "InsPriceRatio": int(row['InsPriceRatio']),
            "Amt": float(row['InsPrice']),
            "Attribute": int(row['Attribute']),
            "ByProviderId": int(row['ByProviderId']),
            "DiscAmtSeq": int(row['DiscAmtSeq']),
            "MedServiceTypeL0": int(row['MedServiceTypeL0']),
            "MedServiceTypeL2": int(row['MedServiceTypeL2']),
            "MedServiceTypeL3": int(row['MedServiceTypeL3']),
            "NonSubclinical": handle_null(row['NonSubclinical']),
            "TypeL0Code": handle_null(row['TypeL0Code']),
            "ByProviderCode": handle_null(row['ByProviderCode']),
            "ByProviderName": handle_null(row['ByProviderName']),
            "ServiceGroupName": handle_null(row['ServiceGroupName']),
            "ServiceTypeL3Name": handle_null(row['ServiceTypeL3Name']),
            "ServiceCode": handle_null(row['ServiceCode']),
            "ServiceName": handle_null(row['ServiceName']),
            "InsBenefitTypeName": handle_null(row['InsBenefitTypeName']),
            "ReqDate": handle_null(row['ReqDate']),
            "AttrString": handle_null(row['AttrString']),
            "PaidAttrString": handle_null(row['PaidAttrString']),
            "ServiceTypeOrderIndex": int(row['ServiceTypeOrderIndex']),
            "MedItemType": int(row['MedItemType']),
            "MedItem": handle_null(row['MedItem']),
            "Checked": handle_null(row['Checked']),
            "OnDate": onDate,
            "TotalInvoiceAmtRound": handle_null(row['TotalInvoiceAmtRound']),
            "TotalReceiptAmtRound": handle_null(row['TotalReceiptAmtRound']),
            "PtAmt": float(row['PtAmt']),
            "PtAmtRound": float(row['PtAmtRound']),
            "PtAmtPaid": float(row['PtAmtPaid']),
            "PtCoPayAmt": float(row['PtCoPayAmt']),
            "PtCoPayAmtRound": float(row['PtCoPayAmtRound']),
            "InsAmt": float(row['InsAmt']),
            "InsAmtRound": float(row['InsAmtRound']),
            "DiscAmt": float(row['DiscAmt']),
            "ReqBy": handle_null(row['ReqBy'])
        },
        "FullAddress": handle_null(row['FullAddress'])
    }
    create_service_designation(service_data)
    return service_data


# Kiểm tra chỉ định dịch vụ
def check_service_designation(row):
    url = f"{base_url}/cis/LabExamItems/LabExamIds?ExcludedAttribute=&serviceTypeL0=&isLoadDelete=False"
    headers = {"Authorization": auth_token}
    labExId = data_of_create_service_designation(row)
    data = [labExId]
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()["labExId"]


def process_from_visit_service_designation():
    file_path = "D://HIS api automation/DataTest/Data_API_Khám_bệnh.xlsx"
    excel_data = pd.read_excel(file_path, sheet_name="Sheet1")
    for index, row in excel_data.iterrows():
        check_service_designation(row)


# Call

def process_test():
    from Khám_bệnh.PUT import update_information_patient_from_excel
    file_path = "C:\\Users\\Thanh Truc\\Desktop\\Book1.xlsx"
    excel_data = pd.read_excel(file_path, sheet_name="Sheet1")
    for index, row in excel_data.iterrows():
        create_information_patient()
        update_information_patient_from_excel(row)
        start_service_designation()



process_test()
