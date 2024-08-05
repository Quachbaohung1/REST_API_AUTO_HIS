import json

import requests
from Cấu_hình.Setup import base_url_2, auth_token_2, base_url_4, auth_token_4, base_url, auth_token


# Xuất viện
def discharged_hospital(data_his):
    url = f"{base_url_4}/MedRecords/UpdateMedRcdFieldsNull"
    headers = {"Authorization": auth_token_4, "Content-Type": "application/problem+json"}
    # Chuyển đổi dữ liệu thành JSON
    json_data = json.dumps(data_his)
    data = json_data
    response = requests.put(url, data=data, headers=headers)
    response.raise_for_status()


def data_of_discharged_hospital(Medrecords_jsons):
    from Tiếp_nhận.GET import CurrentServerDateTime
    import pandas as pd

    row = pd.Series({
        "FollowupOn": "2024-07-30T15:50:00+07:00",
        "TxMethod": "Test bệnh nhân xuất viện",
        "IsPaid": "false"
    })

    # Chuyển đổi Series thành dict
    row_dict = row.to_dict()

    IsPaid = False if str(row['IsPaid']).lower() == 'false' else True
    create_on = CurrentServerDateTime()
    date_str = create_on.replace('"', '')
    Discharged_hospital_data = []
    lstMedRcd_datas = []
    for Medrecords_json in Medrecords_jsons:
        lstMedRcd_data = {
            "MedRcdId": Medrecords_json.get("medRcdId", None),
            "Code": Medrecords_json.get("code", None),
            "Type": Medrecords_json.get("type", None),
            "RcvType": Medrecords_json.get("rcvType", None),
            "RxTypeIn": Medrecords_json.get("rxTypeIn", None),
            "RcvState": Medrecords_json.get("rcvState", None),
            "RcvWardId": Medrecords_json.get("rcvWardId", None),
            "RcvOn": Medrecords_json.get("rcvOn", None),
            "PatientId": Medrecords_json.get("patientId", None),
            "PtName": Medrecords_json.get("ptName", None),
            "PtDob": Medrecords_json.get("ptDob", None),
            "PtGender": Medrecords_json.get("ptGender", None),
            "PtAddress": Medrecords_json.get("ptAddress", None),
            "PtDistrict": Medrecords_json.get("ptDistrict", None),
            "PtWard": Medrecords_json.get("ptWard", None),
            "PtEthnic": Medrecords_json.get("ptEthnic", None),
            "PtNationality": Medrecords_json.get("ptNationality", None),
            "PtOccupation": Medrecords_json.get("ptOccupation", None),
            "InsCardNo": Medrecords_json.get("insCardNo", None),
            "InsBenefitType": Medrecords_json.get("insBenefitType", None),
            "InsBenefitRatio": Medrecords_json.get("insBenefitRatio", None),
            "VisitAttribute": Medrecords_json.get("visitAttribute", None),
            "DxInByStaffId": Medrecords_json.get("dxInByStaffId", None),
            "DxInText": Medrecords_json.get("dxInText", None),
            "DxInICD": Medrecords_json.get("dxInICD", None),
            "VisitId": Medrecords_json.get("visitId", None),
            "FileStoreNo": Medrecords_json.get("fileStoreNo", None),
            "EmrId": Medrecords_json.get("emrId", None),
            "EmrStatus": Medrecords_json.get("emrStatus", None),
            "MedRcdNo": Medrecords_json.get("medRcdNo", None),
            "Notes": Medrecords_json.get("notes", None),
            "CreateById": Medrecords_json.get("createById", None),
            "CreateOn": Medrecords_json.get("createOn", None),
            "Status": Medrecords_json.get("status", None),
            "FollowupOn": row_dict["FollowupOn"],
            "TxMethod": str(row_dict["TxMethod"]),
            "CreateByStaffName": None,
            "WardAdmission": None,
            "TxDays": 1.0,
            "IsPaid": IsPaid,
            "InsBenefitTypeName": None
        }
        lstMedRcd_datas.append(lstMedRcd_data)

        discharge_data = {
            "lstMedRcd": lstMedRcd_datas,
            "FieldsSetNull": [
                "FollowupOn",
                "TxMethod"
            ]
        }
        Discharged_hospital_data.append(discharge_data)

    return Discharged_hospital_data

