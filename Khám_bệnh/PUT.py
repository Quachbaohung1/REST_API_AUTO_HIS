import requests
import pandas as pd


#Base url
base_url = "http://115.79.31.186:1096"
#Auth token
auth_token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IjM4MzkiLCJyb2xlIjoiQWRtaW4iLCJBY2NvdW50TmFtZSI6Imh1bmdxYiIsIkNsaWVudElwQWRkcmVzcyI6Ijo6MSIsIklzTG9jYWxJcCI6IlRydWUiLCJuYmYiOjE3MTUxODQ2NDIsImV4cCI6MTcxNTE4ODI0MiwiaWF0IjoxNzE1MTg0NjQyfQ.CihuC246iqFUos4MNZtNWs2q_SBOtmbXz4NRNuRQ4rg"
def update_information_patient(all_info):
    for info in all_info:
        entryId = info["entryId"]
        url = f"{base_url}/pms/VisitEntries/{entryId}?forceNull=True&ptFullAddress=5%2F49+Ntl%2C+Ph%C6%B0%E1%BB%9Dng+07%2C+Qu%E1%BA%ADn+B%C3%ACnh+Th%E1%BA%A1nh%2C+Th%C3%A0nh+ph%E1%BB%91+H%E1%BB%93+Ch%C3%AD+Minh&isPassMedAIValid=&isPassMedAIValidOtherPx=False&isPassInteraction=False&isRemoveAllConsulation=True&isUpdateEntryValOnly=False&isBackupStatus=True"
        headers = {"Authorization": auth_token}
        response = requests.put(url, json=info, headers=headers)
        response.raise_for_status()

# Tạo thông tin ở tab Khám bệnh
def update_information_patient_from_excel(row):
    from Khám_bệnh.GET import get_to_update

    all_info = get_to_update()

    if len(all_info) == 0:
        print("No information about patients.")
        return

    for info in all_info:
        entryId = info.get("entryId")
        visitId = info.get("visitId")
        medServiceId = info.get("medServiceId")
        wardUnitId = info.get("wardUnitId")
        onDate = info.get("createOn")
        createOn = info.get("createOn")
        createById = info.get("createById")
        status = info.get("status")
        insBenefitType = info.get("insBenefitType")
        insBenefitRatio = info.get("insBenefitRatio")
        priceId = info.get("priceId")
        qmsNo = info.get("qmsNo")
        ticketId = info.get("ticketId")
        createByWardUnitId = info.get("createByWardUnitId")

        if pd.isna(row['MedRcdNo']):
            MedRcdNo = ''
        else:
            MedRcdNo = str(row['InsCheckedStatus'])

        NationalCode = "0" + str(row['NationalCode'])

        if pd.isna(row['ServiceGroupName']):
            ServiceGroupName = ''
        else:
            ServiceGroupName = str(row['ServiceGroupName'])

        if pd.isna(row['LabExams']):
            LabExams = ''
        else:
            LabExams = str(row['LabExams'])

        if pd.isna(row['CreatedBy']):
            CreatedBy = ''
        else:
            CreatedBy = str(row['CreatedBy'])

        information_data = {
            "EntryId": entryId,
            "VisitId": visitId,
            "MedServiceId": medServiceId,
            "WardUnitId": wardUnitId,
            "OnDate": onDate,
            "DxSymptom": str(row['DxSymptom']),
            "InitialDxICD": str(row['InitialDxICD']),
            "InitialDxText": str(row['InitialDxText']),
            "DxICD": str(row['DxICD']),
            "DxText": str(row['DxText']),
            "DxByStaffId": int(row['DxByStaffId']),
            "TxInstruction": int(row['TxInstruction']),
            "CreateOn": createOn,
            "CreateById": createById,
            "Status": status,
            "InsBenefitType": insBenefitType,
            "InsBenefitRatio": insBenefitRatio,
            "PriceId": priceId,
            "QmsNo": qmsNo,
            "TicketId": ticketId,
            "MedRcdNo": MedRcdNo,
            "CreateByWardUnitId": createByWardUnitId,
            "VisitDXList": [
                {
                    "IcdCode": "A00",
                    "ICDReason": "false"
                },
                {
                    "IcdCode": "A02.0",
                    "ICDReason": "false"
                }
            ],
            "TxVisit": {
                "TxVisitId": row['TxVisitId'],
                "Type": row['Type'],
                "OnDate": onDate,
                "Attribute": row['Attribute1'],
                "VisitEntryId": row['VisitEntryId'],
                "CreateById": createById,
                "CreateOn": createOn,
                "CreateByStaffName": row['CreateByStaffName']
            },
            "PxItems": [],
            "Service": {
                "ServiceId": int(row['ServiceId']),
                "Code": str(row['Code']),
                "TypeL1": int(row['TypeL1']),
                "TypeL2": int(row['TypeL2']),
                "TypeL3": int(row['TypeL3']),
                "TypeL4": int(row['TypeL4']),
                "Category": int(row['Category']),
                "Rank": int(row['Rank']),
                "Unit": str(row['Unit']),
                "Description": str(row['Description']),
                "InsServiceName": str(row['InsServiceName']),
                "Attribute": int(row['Attribute2']),
                "NationalCode": NationalCode,
                "Status": int(row['Status']),
                "InsPrice": float(row['InsPrice']),
                "Price": float(row['Price']),
                "PriceId": int(row['PriceId']),
                "ServiceGroupName": ServiceGroupName
            },
            "LabExams": LabExams,
            "CreatedBy": CreatedBy,
            "ContentHash": str(row['ContentHash']),
            "IsPassOnWarning": str(row['IsPassOnWarning'])
        }
        update_information_patient(information_data)

