import random

import requests
import pandas as pd
from copy import deepcopy
from Cấu_hình.Setup import base_url, auth_token
from Tiếp_nhận.POST import compare_data, copy_sheet_values


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
                # "dxByStaffId": int(item.get("dxByStaffId")),
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
def create_service_designation(data, verify_data):
    url = f"{base_url}/cis/LabExams/AddWithItems?ptFullAddress=5%2F49+Ntl%2C+Ph%C6%B0%E1%BB%9Dng+07%2C+Qu%E1%BA%ADn+B%C3%ACnh+Th%E1%BA%A1nh%2C+Th%C3%A0nh+ph%E1%BB%91+H%E1%BB%93+Ch%C3%AD+Minh"
    headers = {"Authorization": auth_token}
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        frVisitEntryId = response_data["frVisitEntryId"]
        print("frVisitEntryId:", frVisitEntryId)
        result = compare_data(response_data, verify_data)
        return response_data, frVisitEntryId, result
    except requests.exceptions.RequestException as e:
        # Log the error for debugging purposes
        print(f"\nAn error occurred during patient creation: {e}")


# Dữ liệu của chỉ định dịch vụ
def data_of_create_service_designation(row, all_infoa, all_info, excel_data):
    from Khám_bệnh_CDDV.GET import check_information_patient_subsequent, set_true
    visit_info_list = check_information_patient_subsequent(all_info)

    # Xử lý các giá trị null
    def handle_null(value):
        return value if not pd.isna(value) else None

    # Lấy thông tin từ all_info
    for visit_info in visit_info_list:
        PatientId = visit_info["patient_id"]
        InsCardId = visit_info["insCardId"]

        # Truyền PatientId vào hàm set_true()
        set_true(PatientId)

        for info in all_infoa:
            dxICD = info.get("dxICD", "")
            dxText = info.get("dxText", "")
            entryId = info.get("entryId", "")
            wardUnitId = info.get("wardUnitId", "")
            InsBenefitType = info.get("insBenefitType", 0)
            InsBenefitRatio = info.get("insBenefitRatio", 0)

            NonSubclinical = False if str(row['NonSubclinical']).lower() == 'false' else True
            OnDate = None if pd.isna(row['OnDate2']) else str(row['OnDate2'])
            CreateById = None if pd.isna(row['CreateById']) else int(row['CreateById'])
            dxByStaffId = None if pd.isna(row['DxByStaffId']) else int(row['DxByStaffId'])

            InsPriceRatio = None if pd.isna(row['InsPriceRatio']) else int(row['InsPriceRatio'])

            LabExamItems_datas = []

            for index, lab_row in excel_data.iterrows():
                ByProviderId = None if pd.isna(lab_row['ByProviderId']) else int(lab_row['ByProviderId'])
                MedServiceId = None if pd.isna(lab_row['MedServiceId']) else int(lab_row.get('MedServiceId'))
                PriceId = None if pd.isna(lab_row['PriceId.1']) else int(lab_row.get('PriceId.1'))
                MedServiceTypeL0 = None if pd.isna(lab_row['MedServiceTypeL0']) else int(lab_row.get('MedServiceTypeL0'))
                MedServiceTypeL2 = None if pd.isna(lab_row['MedServiceTypeL2']) else int(lab_row.get('MedServiceTypeL2'))
                MedServiceTypeL3 = None if pd.isna(lab_row['MedServiceTypeL3']) else int(lab_row.get('MedServiceTypeL3'))
                SpecimenTemplateCode = None if pd.isna(lab_row['SpecimenTemplateCode']) else int(lab_row.get("SpecimenTemplateCode"))
                SubClinicUIType = None if pd.isna(lab_row['SubClinicUIType']) else int(lab_row.get("SubClinicUIType"))

                # Handle quantity
                Qty = random.randint(1, 60)

                for _ in range(Qty):
                    LabExamItems_data = {
                        "LabExId": int(lab_row.get('LabExId', 0)),
                        "SpecimenTemplateCode": SpecimenTemplateCode,
                        "SubClinicUIType": SubClinicUIType,
                        "MedServiceId": MedServiceId,
                        "PriceId": PriceId,
                        "InsBenefitType": InsBenefitType,
                        "InsBenefitRatio": InsBenefitRatio,
                        "InsCardId": InsCardId,
                        "Qty": 1,
                        "Price": handle_null(lab_row.get('Price.1')),
                        "InsPrice": handle_null(lab_row.get('InsPrice.1')),
                        "InsPriceRatio": InsPriceRatio,
                        "Amt": handle_null(lab_row.get('InsPrice.1')),
                        "Attribute": int(lab_row.get('Attribute', 0)),
                        "ByProviderId": ByProviderId,
                        "DiscAmtSeq": handle_null(lab_row.get('DiscAmtSeq', None)),
                        "MedServiceTypeL0": MedServiceTypeL0,
                        "MedServiceTypeL2": MedServiceTypeL2,
                        "MedServiceTypeL3": MedServiceTypeL3,
                        "NonSubclinical": NonSubclinical,
                        "TypeL0Code": handle_null(lab_row.get('TypeL0Code', None)),
                        "ByProviderCode": handle_null(lab_row.get('ByProviderCode', None)),
                        "ByProviderName": handle_null(lab_row.get('ByProviderName', None)),
                        "ServiceGroupName": handle_null(lab_row.get('ServiceGroupName', None)),
                        "ServiceTypeL3Name": handle_null(lab_row.get('ServiceTypeL3Name', None)),
                        "ServiceCode": handle_null(lab_row.get('ServiceCode', None)),
                        "ServiceName": handle_null(lab_row.get('ServiceName', None)),
                        "InsBenefitTypeName": handle_null(lab_row.get('InsBenefitTypeName', None)),
                        "ReqDate": handle_null(lab_row.get('ReqDate', None)),
                        "AttrString": handle_null(lab_row.get('AttrString', None)),
                        "PaidAttrString": handle_null(lab_row.get('PaidAttrString', None)),
                        "ServiceTypeOrderIndex": int(lab_row.get('ServiceTypeOrderIndex', 0)),
                        "MedItemType": lab_row.get('MedItemType', None),
                        "MedItem": handle_null(lab_row.get('MedItem', None)),
                        "Checked": handle_null(lab_row.get('Checked', None)),
                        "OnDate": OnDate,
                        "TotalInvoiceAmtRound": handle_null(lab_row.get('TotalInvoiceAmtRound', None)),
                        "TotalReceiptAmtRound": handle_null(lab_row.get('TotalReceiptAmtRound', None)),
                        "PtAmt": float(lab_row.get('PtAmt', 0)),
                        "PtAmtRound": float(lab_row.get('PtAmtRound', 0)),
                        "PtAmtPaid": float(lab_row.get('PtAmtPaid', 0)),
                        "PtCoPayAmt": float(lab_row.get('PtCoPayAmt', 0)),
                        "PtCoPayAmtRound": float(lab_row.get('PtCoPayAmtRound', 0)),
                        "InsAmt": float(lab_row.get('InsAmt', 0)),
                        "InsAmtRound": float(lab_row.get('InsAmtRound', 0)),
                        "DiscAmt": float(lab_row.get('DiscAmt', 0)),
                        "ReqBy": handle_null(lab_row.get('ReqBy', None))
                    }
                    LabExamItems_datas.append(LabExamItems_data)

            service_data = {
                "PatientId": int(PatientId),
                "RefNo": handle_null(row['RefNo']),
                "OnDate": OnDate,
                "LabReqById": dxByStaffId,
                "LabReqNotes": handle_null(row['LabReqNotes']),
                "DxICD": dxICD,
                "DxText": dxText,
                "Attribute": 1,
                "FrVisitEntryId": int(entryId),
                "CreateOn": OnDate,
                "CreateById": CreateById,
                "Status": int(row['Status']),
                "WardUnitId": int(wardUnitId),
                "ServiceName": handle_null(row['ServiceName']),
                "LabExamItems": LabExamItems_datas,
                "ItemI0": LabExamItems_datas[0] if LabExamItems_datas else None,  # Chỉ lấy dịch vụ đầu tiên
                "FullAddress": handle_null(row['FullAddress'])
            }

            # Kiểm tra xem loại bảo hiểm có phải là BHYT hay không
            if handle_null(row['MedServiceTypeL3']) != 66 and handle_null(row['MedServiceTypeL3']) == "nan":
                if isinstance(service_data["LabExamItems"], list):
                    for item in service_data["LabExamItems"]:
                        if isinstance(item, dict) and "SpecimenTemplateCode" in item:
                            del item["SpecimenTemplateCode"]
                elif isinstance(service_data["LabExamItems"], dict):
                    del service_data["LabExamItems"]["SpecimenTemplateCode"]

                if isinstance(service_data["ItemI0"], dict) and "SpecimenTemplateCode" in service_data["ItemI0"]:
                    del service_data["ItemI0"]["SpecimenTemplateCode"]

            if pd.isna(row['SubClinicUIType']).any():
                if isinstance(service_data["LabExamItems"], list):
                    for item in service_data["LabExamItems"]:
                        if isinstance(item, dict) and "SubClinicUIType" in item:
                            del item["SubClinicUIType"]
                elif isinstance(service_data["LabExamItems"], dict):
                    del service_data["LabExamItems"]["SubClinicUIType"]

                if isinstance(service_data["ItemI0"], dict) and "SubClinicUIType" in service_data["ItemI0"]:
                    del service_data["ItemI0"]["SubClinicUIType"]

            return service_data


