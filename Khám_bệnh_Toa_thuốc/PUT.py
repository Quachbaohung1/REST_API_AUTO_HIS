import requests
import pandas as pd


#Base url
base_url = "http://115.79.31.186:1096"
#Auth token
auth_token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IjM4MzkiLCJyb2xlIjoiQWRtaW4iLCJBY2NvdW50TmFtZSI6Imh1bmdxYiIsIkNsaWVudElwQWRkcmVzcyI6Ijo6MSIsIklzTG9jYWxJcCI6IlRydWUiLCJuYmYiOjE3MTUxODQ2NDIsImV4cCI6MTcxNTE4ODI0MiwiaWF0IjoxNzE1MTg0NjQyfQ.CihuC246iqFUos4MNZtNWs2q_SBOtmbXz4NRNuRQ4rg"


def clean_data(value):
    return str(value) if not pd.isna(value) else ''


def update_information_patient(all_info, data):
    headers = {"Authorization": auth_token}
    for info in all_info:
        entryId = info['entryId']
        url = f"{base_url}/pms/VisitEntries/{entryId}?forceNull=True&ptFullAddress=5%2F49+Ntl%2C+Ph%C6%B0%E1%BB%9Dng+07%2C+Qu%E1%BA%ADn+B%C3%ACnh+Th%E1%BA%A1nh%2C+Th%C3%A0nh+ph%E1%BB%91+H%E1%BB%93+Ch%C3%AD+Minh&isPassMedAIValid=&isPassMedAIValidOtherPx=False&isPassInteraction=False&isRemoveAllConsulation=True&isUpdateEntryValOnly=False&isBackupStatus=True"
        response = requests.put(url, json=data, headers=headers)
        response.raise_for_status()


def prepare_information_data(row, info):
    MedRcdNo = clean_data(row['MedRcdNo'])
    NationalCode = "0" + clean_data(row['NationalCode'])
    ServiceGroupName = clean_data(row['ServiceGroupName'])
    LabExams = clean_data(row['LabExams'])
    CreatedBy = clean_data(row['CreatedBy'])
    # Đọc giá trị từ file Excel
    isPassOnWarning_excel = str(row['IsPassOnWarning'])
    # Chuyển đổi giá trị từ chuỗi sang Boolean
    isPassOnWarning = True if isPassOnWarning_excel.lower() == 'true' else False
    information_data = {
        "entryId": info["entryId"],
        "visitId": info["visitId"],
        "medServiceId": info["medServiceId"],
        "wardUnitId": info["wardUnitId"],
        "onDate": info["createOn"],
        "dxSymptom": clean_data(row['DxSymptom']),
        "initialDxICD": clean_data(row['InitialDxICD']),
        "initialDxText": clean_data(row['InitialDxText']),
        "dxICD": clean_data(row['DxICD']),
        "dxText": clean_data(row['DxText']),
        "dxByStaffId": int(row['DxByStaffId']),
        "txInstruction": int(row['TxInstruction']),
        "createOn": info["createOn"],
        "createById": info["createById"],
        "status": info["status"],
        "insBenefitType": info['insBenefitType'],
        "insBenefitRatio": info["insBenefitRatio"],
        "priceId": info["priceId"],
        "qmsNo": info["qmsNo"],
        "ticketId": info["ticketId"],
        "medRcdNo": MedRcdNo,
        "createByWardUnitId": info["createByWardUnitId"],
        "visitDXList": [{"IcdCode": "A00", "ICDReason": "false"}, {"IcdCode": "A02.0", "ICDReason": "false"}],
        "txVisit": {"createOn": info["createOn"], "createByStaffName": row['CreateByStaffName']},
        "pxItems": [],
        "service": {
            "serviceId": int(row['ServiceId']),
            "code": clean_data(row['Code']),
            "typeL1": int(row['TypeL1']),
            "typeL2": int(row['TypeL2']),
            "typeL3": int(row['TypeL3']),
            "typeL4": int(row['TypeL4']),
            "category": int(row['Category']),
            "rank": int(row['Rank']),
            "unit": clean_data(row['Unit']),
            "description": clean_data(row['Description']),
            "insServiceName": clean_data(row['InsServiceName']),
            "attribute": int(row['Attribute2']),
            "nationalCode": NationalCode,
            "status": int(row['Status']),
            "insPrice": float(row['InsPrice']),
            "price": float(row['Price']),
            "priceId": int(row['PriceId']),
            "serviceGroupName": ServiceGroupName
        },
        "labExams": LabExams,
        "createdBy": CreatedBy,
        "contentHash": clean_data(row['ContentHash']),
        "isPassOnWarning": isPassOnWarning
    }
    return information_data, information_data["entryId"]


