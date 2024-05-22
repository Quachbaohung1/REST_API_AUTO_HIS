import requests
import pandas as pd
from copy import deepcopy


# Base url
base_url = "http://115.79.31.186:1096"

# Auth token
auth_token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IjM4MzkiLCJyb2xlIjoiQWRtaW4iLCJBY2NvdW50TmFtZSI6Imh1bmdxYiIsIkNsaWVudElwQWRkcmVzcyI6Ijo6MSIsIklzTG9jYWxJcCI6IlRydWUiLCJuYmYiOjE3MTUxODQ2NDIsImV4cCI6MTcxNTE4ODI0MiwiaWF0IjoxNzE1MTg0NjQyfQ.CihuC246iqFUos4MNZtNWs2q_SBOtmbXz4NRNuRQ4rg"


# Lấy thông tin tất cả các bệnh nhân
def create_information_patient():
    from Khám_bệnh_CDDV.GET import check_patient_in_room
    patient_ids = check_patient_in_room()
    url = f"{base_url}/pms/Patients/PatientIds"
    headers = {"Authorization": auth_token}
    data = patient_ids
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()


# Chọn bệnh nhân
def choose_patient():
    from Khám_bệnh_CDDV.GET import check_visit_enty
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
def start_service_designation(entry_data):
    all_infoa = []
    for entryId in entry_data:
        url = f"{base_url}/pms/VisitEntries/Ids?wardUnitId="
        headers = {"Authorization": auth_token}
        data = [entryId]
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        response_json = response.json()
        # In phản hồi JSON để kiểm tra cấu trúc
        print("Response JSON:", response_json)

        # Lặp qua từng từ điển trong danh sách
        for item in response_json:
            # Tạo một danh sách con chứa các giá trị
            info = {
                "onDate": item.get("onDate"),
                "dxByStaffId": int(item.get("dxByStaffId")),
                "dxICD": str(item.get("dxICD")),
                "dxText": str(item.get("dxText")),
                "entryId": int(item.get("entryId")),
                "wardUnitId": int(item.get("wardUnitId")),
                "insBenefitType": int(item.get("insBenefitType")),
                "insBenefitRatio": int(item.get("insBenefitRatio")),
            }
            # Thêm danh sách con vào danh sách all_info
            all_infoa.append(info)

            print("all_infoa:", all_infoa)

    return all_infoa


# Chỉ định dịch vụ
def create_service_designation(data):
    url = f"{base_url}/cis/LabExams/AddWithItems?ptFullAddress=5%2F49+Ntl%2C+Ph%C6%B0%E1%BB%9Dng+07%2C+Qu%E1%BA%ADn+B%C3%ACnh+Th%E1%BA%A1nh%2C+Th%C3%A0nh+ph%E1%BB%91+H%E1%BB%93+Ch%C3%AD+Minh"
    headers = {"Authorization": auth_token}
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    frVisitEntryId = response.json()["frVisitEntryId"]
    print("frVisitEntryId:", frVisitEntryId)  # In ra labExId
    return frVisitEntryId


# Dữ liệu của chỉ định dịch vụ
def data_of_create_service_designation(row, all_infoa, all_info):
    from Khám_bệnh_CDDV.GET import check_information_patient_subsequent, set_true
    visit_info_list = check_information_patient_subsequent(all_info)

    # Xử lý các giá trị null
    def handle_null(value):
        return str(value) if not pd.isna(value) else ''

    # Lấy thông tin từ all_info
    for visit_info in visit_info_list:
        PatientId = visit_info["patient_id"]
        InsCardId = visit_info["insCardId"]

        # Truyền PatientId vào hàm set_true()
        set_true(PatientId)

        for info in all_infoa:
            onDate = info.get("onDate", "")
            dxByStaffId = info.get("dxByStaffId", "")
            dxICD = info.get("dxICD", "")
            dxText = info.get("dxText", "")
            entryId = info.get("entryId", "")
            wardUnitId = info.get("wardUnitId", "")
            InsBenefitType = info.get("insBenefitType", 0)
            InsBenefitRatio = info.get("insBenefitRatio", 0)

            # Chuyển đổi giá trị "NonSubclinical" sang kiểu boolean
            NonSubclinical = False if str(row['NonSubclinical']).lower() == 'false' else True

            service_data = {
                "PatientId": PatientId,
                "RefNo": handle_null(row['RefNo']),
                "OnDate": onDate,
                "LabReqById": dxByStaffId,
                "LabReqNotes": handle_null(row['LabReqNotes']),
                "DxICD": dxICD,
                "DxText": dxText,
                "Attribute": 1,
                "FrVisitEntryId": entryId,
                "CreateOn": onDate,
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
                        "NonSubclinical": NonSubclinical,
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
                    "NonSubclinical": NonSubclinical,
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
            frVisitEntryId = create_service_designation(service_data)
            return frVisitEntryId

# Kiểm tra chỉ định dịch vụ
# def check_service_designation(row, all_infoa):
#     url = f"{base_url}/cis/LabExamItems/LabExamIds?ExcludedAttribute=&serviceTypeL0=&isLoadDelete=False"
#     headers = {"Authorization": auth_token}
#
#     # Get the labExId from data_of_create_service_designation
#     labExIds = data_of_create_service_designation(row, all_infoa)
#
#     if isinstance(labExIds, int):
#         labExIds = [labExIds]
#
#     for labExId in labExIds:
#         data = [labExId]
#         # Thực hiện yêu cầu POST để kiểm tra service designation
#         response = requests.post(url, json=data, headers=headers)
#         response.raise_for_status()
#
#         # In và trả về JSON phản hồi để kiểm tra và xác minh
#         response_json = response.json()
#         print("response_json", response_json)
#
#         return response_json



def generate_additional_data(original_data, num_records):
    new_data = []

    for _ in range(num_records):
        for _, row in original_data.iterrows():
            new_row = deepcopy(row)

            new_data.append(new_row)

    return pd.DataFrame(new_data)

def write_data_to_excel(file_path, sheet_name, data):
    # Ghi dữ liệu vào tệp Excel và ghi đè lên dữ liệu hiện có
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
        data.to_excel(writer, sheet_name=sheet_name, index=False)


def process_kb_CDDV():
    from Khám_bệnh_CDDV.PUT import update_information_patient_from_excel
    file_path = "D://HIS api automation/DataTest/Data_API_Khám_bệnh.xlsx"
    sheet_name = "Sheet1"

    # Đọc dữ liệu gốc từ tệp Excel
    excel_data = pd.read_excel(file_path, sheet_name=sheet_name)

    # Tạo dữ liệu bổ sung và ghi vào file Excel
    num_records_to_add = 2  # Số dòng dữ liệu bổ sung
    additional_data = generate_additional_data(excel_data.tail(1), num_records_to_add)
    write_data_to_excel(file_path, sheet_name, additional_data)

    # Đọc lại dữ liệu đã ghi vào file
    additional_data = pd.read_excel(file_path, sheet_name=sheet_name)
    # Thông tin
    frVisitEntryIds = []
    for index, row in additional_data.iterrows():
        # create_information_patient()
        frVisitEntryId = update_information_patient_from_excel(row)
        frVisitEntryIds.append(frVisitEntryId)
        print("frVisitEntryIds:", frVisitEntryIds)
    return frVisitEntryIds


process_kb_CDDV()