# Dữ liệu của chỉ định dịch vụ nội trú
def data_of_create_service_designation_NT(row, all_infoa, all_info, excel_data, txVisitId, wardAdmId):
    from Khám_bệnh_CDDV.GET import check_information_patient_subsequent, set_true
    visit_info_list = check_information_patient_subsequent(all_info)

    # Xử lý các giá trị null
    def handle_null(value):
        return value if not pd.isna(value) else None

    # Lấy thông tin từ all_info
    for visit_info in visit_info_list:
        PatientId = visit_info["patient_id"]
        InsCardId = visit_info["insCardId"]

        # Truyền PatientId vào hàm set_true()
        set_true(PatientId)

        for info in all_infoa:
            dxICD = info.get("dxICD", "")
            dxText = info.get("dxText", "")
            InsBenefitType = info.get("insBenefitType", 0)
            InsBenefitRatio = info.get("insBenefitRatio", 0)

            NonSubclinical = False if str(row['NonSubclinical']).lower() == 'false' else True
            OnDate = None if pd.isna(row['OnDate2']) else str(row['OnDate2'])
            CreateById = None if pd.isna(row['CreateById']) else int(row['CreateById'])
            dxByStaffId = None if pd.isna(row['DxByStaffId']) else int(row['DxByStaffId'])

            InsPriceRatio = None if pd.isna(row['InsPriceRatio']) else int(row['InsPriceRatio'])

            LabExamItems_datas = []

            for index, lab_row in excel_data.iterrows():
                ByProviderId = None if pd.isna(lab_row['ByProviderId']) else int(lab_row['ByProviderId'])
                MedServiceId = None if pd.isna(lab_row['MedServiceId']) else int(lab_row.get('MedServiceId'))
                PriceId = None if pd.isna(lab_row['PriceId.1']) else int(lab_row.get('PriceId.1'))
                MedServiceTypeL0 = None if pd.isna(lab_row['MedServiceTypeL0']) else int(lab_row.get('MedServiceTypeL0'))
                MedServiceTypeL2 = None if pd.isna(lab_row['MedServiceTypeL2']) else int(lab_row.get('MedServiceTypeL2'))
                MedServiceTypeL3 = None if pd.isna(lab_row['MedServiceTypeL3']) else int(lab_row.get('MedServiceTypeL3'))
                SpecimenTemplateCode = None if pd.isna(lab_row['SpecimenTemplateCode']) else int(lab_row.get("SpecimenTemplateCode"))
                SubClinicUIType = None if pd.isna(lab_row['SubClinicUIType']) else int(lab_row.get("SubClinicUIType"))

                # Handle quantity
                Qty = random.randint(1, 60)

                for _ in range(Qty):
                    LabExamItems_data = {
                        "LabExId": int(lab_row.get('LabExId', 0)),
                        "SpecimenTemplateCode": SpecimenTemplateCode,
                        "SubClinicUIType": SubClinicUIType,
                        "MedServiceId": MedServiceId,
                        "PriceId": PriceId,
                        "InsBenefitType": InsBenefitType,
                        "InsBenefitRatio": InsBenefitRatio,
                        "InsCardId": InsCardId,
                        "Qty": 1,
                        "Price": handle_null(lab_row.get('Price.1')),
                        "InsPrice": handle_null(lab_row.get('InsPrice.1')),
                        "InsPriceRatio": InsPriceRatio,
                        "Amt": handle_null(lab_row.get('InsPrice.1')),
                        "Attribute": int(lab_row.get('Attribute', 0)),
                        "ByProviderId": ByProviderId,
                        "DiscAmtSeq": handle_null(lab_row.get('DiscAmtSeq', None)),
                        "MedServiceTypeL0": MedServiceTypeL0,
                        "MedServiceTypeL2": MedServiceTypeL2,
                        "MedServiceTypeL3": MedServiceTypeL3,
                        "NonSubclinical": NonSubclinical,
                        "TypeL0Code": handle_null(lab_row.get('TypeL0Code', None)),
                        "ByProviderCode": handle_null(lab_row.get('ByProviderCode', None)),
                        "ByProviderName": handle_null(lab_row.get('ByProviderName', None)),
                        "ServiceGroupName": handle_null(lab_row.get('ServiceGroupName', None)),
                        "ServiceTypeL3Name": handle_null(lab_row.get('ServiceTypeL3Name', None)),
                        "ServiceCode": handle_null(lab_row.get('ServiceCode', None)),
                        "ServiceName": handle_null(lab_row.get('ServiceName', None)),
                        "InsBenefitTypeName": handle_null(lab_row.get('InsBenefitTypeName', None)),
                        "ReqDate": handle_null(lab_row.get('ReqDate', None)),
                        "AttrString": handle_null(lab_row.get('AttrString', None)),
                        "PaidAttrString": handle_null(lab_row.get('PaidAttrString', None)),
                        "ServiceTypeOrderIndex": int(lab_row.get('ServiceTypeOrderIndex', 0)),
                        "MedItemType": lab_row.get('MedItemType', None),
                        "MedItem": handle_null(lab_row.get('MedItem', None)),
                        "Checked": handle_null(lab_row.get('Checked', None)),
                        "OnDate": OnDate,
                        "TotalInvoiceAmtRound": handle_null(lab_row.get('TotalInvoiceAmtRound', None)),
                        "TotalReceiptAmtRound": handle_null(lab_row.get('TotalReceiptAmtRound', None)),
                        "PtAmt": float(lab_row.get('PtAmt', 0)),
                        "PtAmtRound": float(lab_row.get('PtAmtRound', 0)),
                        "PtAmtPaid": float(lab_row.get('PtAmtPaid', 0)),
                        "PtCoPayAmt": float(lab_row.get('PtCoPayAmt', 0)),
                        "PtCoPayAmtRound": float(lab_row.get('PtCoPayAmtRound', 0)),
                        "InsAmt": float(lab_row.get('InsAmt', 0)),
                        "InsAmtRound": float(lab_row.get('InsAmtRound', 0)),
                        "DiscAmt": float(lab_row.get('DiscAmt', 0)),
                        "ReqBy": handle_null(lab_row.get('ReqBy', None))
                    }
                    LabExamItems_datas.append(LabExamItems_data)

            service_data = {
                "PatientId": int(PatientId),
                "RefNo": handle_null(row['RefNo']),
                "OnDate": OnDate,
                "LabReqById": dxByStaffId,
                "LabReqNotes": handle_null(row['LabReqNotes']),
                "DxICD": dxICD,
                "DxText": dxText,
                "Attribute": 2,
                "FrWardAdmId": wardAdmId,
                "FrTxVisitId": txVisitId,
                "CreateOn": OnDate,
                "CreateById": CreateById,
                "Status": int(row['Status']),
                "WardUnitId": 659,
                "ServiceName": None,
                "LabExamItems": LabExamItems_datas,
                "ItemI0": LabExamItems_datas[0] if LabExamItems_datas else None,  # Chỉ lấy dịch vụ đầu tiên
                "FullAddress": handle_null(row['FullAddress'])
            }

            # Kiểm tra xem loại bảo hiểm có phải là BHYT hay không
            if handle_null(row['MedServiceTypeL3']) != 66 and handle_null(row['MedServiceTypeL3']) == "nan":
                if isinstance(service_data["LabExamItems"], list):
                    for item in service_data["LabExamItems"]:
                        if isinstance(item, dict) and "SpecimenTemplateCode" in item:
                            del item["SpecimenTemplateCode"]
                elif isinstance(service_data["LabExamItems"], dict):
                    del service_data["LabExamItems"]["SpecimenTemplateCode"]

                if isinstance(service_data["ItemI0"], dict) and "SpecimenTemplateCode" in service_data["ItemI0"]:
                    del service_data["ItemI0"]["SpecimenTemplateCode"]

            if pd.isna(row['SubClinicUIType']).any():
                if isinstance(service_data["LabExamItems"], list):
                    for item in service_data["LabExamItems"]:
                        if isinstance(item, dict) and "SubClinicUIType" in item:
                            del item["SubClinicUIType"]
                elif isinstance(service_data["LabExamItems"], dict):
                    del service_data["LabExamItems"]["SubClinicUIType"]

                if isinstance(service_data["ItemI0"], dict) and "SubClinicUIType" in service_data["ItemI0"]:
                    del service_data["ItemI0"]["SubClinicUIType"]

            return service_data


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