def update_information_patient_from_excel(row, is_first_run):
    from Khám_bệnh_Toa_thuốc.GET import get_to_update_initial
    # from Khám_bệnh_Toa_thuốc.POST import
    all_info = get_to_update_initial()
    print("all_info:", all_info)
    if len(all_info) == 0:
        print("No information about patients.")
        return
    for info in all_info:
        print("info:", info)  # Kiểm tra giá trị của info
        if not isinstance(info, dict):
            print(f"Unexpected info format: {info}")
            continue

        if is_first_run:
            information_data, entryId = prepare_information_data(row, info)
        else:
            MedRcdNo = clean_data(row['MedRcdNo'])
            NationalCode = "0" + clean_data(row['NationalCode'])
            ServiceGroupName = clean_data(row['ServiceGroupName'])
            LabExams = clean_data(row['LabExams'])
            CreatedBy = clean_data(row['CreatedBy'])
            # Đọc giá trị từ file Excel
            isPassOnWarning_excel = str(row['IsPassOnWarning'])
            # Chuyển đổi giá trị từ chuỗi sang Boolean
            isPassOnWarning = True if isPassOnWarning_excel.lower() == 'true' else False

            def handle_null(value, default=None, to_type=int):
                return to_type(value) if not pd.isna(value) else default

            IsInInsCat = False if str(row['IsInInsCat']).lower() == 'false' else True
            IsLocalPharmacy = False if str(row['IsLocalPharmacy']).lower() == 'false' else True
            IsPaid = False if str(row['IsPaid']).lower() == 'false' else True

            information_data = {
                "entryId": info["entryId"],
                "visitId": info["visitId"],
                "medServiceId": info["medServiceId"],
                "wardUnitId": info["wardUnitId"],
                "onDate": info["createOn"],
                "dxSymptom": clean_data(row['DxSymptom']),
                "initialDxICD": clean_data(row['InitialDxICD']),
                "initialDxText": clean_data(row['InitialDxText']),
                "dxICD": clean_data(row['DxICD']),
                "dxText": clean_data(row['DxText']),
                "dxByStaffId": int(row['DxByStaffId']),
                "txInstruction": int(row['TxInstruction']),
                "createOn": info["createOn"],
                "createById": info["createById"],
                "status": info["status"],
                "insBenefitType": info['insBenefitType'],
                "insBenefitRatio": info["insBenefitRatio"],
                "priceId": info["priceId"],
                "qmsNo": info["qmsNo"],
                "ticketId": info["ticketId"],
                "medRcdNo": MedRcdNo,
                "createByWardUnitId": info["createByWardUnitId"],
                "visitDXList": [{"IcdCode": "A00", "ICDReason": "false"}, {"IcdCode": "A02.0", "ICDReason": "false"}],
                "txVisit": {"createOn": info["createOn"], "createByStaffName": row['CreateByStaffName']},
                "PxItems": [
                    {
                        "ItemId": int(row['ItemIds']),
                        "ItemName": str(row['ItemName']),
                        "ItemUnit": str(row['ItemUnit']),
                        "Qty": float(row['Qty']),
                        "Notes": clean_data(row['Notes']),
                        "DoseNO": float(row['DoseNO']),
                        "DoseAN": float(row['DoseAN']),
                        "TxtDoseNO": str(row['TxtDoseNO']),
                        "TxtDoseAN": str(row['TxtDoseAN']),
                        "UseWeekDay": int(row['UseWeekDay']),
                        "UseDays": int(row['UseDays']),
                        "Attribute": int(row['Attribute']),
                        "IsPaid": IsPaid,
                        "StoreId": int(row['StoreIds']),
                        "InvSource": int(row['InvSource']),
                        "MedStrenght": str(row['MedStrenght']),
                        "MedUseRoute": str(row['MedUseRoute1']),
                        "MedItem": {
                            "ItemId": int(row['ItemIds']),
                            "InsIndex": clean_data(row['InsIndex']),
                            "Code": str(row['Code2']),
                            "Type": int(row['Type']),
                            "ItemCat": int(row['ItemCat']),
                            "ATC": clean_data(row['ATC']),
                            "Name": str(row['Name']),
                            "Description": clean_data(row['Description']),
                            "NtlCode": str(row['NtlCode']),
                            "NtlName": str(row['NtlName']),
                            "Unit": str(row['Unit']),
                            "PkgUnit": str(row['PkgUnit']),
                            "PkgUnitText": str(row['PkgUnitText']),
                            "UsageUnit": str(row['UsageUnit']),
                            "PPP": int(row['PPP']),
                            "PPU": int(row['PPU']),
                            "MedAI": str(row['MedAI']),
                            "MedUseRoute": int(row['MedUseRoute']),
                            "MedDosageForm": int(row['MedDosageForm']),
                            "MedStrenght": str(row['MedStrenght']),
                            "MedGbCode": clean_data(row['MedGbCode']),
                            "RegNo": str(row['RegNo']),
                            "MfrCode": int(row['MfrCode']),
                            "MfrName": str(row['MfrName']),
                            "MfrAddr": str(row['MfrAddr']),
                            "MfrCountry": str(row['MfrCountry']),
                            "InsCode": str(row['InsCode']),
                            "InsName": str(row['InsName']),
                            "InsPayRatio1": int(row['InsPayRatio1']),
                            "Price": row['Price'],
                            "Attribute": int(row['Attribute']),
                            "DrugWarnings": clean_data(row['DrugWarnings']),
                            "StockCritLevel": int(row['StockCritLevel']),
                            "Status": int(row['Status']),
                            "BidGroupCode": int(row['BidGroupCode']),
                            "BidPackageCode": int(row['BidPackageCode']),
                            "BidDocNo": str(row['BidDocNo']),
                            "SysFullName": str(row['SysFullName']),
                            "ProcessingMethodCode": clean_data(row['ProcessingMethodCode']),
                            "Note": clean_data(row['Note']),
                            "FullName": str(row['FullName']),
                            "IsInInsCat": IsInInsCat,
                            "Remaining": row['Remaining'],
                            "InsPrice": row['InsPrice'],
                            "AttributeDisplay": str(row['AttributeDisplay']),
                            "IsLocalPharmacy": IsLocalPharmacy,
                            "PlanCoefficient": float(row['PlanCoefficient']),
                            "PurchaseName": handle_null(row['PurchaseName'], default=None, to_type=int)
                        },
                        "Code": clean_data(row['Code']),
                        "InsBenefitType": handle_null(row['InsBenefitType'], default=None, to_type=int),
                        "OnVisit": handle_null(row['OnVisit'], default=None, to_type=int),
                        "WardAdmId": handle_null(row['WardAdmId'], default=None, to_type=int),
                        "TxVisitMedReturnId": handle_null(row['TxVisitMedReturnId'], default=None, to_type=int),
                        "ApproveQty": handle_null(row['ApproveQty'], default=None, to_type=int),
                        "Dosage": str(row['Dosage'])
                    }
                ],
                "service": {
                    "serviceId": int(row['ServiceId']),
                    "code": str(row['Code1']),
                    "typeL1": int(row['TypeL1']),
                    "typeL2": int(row['TypeL2']),
                    "typeL3": int(row['TypeL3']),
                    "typeL4": int(row['TypeL4']),
                    "category": int(row['Category']),
                    "rank": int(row['Rank']),
                    "unit": clean_data(row['Unit']),
                    "description": clean_data(row['Description']),
                    "insServiceName": clean_data(row['InsServiceName']),
                    "attribute": int(row['Attribute2']),
                    "nationalCode": NationalCode,
                    "status": int(row['Status']),
                    "insPrice": float(row['InsPrice']),
                    "price": float(row['Price']),
                    "priceId": int(row['PriceId']),
                    "serviceGroupName": ServiceGroupName
                },
                "labExams": LabExams,
                "createdBy": CreatedBy,
                "contentHash": clean_data(row['ContentHash']),
                "isPassOnWarning": isPassOnWarning
            }
        update_information_patient(all_info, information_data)