import requests
import pandas as pd


#Base url
base_url = "http://115.79.31.186:1096"
#Auth token
auth_token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IjM4MzkiLCJyb2xlIjoiQWRtaW4iLCJBY2NvdW50TmFtZSI6Imh1bmdxYiIsIkNsaWVudElwQWRkcmVzcyI6Ijo6MSIsIklzTG9jYWxJcCI6IlRydWUiLCJuYmYiOjE3MTUxODQ2NDIsImV4cCI6MTcxNTE4ODI0MiwiaWF0IjoxNzE1MTg0NjQyfQ.CihuC246iqFUos4MNZtNWs2q_SBOtmbXz4NRNuRQ4rg"


def clean_data(value):
    return str(value) if not pd.isna(value) else ''


def update_information_patient(data):
    headers = {"Authorization": auth_token}
    url = f"{base_url}/cis/LabExams/?ptFullAddress=&isUpdateItem=False&isUpdateOnlyItem=False"
    response = requests.put(url, json=data, headers=headers)
    response.raise_for_status()


def prepare_information_data(row):
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
        "LabExId": 2359381,
        "Type": 1,
        "PatientId": 3277592,
        "RefNo": "RI.24.0009815",
        "OnDate": "2024-05-20T16:30:00",
        "LabReqById": 3839,
        "LabReqNotes": "",
        "DxICD": "A00.9",
        "DxText": "Bệnh tả, không đặc hiệu",
        "Attribute": 1,
        "FrVisitEntryId": 28052,
        "LabDxConclusion": "zxc",
        "LabDxConcludeById": 1291,
        "LabDoneById": 1234,
        "LabDxApproveById": 1291,
        "LabDxIssueOn": "2024-05-20T16:31:39.4639541+07:00",
        "CreateOn": "2024-05-20T16:30:00",
        "CreateById": 3839,
        "LabDxDescription": "kwQAAB+LCAAAAAAABAClVM1u1DAQPheJd7CClJ6Sze6y2m2SRoJd4EDFAfECjuNNhk3syPZSQtUn4EKFekIceuBeruRa7XvkTXD+2hSEoDRSJHtmPs/3zSfbD3lUBA8f7PlSFSlFqsjpoaHoezUiUhp1Zs8m8rnzZLyazmcndcbCKcTMfbuVCtaF14SARZQp18mVl2ERA6uXaPB7KTBqJRTiRLlje3banTyeHownk+n0hPCUC/eR03xeiMkmFnzLIqtNKIGZzLHQXbw1Z8pa4wzSwt1/AxmV6BU9Rq95htl+m5Xwgbrjx3lXfNz2ZVxkOO0qar19pGdzMHu2mE9WzlBnStfqH0X2xywW8+VkNXv6v6KWunMoYCjFuYsUf9SEGl9zRFIs5aFx46IR+Loru0n0JhiBdVSVn1mMWFyV3wlKMKDQpAQE8XS9ibvV1VlVngGyXyYmb0MxUkn141uBVFWeM73ZXe4udFRjMNkq6hFEtnovd5dV+VUXiOtj8wQyW1PWlAJ/lAd3pbz8pYWCDG0GxGIwsYI0oh6z0dWnlkCMNia0MJZoubgDKsEbSFV+AaQVXTA9AIgFftcU1roa+H0I/31qLNmirCvS89FJuO3Ffdq/MHk/r96NhJv4WuNt04eTJD0SRVX5kSR/YtFfo99Y9BfDCEwWytwb4kfdU/QTDSCn/JMEAAA=",
        "LabDxTechnique": "Chụp Xquang cột sống cổ chếch hai bên",
        "LabDxComment": "gdv",
        "LabDxOn": "2024-05-20T16:31:39.4639541+07:00",
        "LabDxApproveOn": "2024-05-20T16:31:39.5691112+07:00",
        "OrdGrpId": 2359381,
        "Status": 16,
        "IdToFiller": "2124053789",
        "WardUnitId": 149,
        "SysOrdGrpId": 2359381,
        "AbbrId": 1159,
        "DxInitial": "rtsu",
        "LabDxDescriptionHtml": "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\r\n<html xmlns=\"http://www.w3.org/1999/xhtml\">\r\n\t<head>\r\n\t\t<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" /><title>\r\n\t\t</title>\r\n\t\t<style type=\"text/css\">\r\n\t\t\t.csF0A1D375{text-align:justify;text-indent:0pt;margin:0pt 0pt 0pt 0pt;line-height:1.5}\r\n\t\t\t.cs13912233{color:#000000;background-color:transparent;font-family:'Times New Roman';font-size:14pt;font-weight:normal;font-style:normal;}\r\n\t\t\t.cs95E872D0{text-align:left;text-indent:0pt;margin:0pt 0pt 0pt 0pt}\r\n\t\t\t.cs887C2D5B{color:#000000;background-color:transparent;font-family:Calibri;font-size:10pt;font-weight:normal;font-style:normal;}\r\n\t\t</style>\r\n\t</head>\r\n\t<body>\r\n\t\t<p class=\"csF0A1D375\"><span class=\"cs13912233\">-Lồng ngực hai b&ecirc;n c&acirc;n đối .Kh&ocirc;ng thấy tổn thương c&aacute;c cung sườn tr&ecirc;n phim.</span></p><p class=\"csF0A1D375\"><span class=\"cs13912233\">-C&aacute;c cung tim kh&ocirc;ng gi&atilde;n. Đường k&iacute;nh ngang tim trong giới hạn b&igrave;nh thường.</span></p><p class=\"csF0A1D375\"><span class=\"cs13912233\">-Kh&ocirc;ng thấy tổn thương nhu m&ocirc; phổi hai b&ecirc;n.</span></p><p class=\"csF0A1D375\"><span class=\"cs13912233\">-G&oacute;c sườn ho&agrave;nh hai b&ecirc;n kh&ocirc;ng c&oacute; dịch.</span></p><p class=\"cs95E872D0\"><span class=\"cs887C2D5B\">&nbsp;</span></p></body>\r\n</html>\r\n",
        "Visit": {
            "VisitId": 993840,
            "VisitCode": "TN.2405.001114",
            "ReceiveType": 1,
            "RcvState": 1,
            "RxTypeIn": 1,
            "VisitOn": "2024-05-20T16:29:00",
            "PatientId": 3277592,
            "PtName": "Quách Bảo Hưng 487",
            "PtAge": 24,
            "PtGender": 1,
            "PtDob": "2000-01-01T00:00:00",
            "PtAddress": "5/49 Ntl",
            "PtDistrict": "765",
            "PtWard": "26926",
            "PtEthnic": "01",
            "PtNationality": "VN",
            "PtOccupation": 134,
            "InsCardId": 1018329,
            "InsCardNo": "DN4127389127785",
            "InsBenefitType": 2,
            "InsBenefitRatio": 80,
            "Attribute": 0,
            "FileStoreNo": "",
            "QmsNo": "78",
            "TicketId": 51723,
            "CreateOn": "2024-05-20T16:30:00",
            "CreateById": 3839,
            "Status": 1,
            "InsCheckedMessage": "Thẻ BHYT hợp lệ",
            "InsCheckedStatus": 1,
            "StmId": 10193,
            "Entry": {
                "EntryId": 28052,
                "VisitId": 993840,
                "MedServiceId": 4803,
                "WardUnitId": 149,
                "OnDate": "2024-05-20T16:30:00",
                "DxSymptom": "Bệnh tả, không đặc hiệu",
                "InitialDxICD": "A00.9",
                "InitialDxText": "Bệnh tả, không đặc hiệu",
                "DxICD": "A00.9",
                "DxText": "Bệnh tả, không đặc hiệu",
                "DxByStaffId": 3839,
                "TxInstruction": 3,
                "CreateOn": "2024-05-20T16:30:00",
                "CreateById": 3839,
                "Status": 8,
                "InsBenefitType": 2,
                "InsBenefitRatio": 80,
                "PriceId": 1083660,
                "QmsNo": "29",
                "TicketId": 51724,
                "MedRcdNo": "",
                "LastDxOn": "2024-05-20T16:29:00",
                "CreateByWardUnitId": 560,
                "Service": null,
                "LabExams": null,
                "CreatedBy": null,
                "ContentHash": "28052|993840|149|20/05/2024 16:30|A00.9|Bệnh tả, không đặc hiệu|3839|3|20/05/2024 16:30|3839||||PendingProcessing|4803|80||Bệnh tả, không đặc hiệu|2|1083660|29||",
                "IsPassOnWarning": false
            },
            "FullPatientCode": null,
            "InsBenefitTypeName": null,
            "WardUnitNames": null,
            "CreateByStaffName": null,
            "ContentHash": "993840|TN.2405.001114|1|Normal|CorrectRoute|20/05/2024 16:29|3277592|Quách Bảo Hưng 487|24|Male|01/01/2000 00:00|5/49 Ntl|765|26926|01|VN|134|1018329|DN4127389127785|2|80|None||||||78||20/05/2024 16:30|3839|Open|||||51723||||28052|993840|149|20/05/2024 16:30|A00.9|Bệnh tả, không đặc hiệu|3839|3|20/05/2024 16:30|3839||||PendingProcessing|4803|80||Bệnh tả, không đặc hiệu|2|1083660|29||",
            "LastUpdateByStaffName": null,
            "ModifiedOn": null
        },
        "ServiceName": "Chụp Xquang cột sống cổ chếch hai bên",
        "LabExamItems": [
            {
                "ExItemId": 3082259,
                "LabExId": 2359381,
                "MedServiceId": 392,
                "PriceId": 1083660,
                "InsBenefitType": 2,
                "InsBenefitRatio": 80,
                "InsCardId": 1018329,
                "Qty": 1.00,
                "Price": 37500.0,
                "InsPrice": 37500.0,
                "InsPriceRatio": 100,
                "Amt": 37500.0,
                "EqptCode": "XQ.1.75009.EEYO110",
                "Attribute": 8195,
                "ByProviderId": 552,
                "Status": 1,
                "DiscAmtSeq": 0,
                "MedServiceTypeL0": 2,
                "MedServiceTypeL2": 6,
                "MedServiceTypeL3": 25,
                "NonSubclinical": false,
                "TypeL0Code": null,
                "ByProviderCode": null,
                "ByProviderName": "Phòng X quang",
                "ServiceGroupName": "Chẩn đoán hình ảnh",
                "ServiceTypeL3Name": null,
                "ServiceCode": "xqm242",
                "ServiceName": "Chụp Xquang cột sống cổ chếch hai bên",
                "InsBenefitTypeName": null,
                "ReqDate": null,
                "AttrString": "Chờ thực hiện",
                "PaidAttrString": "Chờ thanh toán",
                "ServiceTypeOrderIndex": 0,
                "MedItemType": 1,
                "MedItem": null,
                "Checked": null,
                "OnDate": "2024-05-20T16:30:00",
                "TotalInvoiceAmtRound": null,
                "TotalReceiptAmtRound": null,
                "PtAmt": 0.0,
                "PtAmtRound": 0.0,
                "PtAmtPaid": 0.0,
                "PtCoPayAmt": 0.0,
                "PtCoPayAmtRound": 0.0,
                "InsAmt": 0.0,
                "InsAmtRound": 0.0,
                "DiscAmt": 0.0,
                "ReqBy": null
            }
        ],
        "ItemI0": {
            "ExItemId": 3082259,
            "LabExId": 2359381,
            "MedServiceId": 392,
            "PriceId": 1083660,
            "InsBenefitType": 2,
            "InsBenefitRatio": 80,
            "InsCardId": 1018329,
            "Qty": 1.00,
            "Price": 37500.0,
            "InsPrice": 37500.0,
            "InsPriceRatio": 100,
            "Amt": 37500.0,
            "EqptCode": "XQ.1.75009.EEYO110",
            "Attribute": 8195,
            "ByProviderId": 552,
            "Status": 1,
            "DiscAmtSeq": 0,
            "MedServiceTypeL0": 2,
            "MedServiceTypeL2": 6,
            "MedServiceTypeL3": 25,
            "NonSubclinical": false,
            "TypeL0Code": null,
            "ByProviderCode": null,
            "ByProviderName": "Phòng X quang",
            "ServiceGroupName": "Chẩn đoán hình ảnh",
            "ServiceTypeL3Name": null,
            "ServiceCode": "xqm242",
            "ServiceName": "Chụp Xquang cột sống cổ chếch hai bên",
            "InsBenefitTypeName": null,
            "ReqDate": null,
            "AttrString": "Chờ thực hiện",
            "PaidAttrString": "Chờ thanh toán",
            "ServiceTypeOrderIndex": 0,
            "MedItemType": 1,
            "MedItem": null,
            "Checked": null,
            "OnDate": "2024-05-20T16:30:00",
            "TotalInvoiceAmtRound": null,
            "TotalReceiptAmtRound": null,
            "PtAmt": 0.0,
            "PtAmtRound": 0.0,
            "PtAmtPaid": 0.0,
            "PtCoPayAmt": 0.0,
            "PtCoPayAmtRound": 0.0,
            "InsAmt": 0.0,
            "InsAmtRound": 0.0,
            "DiscAmt": 0.0,
            "ReqBy": null
        },
        "FullAddress": "5/49 Ntl, Phường 07, Quận Bình Thạnh, Thành phố Hồ Chí Minh"
    }
    return information_data, information_data["entryId"]


def update_information_patient_from_excel(row):
    from Khám_bệnh_CDDV.GET import get_to_update_initial, get_data_by_entry_id
    from Khám_bệnh_CDDV.POST import start_service_designation, data_of_create_service_designation
    all_info = get_to_update_initial()
    print("all_infoa:",all_info)
    if len(all_info) == 0:
        print("No information about patients.")
        return
    for info in all_info:
        information_data, entryId = prepare_information_data(row, info)
        update_information_patient(all_info)
        entry_data = get_data_by_entry_id(entryId)
        # Truyền entry_data vào hàm start_service_designation
        start_service_designation(entry_data)
        all_infoa = start_service_designation(entry_data)
        data_of_create_service_designation(row, all_infoa)