def process_check_patient_in_room():
    from Khám_bệnh_CDDV.GET import get_all_info
    # Thông tin
    entry_ids = [44715, 44716, 44717, 44718, 44719, 44720, 44721, 44722, 44723, 44724, 44725, 44726, 44727, 44728, 44729, 44730, 44731, 44732, 44733, 44734, 44735, 44736, 44737, 44738, 44739, 44740, 44741, 44742, 44743, 44744, 44745, 44746, 44747, 44748, 44749, 44750, 44751, 44752, 44753, 44754, 44755, 44756, 44757, 44758, 44759, 44760, 44761, 44762, 44763, 44764, 44765, 44766, 44767, 44768, 44769, 44770, 44771, 44772, 44773, 44774, 44775, 44776, 44777, 44778, 44779, 44780, 44781, 44782, 44783, 44784, 44785, 44786, 44787, 44788, 44789, 44790, 44791, 44792, 44793, 44794, 44795, 44796, 44797, 44798, 44799, 44800, 44801, 44802, 44803, 44804, 44805, 44806, 44807, 44808, 44809, 44810, 44811, 44812, 44813, 44814, 44815, 44816, 44817, 44818, 44819, 44820, 44821, 44822, 44823, 44824, 44825, 44826, 44827, 44828, 44829, 44830, 44831, 44832, 44833, 44834, 44835, 44836, 44837, 44838, 44839, 44840, 44841, 44842, 44843, 44844, 44845, 44846, 44847, 44848, 44849, 44850, 44851, 44852, 44853, 44854, 44855, 44856, 44857, 44858, 44859, 44860, 44861, 44862, 44863, 44864, 44865, 44866, 44867, 44868, 44869, 44870, 44871, 44872, 44873, 44874, 44875, 44876, 44877, 44878, 44879, 44880, 44881, 44882, 44883, 44884, 44885, 44886, 44887, 44888, 44889, 44890, 44891, 44892, 44893, 44894, 44895, 44896, 44897, 44898, 44899, 44900, 44901, 44902, 44903, 44904, 44905, 44906, 44907, 44908, 44909, 44910, 44911, 44912, 44913, 44914, 44915, 44916, 44917, 44918, 44919, 44920, 44921, 44922, 44923, 44924, 44925, 44926, 44927, 44928, 44929, 44930, 44931, 44932, 44933, 44934, 44935, 44936, 44937, 44938, 44939, 44940, 44941, 44942, 44943, 44944, 44945, 44946, 44947, 44948, 44949, 44950, 44951, 44952, 44953, 44954, 44955, 44956, 44957, 44958, 44959, 44960, 44961, 44962, 44963, 44964, 44965, 44966, 44967, 44968, 44969, 44970, 44971, 44972, 44973, 44974, 44975, 44976, 44977, 44978, 44979, 44980, 44981, 44982, 44983, 44984, 44985, 44986, 44987, 44988, 44989, 44990, 44991, 44993, 44994, 44995, 44996, 44997, 44998, 44999, 45000, 45001, 45002, 45003, 45004, 45005, 45006, 45007, 45008, 45009, 45010, 45011, 45012, 45013, 45014, 45015, 45016, 45017, 45018, 45019, 45020, 45021, 45022, 45023, 45024, 45025, 45026, 45027, 45028, 45029, 45030, 45031, 45032, 45033, 45034, 45035, 45036, 45037, 45038, 45039, 45040, 45041, 45042, 45043, 45044, 45045, 45046, 45047, 45048, 45049, 45050, 45051, 45052, 45053, 45054, 45055, 45056, 45057, 45058, 45059, 45060, 45061, 45062, 45063, 45064, 45065, 45066, 45067, 45068, 45069, 45070, 45071, 45072, 45073, 45074, 45075, 45076, 45077, 45078, 45079, 45080, 45081, 45082, 45083, 45084, 45085, 45086, 45087, 45088, 45089, 45090, 45091, 45092, 45093, 45094, 45095, 45096, 45097, 45098, 45099, 45100, 45101, 45102, 45103, 45104, 45105, 45106, 45107, 45108, 45109, 45110, 45111, 45112, 45113, 45114, 45115, 45116, 45117, 45118, 45119, 45120, 45121, 45122, 45123, 45124, 45125, 45127, 45128, 45129, 45130, 45131, 45132, 45133, 45134, 45135, 45136, 45137, 45138, 45139, 45140, 45141, 45142, 45143, 45144, 45145, 45146, 45147, 45148, 45149, 45150, 45151, 45152, 45153, 45154, 45155, 45156, 45157, 45158, 45159, 45160, 45161, 45162, 45163, 45164, 45165, 45166, 45167, 45168, 45169, 45170, 45171, 45172, 45173, 45174, 45175, 45176, 45177, 45178, 45179, 45180, 45181, 45182, 45183, 45184, 45185, 45186, 45187, 45188, 45189, 45190, 45191, 45192, 45193, 45194, 45195, 45196, 45197, 45198, 45199, 45200, 45201, 45202, 45203, 45204, 45206, 45207, 45208, 45209, 45210, 45211, 45212, 45213, 45214, 45215, 45216, 45217, 45218, 45219, 45220, 45221, 45222, 45223, 45224, 45225, 45226, 45227, 45228, 45229, 45230, 45231, 45232, 45233, 45234, 45235, 45236, 45237, 45238, 45239, 45240, 45241, 45242, 45243, 45244, 45245, 45246, 45247, 45248, 45249, 45250, 45251, 45252, 45253, 45254, 45255, 45256, 45257, 45258, 45259, 45260, 45261, 45262, 45263, 45264, 45265, 45266, 45267, 45268, 45269, 45270, 45271, 45272, 45273, 45274, 45275, 45276, 45277, 45278, 45279, 45280, 45281, 45282, 45283, 45284, 45285, 45286, 45287, 45288, 45289, 45290, 45291, 45292, 45293, 45294, 45295, 45296, 45297, 45298, 45299, 45300, 45301, 45302, 45303, 45304, 45305, 45306, 45307, 45308, 45309, 45310, 45311, 45312, 45313, 45314, 45315, 45316, 45317, 45318, 45319, 45320, 45321, 45322, 45323, 45324, 45325, 45326, 45327, 45328, 45329, 45330, 45331, 45332, 45333, 45334, 45335, 45336, 45337, 45338, 45339, 45340, 45341, 45342, 45343, 45344, 45345, 45346, 45347, 45348, 45349, 45350, 45351, 45352, 45353, 45354, 45355, 45356, 45357, 45358, 45359, 45360, 45361, 45362, 45363, 45364, 45365, 45366, 45367, 45368, 45369, 45370, 45371, 45372, 45373, 45374, 45375, 45376, 45377, 45378, 45379, 45380, 45381, 45382, 45383, 45384, 45385, 45386, 45387, 45388, 45389, 45390, 45391, 45392, 45393, 45394, 45395, 45396, 45397, 45398, 45399, 45400, 45401, 45402, 45403, 45404, 45405, 45406, 45407, 45408, 45409, 45410, 45411, 45412, 45413, 45414, 45415, 45416, 45417, 45418, 45419, 45420, 45421, 45422, 45423, 45424, 45425, 45426, 45427, 45428, 45429, 45430, 45431, 45432, 45433, 45434, 45435, 45436, 45437, 45438, 45439, 45440, 45441, 45442, 45443, 45444, 45445, 45446, 45447, 45448, 45449, 45450, 45451, 45452, 45453, 45454, 45455, 45456, 45457, 45458, 45459, 45460, 45461, 45462, 45463, 45464, 45465, 45466, 45467, 45468, 45469, 45470, 45471, 45472, 45473, 45474, 45475, 45476, 45477, 45478, 45479, 45480, 45481, 45482, 45483, 45484, 45485, 45486, 45487, 45488, 45489, 45490, 45491, 45492, 45493, 45494, 45495, 45496, 45497, 45498, 45499, 45500, 45501, 45502, 45503, 45504, 45505, 45506, 45507, 45508, 45509, 45510, 45511, 45512, 45513, 45514, 45515, 45516, 45517, 45518, 45519, 45520, 45521, 45522, 45523, 45524, 45525, 45526, 45527, 45528, 45529, 45530, 45531, 45532, 45533, 45534, 45535, 45536, 45537, 45538, 45539, 45540, 45541, 45542, 45543, 45544, 45545, 45546, 45547, 45548, 45549, 45550, 45551, 45552, 45553, 45554, 45555, 45556, 45557, 45558, 45559, 45560, 45561, 45562, 45563, 45564, 45565, 45566, 45567, 45568, 45569, 45570, 45571, 45572, 45573, 45574, 45575, 45576, 45577, 45578, 45579, 45580, 45581, 45582, 45583, 45584, 45585, 45586, 45587, 45588, 45589, 45590, 45591, 45592, 45593, 45594, 45595, 45596, 45597, 45598, 45599, 45600, 45601, 45602, 45603, 45604, 45605, 45606, 45607, 45608, 45609, 45610, 45611, 45612, 45613, 45614, 45615, 45616, 45617, 45618, 45619, 45620, 45621, 45622, 45623, 45624, 45625, 45626, 45627, 45628, 45629, 45630, 45631, 45632, 45633, 45634, 45635, 45636, 45637, 45638, 45639, 45640, 45641, 45642, 45643, 45644, 45645, 45646, 45647, 45648, 45649, 45650, 45651, 45652, 45653, 45654, 45655, 45656, 45657, 45658, 45659, 45660, 45661, 45662, 45663, 45664, 45665, 45666, 45667, 45668, 45669, 45670, 45671, 45672, 45673, 45674, 45675, 45676, 45677, 45678, 45679, 45680, 45681, 45682, 45683, 45684, 45685, 45686, 45687, 45688, 45689, 45690, 45691, 45692, 45693, 45694, 45695, 45696, 45697, 45698, 45699, 45700, 45701, 45702, 45703, 45704, 45705, 45706, 45707, 45708, 45709, 45710, 45711, 45712, 45713, 45714, 45715, 45716, 45717]

    for entry_id in entry_ids:
        all_info = get_all_info(entry_id)
        print("all_info:", all_info)
        if len(all_info) == 0:
            print("No information about patients.")
            return []
        return all_info


