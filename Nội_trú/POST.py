import pandas as pd
import random
import requests
from Cấu_hình.Setup import base_url_2, auth_token_2, base_url_4, auth_token_4, base_url, auth_token


# Lấy thông tin bệnh nhân đang ở màn hình danh sách chờ nhập kho
def get_info_patient_wait(visitIds):
    url = f"{base_url_2}/VisitWardAdmCerts/LoadByVisitIds"
    headers = {"Authorization": auth_token_2}
    data = visitIds
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    # if isinstance(response_data, list):
    #     for item in response_data:
    #         txVisitId = item.get("txVisitId", None)
    #         if txVisitId is not None:
    #             print("txVisitId:", txVisitId)
    # else:
    #     print("response_data is not a list")
    return response_data


# Tạo record trong nội trú
def create_Medrecord(data, visitIds):
    for visitId in visitIds:
        url = f"{base_url_4}/MedRecords/?visitId={visitId}"
        headers = {"Authorization": auth_token_4}
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        wardAdmId = response_data.get("wardAdmission", {}).get("wardAdmId")
    return wardAdmId, response_data


def data_of_Medrecord(row, visit_data, entry_data):
    from Tiếp_nhận.GET import CurrentServerDateTime
    # print(visit_json)
    # print(response_data)
    rcv_on = entry_data.get("createOn", None)
    create_on = CurrentServerDateTime()
    date_str = create_on.replace('"', '')
    IsCombineTreatment = True if str(row['IsCombineTreatment']).lower() == 'false' else False
    IsEmergecy = True if str(row['IsEmergecy']).lower() == 'false' else False
    Medrecord_data = {
        "Code": "",
        "Type": int(row["Type"]),
        "RcvType": int(row["RcvType"]),
        "RxTypeIn": int(row["RxTypeIn"]),
        "RcvWardId": int(row["RcvWardId"]),
        "RcvOn": rcv_on,
        "PatientId": visit_data["patientId"],
        "PtName": visit_data["ptName"],
        "PtDob": visit_data.get("ptDob", ""),
        "PtGender": visit_data.get("ptGender", ""),
        "PtAddress": visit_data.get("ptAddress", ""),
        "PtDistrict": visit_data.get("ptDistrict", ""),
        "PtWard": visit_data.get("ptWard", ""),
        "PtEthnic": visit_data.get("ptEthnic", ""),
        "PtNationality": visit_data.get("ptNationality", ""),
        "PtOccupation": visit_data.get("ptOccupation", ""),
        "InsCardNo": visit_data.get("insCardNo", ""),
        "InsBenefitType": visit_data.get("insBenefitType", ""),
        "InsBenefitRatio": visit_data.get("insBenefitRatio", ""),
        "VisitAttribute": int(row["VisitAttribute"]),
        "DxInByStaffId": entry_data.get("dxByStaffId", ""),
        "DxInText": entry_data.get("dxText", ""),
        "DxInICD": entry_data.get("dxICD", ""),
        "VisitId": visit_data.get("visitId", ""),
        "FileStoreNo": "",
        "MedRcdNo": "",
        "Notes": "",
        "CreateById": visit_data.get("createById", ""),
        "Status": int(row["Status"]),
        "PtCode": "24023987",
        "CreateByStaffName": str(row["CreateByStaffName"]),
        "WardAdmission": {
            "WardUnitId": int(row["WardUnitId"]),
            "BedId": int(row["BedId"]),
            "ReceiveOn": entry_data.get("createOn", ""),
            "DxByStaffId": entry_data.get("dxByStaffId", ""),
            "CreateById": visit_data.get("createById", ""),
            "CreateOn": date_str,
            "Status": entry_data.get("status", ""),
            "PtId": None,
            "OptRequestId": None,
            "OptId": None,
            "PtCode": None,
            "PtName": None,
            "PtGender": None,
            "PtDob": None,
            "FullAddress": None,
            "MobileNo": None,
            "InsCardNo": None,
            "InsBenefitType": None,
            "InsBenefitRatio": None,
            "CreateByStaffName": None,
            "DxInByStaffId": None,
            "DxInByStaffName": None,
            "TxVisitId": None,
            "IsSelect": int(row["IsSelect"]),
            "TxVisitList": None,
            "TxVisitMedList": None,
            "VoucherOuts": None,
            "Patient": None,
            "MEEmrImage": None,
            "EmrOrdId": None,
            "WardId": int(row["WardId"]),
            "Code": None,
            "MedRcdNo": None,
            "MedRecord": None,
            "BedName": None,
            "IsCombineTreatment": IsCombineTreatment,
            "TransferUnitId": None,
            "RcvOn": None,
            "BloodType": None,
            "BedCode": None,
            "IsEmergecy": IsEmergecy,
            "CareLevel": None
        },
        "TxVisitDXs": [],
        "TxDays": float(row["TxDays"]),
        "IsPaid": None,
        "InsBenefitTypeName": None
    }
    return Medrecord_data