def process_insert_info_patient(test_data, testcase_id):
    from Khám_bệnh_CDDV.GET import get_all_info
    from Khám_bệnh_CDDV.PUT import prepare_information_data, update_information_patient
    test_data = test_data[test_data['TestCaseId'] == testcase_id]

    # Đọc dữ liệu gốc từ tệp Excel
    excel_data = test_data

    # Thông tin
    entry_ids = [44715, 44716, 44717, 44718, 44719, 44720, 44721, 44722, 44723, 44724, 44725, 44726, 44727, 44728, 44729, 44730, 44731, 44732, 44733, 44734, 44735, 44736, 44737, 44738, 44739, 44740, 44741, 44742, 44743, 44744, 44745, 44746, 44747, 44748, 44749, 44750, 44751, 44752, 44753, 44754, 44755, 44756, 44757, 44758, 44759, 44760, 44761, 44762, 44763, 44764, 44765, 44766, 44767, 44768, 44769, 44770, 44771, 44772, 44773, 44774, 44775, 44776, 44777, 44778, 44779, 44780, 44781, 44782, 44783, 44784, 44785, 44786, 44787, 44788, 44789, 44790, 44791, 44792, 44793, 44794, 44795, 44796, 44797, 44798, 44799, 44800, 44801, 44802, 44803, 44804, 44805, 44806, 44807, 44808, 44809, 44810, 44811, 44812, 44813, 44814, 44815, 44816, 44817, 44818, 44819, 44820, 44821, 44822, 44823, 44824, 44825, 44826, 44827, 44828, 44829, 44830, 44831, 44832, 44833, 44834, 44835, 44836, 44837, 44838, 44839, 44840, 44841, 44842, 44843, 44844, 44845, 44846, 44847, 44848, 44849, 44850, 44851, 44852, 44853, 44854, 44855, 44856, 44857, 44858, 44859, 44860, 44861, 44862, 44863, 44864, 44865, 44866, 44867, 44868, 44869, 44870, 44871, 44872, 44873, 44874, 44875, 44876, 44877, 44878, 44879, 44880, 44881, 44882, 44883, 44884, 44885, 44886, 44887, 44888, 44889, 44890, 44891, 44892, 44893, 44894, 44895, 44896, 44897, 44898, 44899, 44900, 44901, 44902, 44903, 44904, 44905, 44906, 44907, 44908, 44909, 44910, 44911, 44912, 44913, 44914, 44915, 44916, 44917, 44918, 44919, 44920, 44921, 44922, 44923, 44924, 44925, 44926, 44927, 44928, 44929, 44930, 44931, 44932, 44933, 44934, 44935, 44936, 44937, 44938, 44939, 44940, 44941, 44942, 44943, 44944, 44945, 44946, 44947, 44948, 44949, 44950, 44951, 44952, 44953, 44954, 44955, 44956, 44957, 44958, 44959, 44960, 44961, 44962, 44963, 44964, 44965, 44966, 44967, 44968, 44969, 44970, 44971, 44972, 44973, 44974, 44975, 44976, 44977, 44978, 44979, 44980, 44981, 44982, 44983, 44984, 44985, 44986, 44987, 44988, 44989, 44990, 44991, 44993, 44994, 44995, 44996, 44997, 44998, 44999, 45000, 45001, 45002, 45003, 45004, 45005, 45006, 45007, 45008, 45009, 45010, 45011, 45012, 45013, 45014, 45015, 45016, 45017, 45018, 45019, 45020, 45021, 45022, 45023, 45024, 45025, 45026, 45027, 45028, 45029, 45030, 45031, 45032, 45033, 45034, 45035, 45036, 45037, 45038, 45039, 45040, 45041, 45042, 45043, 45044, 45045, 45046, 45047, 45048, 45049, 45050, 45051, 45052, 45053, 45054, 45055, 45056, 45057, 45058, 45059, 45060, 45061, 45062, 45063, 45064, 45065, 45066, 45067, 45068, 45069, 45070, 45071, 45072, 45073, 45074, 45075, 45076, 45077, 45078, 45079, 45080, 45081, 45082, 45083, 45084, 45085, 45086, 45087, 45088, 45089, 45090, 45091, 45092, 45093, 45094, 45095, 45096, 45097, 45098, 45099, 45100, 45101, 45102, 45103, 45104, 45105, 45106, 45107, 45108, 45109, 45110, 45111, 45112, 45113, 45114, 45115, 45116, 45117, 45118, 45119, 45120, 45121, 45122, 45123, 45124, 45125, 45127, 45128, 45129, 45130, 45131, 45132, 45133, 45134, 45135, 45136, 45137, 45138, 45139, 45140, 45141, 45142, 45143, 45144, 45145, 45146, 45147, 45148, 45149, 45150, 45151, 45152, 45153, 45154, 45155, 45156, 45157, 45158, 45159, 45160, 45161, 45162, 45163, 45164, 45165, 45166, 45167, 45168, 45169, 45170, 45171, 45172, 45173, 45174, 45175, 45176, 45177, 45178, 45179, 45180, 45181, 45182, 45183, 45184, 45185, 45186, 45187, 45188, 45189, 45190, 45191, 45192, 45193, 45194, 45195, 45196, 45197, 45198, 45199, 45200, 45201, 45202, 45203, 45204, 45206, 45207, 45208, 45209, 45210, 45211, 45212, 45213, 45214, 45215, 45216, 45217, 45218, 45219, 45220, 45221, 45222, 45223, 45224, 45225, 45226, 45227, 45228, 45229, 45230, 45231, 45232, 45233, 45234, 45235, 45236, 45237, 45238, 45239, 45240, 45241, 45242, 45243, 45244, 45245, 45246, 45247, 45248, 45249, 45250, 45251, 45252, 45253, 45254, 45255, 45256, 45257, 45258, 45259, 45260, 45261, 45262, 45263, 45264, 45265, 45266, 45267, 45268, 45269, 45270, 45271, 45272, 45273, 45274, 45275, 45276, 45277, 45278, 45279, 45280, 45281, 45282, 45283, 45284, 45285, 45286, 45287, 45288, 45289, 45290, 45291, 45292, 45293, 45294, 45295, 45296, 45297, 45298, 45299, 45300, 45301, 45302, 45303, 45304, 45305, 45306, 45307, 45308, 45309, 45310, 45311, 45312, 45313, 45314, 45315, 45316, 45317, 45318, 45319, 45320, 45321, 45322, 45323, 45324, 45325, 45326, 45327, 45328, 45329, 45330, 45331, 45332, 45333, 45334, 45335, 45336, 45337, 45338, 45339, 45340, 45341, 45342, 45343, 45344, 45345, 45346, 45347, 45348, 45349, 45350, 45351, 45352, 45353, 45354, 45355, 45356, 45357, 45358, 45359, 45360, 45361, 45362, 45363, 45364, 45365, 45366, 45367, 45368, 45369, 45370, 45371, 45372, 45373, 45374, 45375, 45376, 45377, 45378, 45379, 45380, 45381, 45382, 45383, 45384, 45385, 45386, 45387, 45388, 45389, 45390, 45391, 45392, 45393, 45394, 45395, 45396, 45397, 45398, 45399, 45400, 45401, 45402, 45403, 45404, 45405, 45406, 45407, 45408, 45409, 45410, 45411, 45412, 45413, 45414, 45415, 45416, 45417, 45418, 45419, 45420, 45421, 45422, 45423, 45424, 45425, 45426, 45427, 45428, 45429, 45430, 45431, 45432, 45433, 45434, 45435, 45436, 45437, 45438, 45439, 45440, 45441, 45442, 45443, 45444, 45445, 45446, 45447, 45448, 45449, 45450, 45451, 45452, 45453, 45454, 45455, 45456, 45457, 45458, 45459, 45460, 45461, 45462, 45463, 45464, 45465, 45466, 45467, 45468, 45469, 45470, 45471, 45472, 45473, 45474, 45475, 45476, 45477, 45478, 45479, 45480, 45481, 45482, 45483, 45484, 45485, 45486, 45487, 45488, 45489, 45490, 45491, 45492, 45493, 45494, 45495, 45496, 45497, 45498, 45499, 45500, 45501, 45502, 45503, 45504, 45505, 45506, 45507, 45508, 45509, 45510, 45511, 45512, 45513, 45514, 45515, 45516, 45517, 45518, 45519, 45520, 45521, 45522, 45523, 45524, 45525, 45526, 45527, 45528, 45529, 45530, 45531, 45532, 45533, 45534, 45535, 45536, 45537, 45538, 45539, 45540, 45541, 45542, 45543, 45544, 45545, 45546, 45547, 45548, 45549, 45550, 45551, 45552, 45553, 45554, 45555, 45556, 45557, 45558, 45559, 45560, 45561, 45562, 45563, 45564, 45565, 45566, 45567, 45568, 45569, 45570, 45571, 45572, 45573, 45574, 45575, 45576, 45577, 45578, 45579, 45580, 45581, 45582, 45583, 45584, 45585, 45586, 45587, 45588, 45589, 45590, 45591, 45592, 45593, 45594, 45595, 45596, 45597, 45598, 45599, 45600, 45601, 45602, 45603, 45604, 45605, 45606, 45607, 45608, 45609, 45610, 45611, 45612, 45613, 45614, 45615, 45616, 45617, 45618, 45619, 45620, 45621, 45622, 45623, 45624, 45625, 45626, 45627, 45628, 45629, 45630, 45631, 45632, 45633, 45634, 45635, 45636, 45637, 45638, 45639, 45640, 45641, 45642, 45643, 45644, 45645, 45646, 45647, 45648, 45649, 45650, 45651, 45652, 45653, 45654, 45655, 45656, 45657, 45658, 45659, 45660, 45661, 45662, 45663, 45664, 45665, 45666, 45667, 45668, 45669, 45670, 45671, 45672, 45673, 45674, 45675, 45676, 45677, 45678, 45679, 45680, 45681, 45682, 45683, 45684, 45685, 45686, 45687, 45688, 45689, 45690, 45691, 45692, 45693, 45694, 45695, 45696, 45697, 45698, 45699, 45700, 45701, 45702, 45703, 45704, 45705, 45706, 45707, 45708, 45709, 45710, 45711, 45712, 45713, 45714, 45715, 45716, 45717]

    if len(entry_ids) != len(excel_data):
        raise ValueError("Số lượng entry_ids và số lượng hàng trong additional_data phải bằng nhau.")

    # Sử dụng một vòng lặp để xử lý từng hàng với từng entry_id tương ứng
    for entry_id, (index, row) in zip(entry_ids, excel_data.iterrows()):
        # Lấy tất cả thông tin bệnh nhân
        all_info = get_all_info(entry_id)
        print("all_info:", all_info)
        if len(all_info) == 0:
            print("No information about patients.")
            return []

        for info in all_info:
            # Chuẩn bị thông tin bệnh nhân và lấy entryId
            information_data, information_data["entryId"] = prepare_information_data(row, info)

            # Cập nhật thông tin bệnh nhân
            result_api = update_information_patient(all_info, information_data)
            return result_api


def process_examination_services(test_data, testcase_id, entry_ids):
    from Tiếp_nhận.POST import process_generate_sum_patient_from_excel
    from Khám_bệnh_CDDV.GET import get_all_info, get_data_by_entry_id
    from Khám_bệnh_CDDV.PUT import prepare_information_data, update_information_patient
    test_data = test_data[test_data['TestCaseId'] == testcase_id]

    # Đọc dữ liệu gốc từ tệp Excel
    excel_data = test_data

    # Thông tin

    verify_data = test_data

    frVisitEntryIds = []
    all_datas = []

    # Sử dụng một vòng lặp để xử lý từng hàng với từng entry_id tương ứng
    for entry_id in entry_ids:
        # Lấy tất cả thông tin bệnh nhân
        all_info = get_all_info(entry_id)
        print("all_info:", all_info)
        if len(all_info) == 0:
            print("No information about patients.")
            continue

        # Lấy dòng dữ liệu của lần chạy đầu tiên
        first_row = excel_data.loc[excel_data.index[0], [
            'TestCaseId', 'DxSymptom', 'InitialDxICD', 'InitialDxText', 'DxICD',
            'DxText', 'DxByStaffId', 'TxInstruction', 'MedRcdNo', 'IcdCode',
            'ICDReason', 'TxVisitId', 'Type', 'Attribute1',
            'CreateByStaffName', 'PxItems', 'ServiceId', 'Code', 'TypeL1',
            'TypeL2', 'TypeL3', 'TypeL4', 'Category', 'Rank', 'Unit', 'Description',
            'InsServiceName', 'Attribute2', 'NationalCode', 'Status', 'InsPrice',
            'Price', 'PriceId', 'ServiceGroupName', 'LabExams', 'CreatedBy',
            'ContentHash', 'IsPassOnWarning', 'NonSubclinical', 'CreateById',
            'FeverOn', 'CreateOn1', 'OnDate1', 'Height', 'Weight', 'Systolic',
            'Diastolic', 'HeartRate', 'Temperature', 'SpO2', 'RespirationRate',
            'Notes', 'OnDate2', 'LabReqNotes', 'ServiceName', 'FullAddress',
            'ByProviderId', 'SpecimenTemplateCode', 'SubClinicUIType', 'PriceId.1', 'InsPriceRatio',
            'MedServiceTypeL3', 'SubClinicUIType', 'RefNo',
        ]]

        for info in all_info:
            verify_row = verify_data
            # Chuẩn bị thông tin bệnh nhân và lấy entryId
            information_data, information_data["entryId"] = prepare_information_data(first_row, info)

            # Cập nhật thông tin bệnh nhân
            update_information_patient(all_info, information_data)

            # Lấy dữ liệu theo entryId
            entry_data = get_data_by_entry_id(information_data["entryId"])

            # Bắt đầu chỉ định dịch vụ
            all_infoa = start_service_designation(entry_data)

            # Tạo chỉ định dịch vụ và lấy frVisitEntryId
            service_data = data_of_create_service_designation(first_row, all_infoa, all_info, excel_data)

            result = create_service_designation(service_data, verify_row)

            if result is None:  # Check if response_data is None, indicating failure
                response_data, frVisitEntryId, result = None, None, "Failed"
            else:
                response_data, frVisitEntryId, result = result

            # Thêm frVisitEntryId vào danh sách
            frVisitEntryIds.append(frVisitEntryId)
            all_datas.append(response_data)

            print("frVisitEntryIds = ", frVisitEntryIds)
            print("all_datas:", all_datas)

    return frVisitEntryIds, all_datas