# Tạo tờ điều trị
def create_TreatmentSheets(wardAdmId):
    txSheetIds = []
    url = f"{base_url_4}/TreatmentSheets/LoadByWardAdmId"
    headers = {"Authorization": auth_token_4}
    data = [wardAdmId]
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    if isinstance(response_data, list):
        for item in response_data:
            txSheetId = item.get("txSheetId", None)
            if txSheetId is not None:
                print("txVisitId:", txSheetId)
                txSheetIds.append(txSheetId)
    else:
        print("response_data is not a list")
    return txSheetIds, response_data


# Thông tin đợt điều trị
def get_info_TreatmentSheets(wardAdmId):
    url = f"{base_url_4}/WardAdmission/GetWardAdmByWardAdmId"
    headers = {"Authorization": auth_token_4}
    data = [wardAdmId]
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    return response_data


# Thông tin của wardadmission
def info_of_wardAdmission(medRcdIds):
    url = f"{base_url_4}/WardAdmission/MedRcdIds"
    headers = {"Authorization": auth_token_4}
    data = medRcdIds
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    return response_data


# Lưu đợt khám
def save_TxVisits(data):
    url = f"{base_url_4}/TxVisits"
    headers = {"Authorization": auth_token_4}
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    txVisitId = response_data.get("txVisitId", None)
    return txVisitId, response_data


def data_of_save_TxVisits(row, entry_data, wardAdmId, visit_data):
    from Tiếp_nhận.GET import CurrentServerDateTime
    IsCheckValidPrescription = False if str(row['IsCheckValidPrescription']).lower() == 'false' else True
    create_on = CurrentServerDateTime()
    date_str = create_on.replace('"', '')
    TxVisits_data = {
        "txSheetDetail": {
            "DzProgress": str(row["DzProgress"]),
            "DxICD": entry_data.get("dxICD", ""),
            "DxICDText": entry_data.get("dxText", ""),
            "TxVisits": None,
            "TxVisitMeds": None,
            "LabExams": None,
            "WardUnitId": None
        },
        "txVisit": {
            "Type": int(row["Type.1"]),
            "OnDate": date_str,
            "WardAdmId": wardAdmId,
            "Description": "",
            "Attribute": int(row["Attribute"]),
            "CreateById": visit_data.get("createById", ""),
            "CreateOn": date_str,
            "InsCardId": visit_data.get("insCardId", ""),
            "WardAdmRoomId": int(row["WardAdmRoomId"]),
            "CreateByStaffName": None
        },
        "IsCheckValidPrescription": IsCheckValidPrescription
    }

    return TxVisits_data


def save_LoadByWardAdmIdList(txSheetIds):
    url = f"{base_url_4}/TxVisits/LoadByWardAdmIdList"
    headers = {"Authorization": auth_token_4}
    data = txSheetIds
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    return response_data


def save_TreatmentSheetDetails(txSheetIds):
    url = f"{base_url_4}/TreatmentSheetDetails/LoadByTreatmentSheetId?isIncludeDetail=False"
    headers = {"Authorization": auth_token_4}
    data = txSheetIds
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    return response_data


# Tạo ExamFollowups
def create_ExamFollowups(medRcdIds):
    response_datas = []
    for medRcdId in medRcdIds:
        url = f"{base_url_4}/ExamFollowups"
        headers = {"Authorization": auth_token_4}
        data = {
            "MedRcdId": medRcdId
        }
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        response_datas.append(response_data)
    return response_datas


# Chạy nội trú
def process_NT(test_data, testcase_id, entry_ids):
    from Nội_trú.GET import load_Patient_wait, date_formatted, check_visit_enty, check_information_patient_initial, take_data_Medrecord, get_Medrecords
    test_data = test_data[test_data['TestCaseId'] == testcase_id]

    date_fomatted = date_formatted
    load_Patient_wait(date_fomatted)

    txVisitIds = []
    wardAdmIds = []
    medRcdIds = []
    Medrecords_jsons = []

    for entry_id in entry_ids:
        visitIds, response_data_1 = check_visit_enty(entry_id)
        visit_idas, visit_json_1 = check_information_patient_initial(visitIds)
        data = get_info_patient_wait(visitIds)
        Medrecord_data = data_of_Medrecord(test_data, visit_json_1, response_data_1)
        wardAdmId, response_data = create_Medrecord(Medrecord_data, visitIds)
        medRcdId, visit_json = take_data_Medrecord(visitIds)

        txSheetIds, response_data = create_TreatmentSheets(wardAdmId)
        get_info_TreatmentSheets(wardAdmId)
        info_of_wardAdmission(medRcdId)

        TxVisits_data = data_of_save_TxVisits(test_data, response_data_1, wardAdmId, visit_json_1)
        txVisitId, response_data = save_TxVisits(TxVisits_data)

        save_LoadByWardAdmIdList(txSheetIds)
        save_TreatmentSheetDetails(txSheetIds)

        Medrecords_json = get_Medrecords(medRcdId)

        medRcdIds.append(medRcdId)
        txVisitIds.append(txVisitId)
        wardAdmIds.append(wardAdmId)
        Medrecords_jsons.append(Medrecords_json)

    return txVisitIds, wardAdmIds, medRcdIds, Medrecords_jsons