# Chỉ định dịch vụ trong nội trú
def process_examination_services_NT(test_data, testcase_id, entry_ids, txVisitIds, wardAdmIds):
    from Khám_bệnh_CDDV.GET import get_all_info, get_data_by_entry_id
    test_data = test_data[test_data['TestCaseId'] == testcase_id]

    # Đọc dữ liệu gốc từ tệp Excel
    excel_data = test_data

    # Thông tin

    verify_data = test_data

    frVisitEntryIds = []
    all_datas = []

    # Sử dụng một vòng lặp để xử lý từng hàng với từng entry_id tương ứng
    for entry_id, txVisitId, wardAdmId in zip(entry_ids, txVisitIds, wardAdmIds):
        # Lấy tất cả thông tin bệnh nhân
        all_info = get_all_info(entry_id)
        print("all_info:", all_info)
        if len(all_info) == 0:
            print("No information about patients.")
            continue

        # Lấy dòng dữ liệu của lần chạy đầu tiên
        first_row = excel_data.loc[excel_data.index[0], [
            'TestCaseId', 'DxSymptom', 'InitialDxICD', 'InitialDxText', 'DxICD',
            'DxText', 'DxByStaffId', 'TxInstruction', 'MedRcdNo', 'IcdCode',
            'ICDReason', 'TxVisitId', 'Type', 'Attribute1',
            'CreateByStaffName', 'PxItems', 'ServiceId', 'Code', 'TypeL1',
            'TypeL2', 'TypeL3', 'TypeL4', 'Category', 'Rank', 'Unit', 'Description',
            'InsServiceName', 'Attribute2', 'NationalCode', 'Status', 'InsPrice',
            'Price', 'PriceId', 'ServiceGroupName', 'LabExams', 'CreatedBy',
            'ContentHash', 'IsPassOnWarning', 'NonSubclinical', 'CreateById',
            'FeverOn', 'CreateOn1', 'OnDate1', 'Height', 'Weight', 'Systolic',
            'Diastolic', 'HeartRate', 'Temperature', 'SpO2', 'RespirationRate',
            'Notes', 'OnDate2', 'LabReqNotes', 'ServiceName', 'FullAddress',
            'ByProviderId', 'SpecimenTemplateCode', 'SubClinicUIType', 'PriceId.1', 'InsPriceRatio',
            'MedServiceTypeL3', 'SubClinicUIType', 'RefNo',
        ]]

        for info in all_info:
            verify_row = verify_data

            # Lấy dữ liệu theo entryId
            entry_data = get_data_by_entry_id(info["entryId"])

            # Bắt đầu chỉ định dịch vụ
            all_infoa = start_service_designation(entry_data)

            # Tạo chỉ định dịch vụ và lấy frVisitEntryId
            service_data = data_of_create_service_designation_NT(first_row, all_infoa, all_info, excel_data, txVisitId, wardAdmId)

            result = create_service_designation(service_data, verify_row)

            if result is None:  # Check if response_data is None, indicating failure
                response_data, frVisitEntryId, result = None, None, "Failed"
            else:
                response_data, frVisitEntryId, result = result

            # Thêm frVisitEntryId vào danh sách
            frVisitEntryIds.append(frVisitEntryId)
            all_datas.append(response_data)

            print("frVisitEntryIds = ", frVisitEntryIds)
            print("all_datas:", all_datas)

    return frVisitEntryIds, all_datas
