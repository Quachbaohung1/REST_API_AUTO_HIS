import pandas as pd
import requests
from Cấu_hình.Setup import base_url, auth_token


# Tạo thông tin abc
def create_abc(visit_ids):
    url = f"{base_url}/cis/TxVisits/VisitIds"
    headers = {"Authorization": auth_token}
    data = visit_ids
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    if isinstance(response_data, list):
        for item in response_data:
            txVisitId = item.get("txVisitId", None)
            if txVisitId is not None:
                print("txVisitId:", txVisitId)
    else:
        print("response_data is not a list")
    return response_data, txVisitId


# Tạo thông tin bcd
def create_bcd(txVisitId):
    url = f"{base_url}/cis/Prescriptions/TxVisitIds"
    headers = {"Authorization": auth_token}
    data = [txVisitId]
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    if isinstance(response_data, list):
        for item in response_data:
            pxId = item.get("pxId", None)
            if pxId is not None:
                print("pxId:", pxId)
    else:
        print("response_data is not a list")
    return response_data, pxId


# Tạo thông tin cde
def create_cde(txVisitId):
    url = f"{base_url}/cis/TxVisitMeds/TxVisitIds"
    headers = {"Authorization": auth_token}
    data = [txVisitId]
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    StoreIds = []
    ItemIds = []
    Qtys = []

    if isinstance(response_data, list) and len(response_data) > 0:
        for item in response_data:
            store_id = item.get("storeId", None)
            item_id = item.get("itemId", None)
            qty_id = item.get("qty", None)
            if store_id is not None:
                StoreIds.append(store_id)
            if item_id is not None:
                ItemIds.append(item_id)
            if qty_id is not None:
                Qtys.append(qty_id)

    else:
        raise ValueError("Unexpected response format or empty list")
    return response_data, StoreIds, ItemIds, Qtys


# Kiểm tra tồn
def create_product(data):
    url = f"{base_url}/ims/InvNowInStores/?invNowStatus="
    headers = {"Authorization": auth_token}
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    return response_data


# Data của tạo phiếu xuất
def data_create_warehouse_return(StoreIds, LotIds):
    product_data = {
        "StoreIds": [StoreIds],
        "ItemIds": None,
        "LotIds": LotIds
    }
    return product_data


# Data của hoàn trả - kho
def data_create_product(StoreIds, ItemIds):
    product_data = {
        "StoreIds": [StoreIds],
        "ItemIds": ItemIds,
        "LotIds": None
    }
    return product_data

# Tạo phiếu xuất
def create_bills(data):
    url = f"{base_url}/ims/Vouchers/CreateVoucherOut/3?withBy=11"
    headers = {"Authorization": auth_token}
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    # Kiểm tra cấu trúc của response_data
    if "voucher" in response_data:
        voucherid = response_data["voucher"].get("voucherId")
        createOn = response_data["voucher"].get("createOn")
        createById = response_data["voucher"].get("createById")
    else:
        raise ValueError("Unexpected response format: 'voucher' key not found")

    if "voucherOuts" in response_data and isinstance(response_data["voucherOuts"], list) and len(
            response_data["voucherOuts"]) > 0:
        id = response_data["voucherOuts"][0].get("id")
    else:
        raise ValueError("Unexpected response format or empty 'voucherOuts' list")
    return response_data, voucherid, id, createOn, createById


# Tạo phiếu xuất thanh lý
def create_liquidation_bills(data):
    url = f"{base_url}/ims/Vouchers/CreateVoucherOut/3?withBy=0"
    headers = {"Authorization": auth_token}
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    # Kiểm tra cấu trúc của response_data
    if "voucher" in response_data:
        voucherid = response_data["voucher"].get("voucherId")
        createOn = response_data["voucher"].get("createOn")
        createById = response_data["voucher"].get("createById")
        StoreId = response_data["voucher"].get("storeId")
    else:
        raise ValueError("Unexpected response format: 'voucher' key not found")

    if "voucherOuts" in response_data and isinstance(response_data["voucherOuts"], list) and len(
            response_data["voucherOuts"]) > 0:
        id = response_data["voucherOuts"][0].get("id")
    else:
        raise ValueError("Unexpected response format or empty 'voucherOuts' list")

    lotIds = []

    # Extract 'lotId' from 'voucherOutInvs'
    voucherOutInvs = response_data.get("voucherOutInvs", [])
    for item in voucherOutInvs:
        lotId = item.get("lotId")
        if lotId is not None:
            lotIds.append(lotId)

    return response_data, voucherid, id, createOn, createById, lotIds, StoreId


# Tạo phiếu xuất hoàn trả kho
def create_warehouse_return_bills(data):
    url = f"{base_url}/ims/Vouchers/CreateVoucherOut/3?withBy=1"
    headers = {"Authorization": auth_token}
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    # Kiểm tra cấu trúc của response_data
    if "voucher" in response_data:
        voucherid = response_data["voucher"].get("voucherId")
        createOn = response_data["voucher"].get("createOn")
        createById = response_data["voucher"].get("createById")
        StoreId = response_data["voucher"].get("storeId")
    else:
        raise ValueError("Unexpected response format: 'voucher' key not found")

    if "voucherOuts" in response_data and isinstance(response_data["voucherOuts"], list) and len(
            response_data["voucherOuts"]) > 0:
        id = response_data["voucherOuts"][0].get("id")
    else:
        raise ValueError("Unexpected response format or empty 'voucherOuts' list")

    lotIds = []

    # Extract 'lotId' from 'voucherOutInvs'
    voucherOutInvs = response_data.get("voucherOutInvs", [])
    for item in voucherOutInvs:
        lotId = item.get("lotId")
        if lotId is not None:
            lotIds.append(lotId)

    return response_data, voucherid, id, createOn, createById, lotIds, StoreId


# Data của tạo phiếu xuất
def data_create_bills(row, StoreIds, ItemIds, visit_details, patientCode, pxId, Qtys, first_prices, invSources):
    # Xử lý các giá trị null
    def handle_null(value):
        return value if not pd.isna(value) else None

    for visit_detail in visit_details:
        voucherOuts_datas = []
        VoucherOutExts_datas = []

        for qty, first_price, invSource, ItemId in zip(Qtys, first_prices, invSources, ItemIds):
            Amt = int(qty) * int(first_price)

            # Create and append voucherOuts_data dictionary
            voucherOuts_data = {
                "PPU": int(row['PPU']),
                "SaleAmt": Amt,
                "Price": first_price,
                "ItemId": ItemId,
                "ItemSource": invSource,
                "Qty": qty,
                "Amt": Amt
            }
            voucherOuts_datas.append(voucherOuts_data)

            # Create and append VoucherOutExts_data dictionary
            VoucherOutExts_data = {
                "Dosage": row['Dosage'],
                "FrPxId": pxId
            }
            VoucherOutExts_datas.append(VoucherOutExts_data)

        bill_data = {
            "imsGetInvNowWithBy": handle_null(row['imsGetInvNowWithBy']),
            "Voucher": {
                "Type": int(row['Type']),
                "OnDate": visit_detail.get("createOn"),
                "Description": str(row['Description']),
                "StoreId": StoreIds,
                "TxVisitId": visit_detail.get("visitId"),
                "VisitEntryId": visit_detail.get("entryId"),
                "InvSource": int(row['InvSource']),
                "CreateById": visit_detail.get("createById"),
                "CreateOn": visit_detail.get("createOn"),
                "InvStatus": int(row['InvStatus']),
                "Attribute": int(row['Attribute']),
                "InvStatusDescription": handle_null(row['InvStatusDescription']),
                "ProcStatusDescription": handle_null(row['ProcStatusDescription']),
                "CustomerName": handle_null(row['CustomerName']),
                "InvoiceText": handle_null(row['InvoiceText'])
            },
            "voucherOuts": voucherOuts_datas,
            "voucherOutInvs": handle_null(row['voucherOutInvs']),
            "InvRequests": [],
            "VoucherExt": {
                "PatientId": visit_detail.get("patientId"),
                "PtNo": str(patientCode),
                "PtName": visit_detail.get("ptName"),
                "PtGender": visit_detail.get("ptGender"),
                "PtDob": visit_detail.get("ptDob"),
                "PtAddress": str(row['PtAddress']),
                "DxICD": visit_detail.get("dxICD"),
                "DxText": visit_detail.get("dxText"),
                "TxNote": visit_detail.get("txNotes"),
                "DoctorName": str(row['DoctorName'])
            },
            "VoucherOutExts": VoucherOutExts_datas,
            "RequestByInventory": handle_null(row['RequestByInventory'])
        }
        return bill_data


# Lấy voucherId cho phát thuốc BHYT
def get_voucherId_BHYT(visit_details):
    url = f"{base_url}/ims/Vouchers/FindWithEntryIds?storeId=28&types=60"
    headers = {"Authorization": auth_token}
    entry_ids = [visit["entryId"] for visit in visit_details]
    data = entry_ids
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    if isinstance(response_data, list) and len(response_data) > 0:
        voucherId = response_data[0].get("voucherId", None)
    else:
        raise ValueError("Unexpected response format or empty list")
    return response_data, voucherId


# Thực hiện tính tiền
def create_info_charge(voucherId):
    url = f"{base_url}/ims/VoucherOuts/VoucherIds"
    headers = {"Authorization": auth_token}
    data = [voucherId]
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    voucherout_ids = []
    itemIds = []
    if isinstance(response_data, list) and len(response_data) > 0:
        for item1 in response_data:
            voucherout_id = item1.get("id", None)
            itemId = item1.get("itemId", None)
            voucherout_ids.append(voucherout_id)
            itemIds.append(itemId)
    else:
        raise ValueError("Unexpected response format or empty list")

    recall_medicine_details = []
    if isinstance(response_data, list):
        for item in response_data:
            amt = item.get("amt", None)
            voucherId = item.get("voucherId", None)
            insPrice = item.get("insPrice", None)

            recall_medicine_details.append({
                "amt": amt,
                "voucherId": voucherId,
                "insPrice": insPrice
            })
    else:
        print("response_data is not a list")
    return response_data, voucherout_ids, itemIds, recall_medicine_details


def create_charge(voucherout_ids):
    url = f"{base_url}/ims/VoucherOutInvs/VouOutIds"
    headers = {"Authorization": auth_token}
    data = voucherout_ids
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    charge_details = []
    if isinstance(response_data, list):
        for item in response_data:
            id = item.get("id", None)
            vouInId = item.get("vouInId", None)
            price = item.get("price", None)
            insPrice = item.get("insPrice", None)
            lotId = item.get("lotId", None)
            qty = item.get("qty", None)
            amt = item.get("amt", None)

            charge_details.append({
                "id": id,
                "vouInId": vouInId,
                "price": price,
                "insPrice": insPrice,
                "lotId": lotId,
                "qty": qty,
                "amt": amt
            })
    else:
        print("response_data is not a list")
    return response_data, charge_details


def charge_success(data):
    url = f"{base_url}/finance/AdvancePayments/RetailPayment"
    headers = {"Authorization": auth_token}
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    return response_data


def data_of_charge_success(row, VoucherId, id, createOn, charge_details, createById):
    # Xử lý các giá trị null
    def handle_null(value):
        return value if not pd.isna(value) else None

    PaymentDatas = []
    total_amt = 0

    for charge_detail in charge_details:
        qty = charge_detail.get("qty", 0)
        price = charge_detail.get("price", 0)
        amt = qty * price
        total_amt += amt
        PaymentData = {
            "PaymentItemId": id,
            "ItemType": int(row["ItemType"]),
            "PayType": int(row["PayType"]),
            "InsBenefitType": int(row["InsBenefitType"]),
            "InsBenefitRatio": int(row["InsBenefitRatio"]),
            "Price": price,
            "InsPrice": charge_detail.get("insPrice"),
            "Qty": qty,
            "DiscAmt": float(row["DiscAmt"])
        }

        PaymentDatas.append(PaymentData)

    charge_data = {
        "Amt": total_amt,
        "CreateById": int(createById),
        "PaymentDate": createOn,
        "Status": int(row['Status']),
        "PaymentMethod": int(row['PaymentMethod']),
        "VoucherId": VoucherId,
        "RePaidForPmtId": handle_null(row['RePaidForPmtId']),
        "PaymentData": PaymentDatas,
        "Prefix": str(row['Prefix']),
        "LastDxOn": handle_null(row['LastDxOn']),
        "RealRevenue": total_amt
    }
    return charge_data


# Tạo phiếu thu hồi
def create_recall(data):
    url = f"{base_url}/ims/Vouchers/CreateVoucherInRevocation/3"
    headers = {"Authorization": auth_token}
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    return response_data


def data_of_create_recall(row, StoreIds, ItemIds, recall_details, charge_details):
    from Tiếp_nhận.GET import CurrentServerDateTime
    date = CurrentServerDateTime()
    if date:
        # Loại bỏ dấu ngoặc kép nếu có
        date = date.strip('"')
        # Loại bỏ phần múi giờ bằng cách tách chuỗi trước dấu "+"
        if '+' in date:
            date = date.split('+')[0]
        elif '-' in date:  # Nếu múi giờ có dấu trừ (cho các múi giờ âm)
            date = date.split('-')[0]
    else:
        date = None

    # Xử lý các giá trị null
    def handle_null(value):
        return value if not pd.isna(value) else None

    RevocationVoucherIns_datas = []

    for charge_detail, ItemId in zip(charge_details, ItemIds):
        RevocationVoucherIns_data = {
            "VouInvId": charge_detail.get("vouInId"),
            "Price": charge_detail.get("price"),
            "RefVouOutInvId": charge_detail.get("id"),
            "PriceCost": charge_detail.get("insPrice"),
            "LotId": charge_detail.get("lotId"),
            "ItemId": ItemId,
            "ItemSource": 32,
            "Qty": charge_detail.get("qty")
        }
        RevocationVoucherIns_datas.append(RevocationVoucherIns_data)

    for recall_detail, StoreId in zip(recall_details, StoreIds):
        create_recall_data = {
            "Voucher": {
                "Type": int(row["Type"]),
                "OnDate": date,
                "StoreId": StoreId,
                "TxVisitId": recall_detail.get("TxVisitId"),
                "VisitEntryId": recall_detail.get("TxVisitId"),
                "RefVoucherId": recall_detail.get("RefVoucherId"),
                "InvSource": recall_detail.get("InvSource"),
                "CreateById": recall_detail.get("createById"),
                "CreateOn": date,
                "InvStatus": recall_detail.get("InvSource"),
                "InvStatusDescription": handle_null(row["InvStatusDescription"]),
                "ProcStatusDescription": handle_null(row["ProcStatusDescription"]),
                "CustomerName": handle_null(row["CustomerName"]),
                "InvoiceText": handle_null(row["InvoiceText"])
            },
            "VoucherIns": [],
            "ItemLots": [],
            "ItemPrices": [],
            "RevocationVoucherIns": RevocationVoucherIns_datas
        }
    return create_recall_data


# Check thuốc trong kho
def data_of_InvNowInStores(response_data):
    for data in response_data:
        InvNowInStores_data = [
            {
                "StoreId": data.get("storeId"),
                "ItemId": data.get("itemId"),
                "Qty": data.get("qty"),
                "QtyInvNow": None,
                "Amt": data.get("amt"),
                "InvSource": data.get("invSource"),
                "IsReqToStoreIns": True,
                "Status": data.get("status"),
                "InvOuts": None,
                "Price": data.get("price"),
                "InsPrice": data.get("insPrice"),
                "TxVisitMedId": None
            }
        ]
        return InvNowInStores_data


# Lấy thông tin thuốc đã kê ở khám bệnh
def check_info_medicine(visit_details):
    url = f"{base_url}/cis/TxVisitMeds/Entries"
    headers = {"Authorization": auth_token}
    for visit_detail in visit_details:
        data = [
            visit_detail["entryId"]
        ]
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    itemIds = []
    if isinstance(response_data, list):
        for item in response_data:
            itemId = item.get("itemId", None)
            storeId = item.get("storeId", None)

            itemIds.append({
                "itemId": itemId,
                "storeId": storeId
            })
    else:
        print("response_data is not a list")
    return response_data, itemIds


def InvNowInStores(data):
    url = f"{base_url}/ims/InvNowInStores/VerifyInStore?ImsGetInvCheckBy=11"
    headers = {"Authorization": auth_token}
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    return response_data


# Lấy thông tin tạo phiếu xuất
def VoucherExts(voucherId):
    url = f"{base_url}/ims/VoucherExts/VoucherIds"
    headers = {"Authorization": auth_token}
    data = [voucherId]
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    return response_data


def VoucherOutExts(voucherout_ids):
    url = f"{base_url}/ims/VoucherOutExts/VouOutIds"
    headers = {"Authorization": auth_token}
    data = voucherout_ids
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    return response_data


def LoadByVoucherIds(voucherId):
    url = f"{base_url}/finance/AdvancePayments/LoadByVoucherIds"
    headers = {"Authorization": auth_token}
    data = [voucherId]
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    Voucher_data = response.json()
    return Voucher_data


# Booking
def booking(data):
    url = f"{base_url}/ims/Statements/add?isBooking=True"
    headers = {"Authorization": auth_token}
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    Voucher_data = response.json()
    stmId = Voucher_data.get("stmId")
    return Voucher_data, stmId


def data_of_booking(row, StoreIds, item_ids, InvSources, RqtQtys, Notes):
    from Tiếp_nhận.GET import CurrentServerDateTime

    def handle_null(value):
        return value if not pd.isna(value) else None

    StmDetail_datas = []

    for item_id, InvSource, RqtQty, Note in zip(item_ids, InvSources, RqtQtys, Notes):
        StmDetail_data = {
            "ItemId": item_id,
            "InvSource": InvSource,
            "RqtQty": RqtQty,
            "Note": Note
        }
        StmDetail_datas.append(StmDetail_data)
        print("StmDetail_datas: ", StmDetail_datas)

    date = CurrentServerDateTime()
    date_strip = date.strip('"')

    booking_data = {
        "Statement": {
            "StmNo": row["StmNo"],
            "Type": int(row["Type.1"]),
            "OnDate": date_strip,
            "Description": handle_null(row["Description"]),
            "StoreId": int(row["StoreId"]),
            "RefStoreId": StoreIds[0],
            "Status": int(row["Status"]),
            "CreateById": int(row["CreateById"]),
            "CreateOn": date_strip
        },
        "StmDetail": StmDetail_datas
    }
    print("booking_data: ", booking_data)
    return booking_data


def StatementDetails(stmId):
    url = f"{base_url}/ims/StatementDetails/stmIds"
    headers = {"Authorization": auth_token}
    data = [stmId]
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    Info_data = response.json()
    return Info_data


# Tìm phiếu để xác nhận nhập kho
def look_for_ticket():
    url = f"{base_url}/ims/Vouchers/list/?storeIds=28&refStoreIds=&providerId=&voucherNo=&status=0&invSource=&BidDocNo=&frmDate=20240701&toDate=20240705&process=&types=20%2C1&attribute="
    headers = {
        "Authorization": auth_token,
        "Content-Type": "application/json"
    }

    # Define the payload as an empty list
    data = []

    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    Info_data = response.json()

    stmIds = []
    voucherIds = []
    if isinstance(Info_data, list):
        for item in Info_data:
            stmId = item.get("stmId", None)

            stmIds.append({
                stmId,
            })
    else:
        print("response_data is not a list")

    if isinstance(Info_data, list):
        for item in Info_data:
            voucherId = item.get("voucherId", None)

            voucherIds.append({
                voucherId,
            })
    else:
        print("response_data is not a list")

    return Info_data, stmId, voucherId


def VoucherIns(voucherId):
    url = f"{base_url}/ims/VoucherIns/VoucherIds?itemId="
    headers = {
        "Authorization": auth_token,
        "Content-Type": "application/json"
    }

    # Send the voucherId as a list
    data = [voucherId]

    # Use the json parameter to send the data
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()

    Info_data = response.json()
    lotIds = []
    itemIds = []

    if isinstance(Info_data, list):
        for item in Info_data:
            lotId = item.get("lotId", None)
            lotIds.append(lotId)

            itemId = item.get("itemId", None)
            itemIds.append(itemId)
    else:
        print("Info_data is not a list")

    return Info_data, lotIds, itemIds


def ItemLots(lotIds):
    url = f"{base_url}/ims/ItemLots/LotIds"
    headers = {
        "Authorization": auth_token,
        "Content-Type": "application/json"
    }
    data = lotIds
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    Info_data = response.json()
    return Info_data


def Items(itemIds):
    url = f"{base_url}/ims/Items/ids"
    headers = {
        "Authorization": auth_token,
        "Content-Type": "application/json"
    }
    data = itemIds
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    Info_data = response.json()
    return Info_data


def data_create_delivery_bill(info_delivery_bills):
    from Tiếp_nhận.GET import CurrentServerDateTime

    date = CurrentServerDateTime()
    date_obj = date.strip('"')

    # Xử lý các giá trị null
    def handle_null(value):
        return value if not pd.isna(value) else None

    voucherOuts_datas = []

    for row in info_delivery_bills:

        # Create and append voucherOuts_data dictionary
        voucherOuts_data = {
            "PPU": int(row['PPU']),
            "VatPerc": int(row['VatPerc']),
            "LotId": int(row['LotId']),
            "ItemId": int(row['ItemId']),
            "ItemSource": int(row['ItemSource']),
            "Qty": int(row['Qty']),
            "Status": int(row['Status'])
        }
        voucherOuts_datas.append(voucherOuts_data)

    bill_data = {
        "imsGetInvNowWithBy": handle_null(row['imsGetInvNowWithBy']),
        "Voucher": {
            "Type": int(row['Type']),
            "RefStoreId": handle_null(row['RefStoreId']),
            "OnDate": date_obj,
            "Description": str(row['Description']),
            "StoreId": int(row['StoreId']),
            "TxVisitId": handle_null(row['TxVisitId']),
            "VisitEntryId": handle_null(row['VisitEntryId']),
            "InvSource": int(row['InvSource']),
            "CreateById": int(row['CreateById']),
            "CreateOn": date_obj,
            "InvStatus": int(row['InvStatus']),
            "Attribute": handle_null(row['Attribute']),
            "InvStatusDescription": handle_null(row['InvStatusDescription']),
            "ProcStatusDescription": handle_null(row['ProcStatusDescription']),
            "CustomerName": handle_null(row['CustomerName']),
            "InvoiceText": handle_null(row['InvoiceText'])
        },
        "voucherOuts": voucherOuts_datas,
        "voucherOutInvs": None,
        "InvRequests": [],
        "VoucherExt": None,
        "voucherIns": None,
        "VoucherOutExts": None,
        "RequestByInventory": handle_null(row['RequestByInventory'])
    }
    return bill_data


# Xuất chuyển kho
def CreateAndSaveVoucherIn(data):
    url = f"{base_url}/ims/Vouchers/CreateAndSaveVoucherIn"
    headers = {
        "Authorization": auth_token,
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    Info_data = response.json()
    return Info_data


def data_CreateAndSaveVoucherIn(row, info_delivery_bills, voucherid, recall_medicine_details, charge_details):
    from Tiếp_nhận.GET import CurrentServerDateTime

    date = CurrentServerDateTime()
    date_obj = date.strip('"')

    def handle_null(value):
        return value if not pd.isna(value) else None

    VoucherIns_datas = []

    # Create and append voucherOuts_data dictionary
    for recall_medicine_detail, charge_detail, info_delivery_bill in zip(recall_medicine_details, charge_details, info_delivery_bills):
        Amt = int(recall_medicine_detail.get("insPrice")) * int(info_delivery_bill['Qty'])
        VoucherIns_data = {
            "Price": recall_medicine_detail.get("insPrice"),
            "VatPerc": int(info_delivery_bill['VatPerc']),
            "VatAmt": Amt,
            "RefVouOutInvId": charge_detail.get("id"),
            "LotId": int(info_delivery_bill['LotId']),
            "ItemId": int(info_delivery_bill['ItemId']),
            "ItemSource": int(info_delivery_bill['ItemSource']),
            "Qty": int(info_delivery_bill['Qty']),
            "Amt": Amt,
            "Status": int(info_delivery_bill['Status'])
        }
        VoucherIns_datas.append(VoucherIns_data)

    VoucherIn_data = {
        "Voucher": {
            "Type": int(info_delivery_bill['Type.1']),
            "OnDate": date_obj,
            "Description": str(info_delivery_bill['Description']),
            "StoreId": int(info_delivery_bill['RefStoreId']),
            "TxVisitId": handle_null(info_delivery_bill['TxVisitId']),
            "VisitEntryId": handle_null(info_delivery_bill['VisitEntryId']),
            "RefVoucherId": voucherid,
            "RefStoreId": int(info_delivery_bill['StoreId']),
            "InvSource": int(info_delivery_bill['InvSource']),
            "CreateById": int(info_delivery_bill['CreateById']),
            "CreateOn": date_obj,
            "InvStatus": int(info_delivery_bill['InvStatus']),
            "InvStatusDescription": handle_null(info_delivery_bill['InvStatusDescription']),
            "ProcStatusDescription": handle_null(info_delivery_bill['ProcStatusDescription']),
            "CustomerName": handle_null(info_delivery_bill['CustomerName']),
            "InvoiceText": handle_null(info_delivery_bill['InvoiceText'])
        },
        "VoucherIns": VoucherIns_datas,
        "ItemLots": [],
        "ItemPrices": [],
        "RevocationVoucherIns": handle_null(row['RevocationVoucherIns'])
    }
    return VoucherIn_data


# Case xuôi
def process_store(test_data, testcase_id):
    from Dược.GET import get_info_patient, get_info_visit, get_store
    from Dược.PUT import data_of_update_status, update_status

    patientCodes = [24013719]

    test_data = test_data.loc[test_data['TestCaseId'] == testcase_id]

    # Đọc dữ liệu gốc từ tệp Excel
    excel_data = test_data

    # Sử dụng một vòng lặp để xử lý từng hàng với từng entry_id tương ứng
    for patientCode, (index, row) in zip(patientCodes, excel_data.iterrows()):

        response_data, patient_id = get_info_patient(patientCode)

        response_data, visit_ids, visit_details = get_info_visit(patient_id)

        response_data, itemIds = check_info_medicine(visit_details)

        # Lọc StoreId và ItemId tương ứng với StoreId = 36
        filtered_itemIds = []

        # Tạo hai danh sách riêng biệt cho itemId và storeId
        item_ids_list = [item["itemId"] for item in itemIds]
        store_ids_list = [item["storeId"] for item in itemIds]

        for itemId, storeId in zip(item_ids_list, store_ids_list):
            if storeId == 36:
                filtered_itemIds.append(int(itemId))

        response_data, first_prices, invSources = get_store(filtered_itemIds)

        response_data, txVisitId = create_abc(visit_ids)

        response_data, pxId = create_bcd(txVisitId)

        response_data, StoreIds, ItemIds, Qtys = create_cde(txVisitId)

        # Lọc StoreId và ItemId tương ứng với StoreId = 36
        filtered_store_ids = []
        filtered_item_ids = []
        filtered_qty_ids = []

        for store_id, item_id, qty_id in zip(StoreIds, ItemIds, Qtys):
            if store_id == 36:
                filtered_store_ids.append(int(store_id))
                filtered_item_ids.append(int(item_id))
                filtered_qty_ids.append(int(qty_id))

        # Kiểm tra và truyền giá trị vào hàm data_create_product nếu có StoreId = 36
        if filtered_store_ids:
            product_data = data_create_product(filtered_store_ids, filtered_item_ids)
        else:
            product_data = None  # Hoặc hành động khác nếu không tìm thấy StoreId = 36

        create_product(product_data)

        # for filtered_store_id, filtered_item_id, filtered_qty_id in zip(filtered_store_ids, filtered_item_ids, filtered_qty_ids):
        bill_data = data_create_bills(row, filtered_store_ids[0], filtered_item_ids, visit_details, patientCode, pxId,
                                      filtered_qty_ids, first_prices, invSources)

        response_data, voucherid, id, createOn, createById = create_bills(bill_data)

        response_data, voucherout_id, itemId, recall_medicine_details = create_info_charge(voucherid)

        response_data, charge_details = create_charge(voucherout_id)

        charge_data = data_of_charge_success(row, voucherid, id, createOn, charge_details, createById)

        response_data = charge_success(charge_data)

        status_data = data_of_update_status(voucherid)

        result_api = update_status(status_data, voucherid)

        return result_api


def process_store_BHYT(test_data, testcase_id): #(Đang chuyển đổi port nên chưa chạy được phát thuốc BHYT trên môi trường Stagging WAN)
    from Dược.GET import get_info_patient, get_info_visit, get_store
    from Dược.PUT import data_of_update_status, update_status
    from Viện_phí.POST import create_info_payment, create_advancePayments, create_service, create_service_designation, data_of_create_service_designation, create_bill
    from Viện_phí.GET import get_info_patient1, check_txInstruction, get_info_status, get_info_service
    from Viện_phí.PUT import closing_costs

    file_path_a = "D://HIS api automation/DataTest/Viện_phí/TC_01.xlsx"

    patientCodes = 24013719

    patientCodes_1 = [24013719]

    sheet_name = "Data"
    sheet_name_a = "Data"

    # Đọc dữ liệu gốc từ tệp Excel
    test_data = test_data.loc[test_data['TestCaseId'] == testcase_id]

    # Đọc dữ liệu gốc từ tệp Excel
    excel_data = test_data
    excel_data_a = pd.read_excel(file_path_a, sheet_name=sheet_name_a)

    # Thực hiện tính tiền trước rồi mới phát thuốc
    visitId = get_info_patient1(patientCodes)
    closing_costs(visitId)
    print("Được thực hiện thanh toán")
    create_advancePayments(visitId)
    response_data, txVisitId = create_abc(visitId)
    response_data_1, StoreIds, ItemIds, Qtys = create_cde(txVisitId)
    InvNowInStores_data = data_of_InvNowInStores(response_data_1)
    InvNowInStores(InvNowInStores_data)

    all_info = create_service(visitId)
    infos = get_info_status(visitId)
    for index_a, row_a in excel_data_a.iterrows():
        service_data = data_of_create_service_designation(row_a, all_info, infos)
    response_data, payment_ids = create_service_designation(service_data)
    get_info_service(visitId)
    create_advancePayments(visitId)
    response_data = create_bill(visitId)

    # Sử dụng một vòng lặp để xử lý từng hàng với từng entry_id tương ứng
    for patientCode, (index, row) in zip(patientCodes_1, excel_data.iterrows()):

        response_data, patient_id = get_info_patient(patientCode)

        response_data, visit_ids, visit_details = get_info_visit(patient_id)

        response_data = get_store()

        response_data, txVisitId = create_abc(visit_ids)

        response_data, pxId = create_bcd(txVisitId)

        response_data, StoreIds, ItemIds, Qtys = create_cde(txVisitId)

        # product_data = data_create_product(StoreIds, ItemIds)

        # create_product(product_data)

        response_data, voucherid = get_voucherId_BHYT(visit_details)

        response_data, voucherout_id, itemId, recall_medicine_details = create_info_charge(voucherid)

        create_charge(voucherout_id)

        # charge_data = data_of_charge_success(row, voucherid, id, createOn)
        #
        # response_data = charge_success(charge_data)

        status_data = data_of_update_status(voucherid)

        result_api = update_status(status_data, voucherid)

        return result_api


# Case ngược
def process_recall_store(test_data, testcase_id):
    from Dược.GET import choose_recall
    from Dược.PUT import data_of_recall_medicine, recall_medicine, data_of_update_status_recall, update_status_recall

    voucherNo = ["NT.RSL.24.07.0067"]

    test_data = test_data.loc[test_data['TestCaseId'] == testcase_id]

    # Đọc dữ liệu gốc từ tệp Excel
    excel_data = test_data

    # Sử dụng một vòng lặp để xử lý từng hàng với từng entry_id tương ứng
    for voucherNo, (index, row) in zip(voucherNo, excel_data.iterrows()):
        response_data, voucherIds, recall_details, StoreIds = choose_recall(voucherNo)

        for voucherId in voucherIds:
            VoucherExts(voucherId)
            response_data, voucherout_ids, itemIds, recall_medicine_details = create_info_charge(voucherId)

        response_data = VoucherOutExts(voucherout_ids)

        response_data, charge_details = create_charge(voucherout_ids)

        Voucher_data = LoadByVoucherIds(voucherId)

        recall_data = data_of_recall_medicine(row, Voucher_data)

        recall_medicine(recall_data)

        create_recall_data = data_of_create_recall(row, StoreIds, itemIds, recall_details, charge_details)

        response_data = create_recall(create_recall_data)

        status_recall_data = data_of_update_status_recall(Voucher_data)

        result_api = update_status_recall(status_recall_data, voucherId)

        return result_api


# Đề nghị thuốc của kho lẻ đến kho chẵn
def recommend_medication(test_data, testcase_id):
    from Dược.GET import choose_medicine_to_recommend
    from Dược.PUT import update_Statements

    test_data = test_data.loc[test_data['TestCaseId'] == testcase_id]

    # Đọc dữ liệu gốc từ tệp Excel
    excel_data = test_data

    item_ids = []
    InvSources = []
    RqtQtys = []
    Notes = []

    for index, row in excel_data.iterrows():
        item_ids.append(int(row['itemId']))
        InvSources.append(int(row['InvSource.1']))
        RqtQtys.append(int(row['RqtQty']))
        Notes.append(str(row['Note']))

    response_data, StoreIds = choose_medicine_to_recommend(item_ids)

    product_data = data_create_product(StoreIds, item_ids)

    create_product(product_data)

    booking_data = data_of_booking(row, StoreIds, item_ids, InvSources, RqtQtys, Notes)

    Voucher_data, stmId = booking(booking_data)

    Info_data = StatementDetails(stmId)

    result_api = update_Statements(stmId)

    return result_api


# Xác nhận nhập kho
def confirm_warehouse(test_data, testcase_id):
    from Dược.GET import Vouchers
    from Dược.PUT import update_confirmed_warehouse, data_of_update_confirmed_warehouse

    test_data = test_data.loc[test_data['TestCaseId'] == testcase_id]

    # Đọc dữ liệu gốc từ tệp Excel
    excel_data = test_data

    Info_data, stmId, voucherId = look_for_ticket()

    StatementDetails(stmId)

    Info_data, lotIds, itemIds = VoucherIns(voucherId)

    ItemLots(lotIds)

    Items(itemIds)

    response_data = Vouchers(voucherId)

    confirmed_warehouse_data = data_of_update_confirmed_warehouse(response_data)

    result_api = update_confirmed_warehouse(confirmed_warehouse_data)

    return result_api


# Chuyển kho
def transfer_warehouse(test_data, testcase_id):

    test_data = test_data.loc[test_data['TestCaseId'] == testcase_id]

    # Đọc dữ liệu gốc từ tệp Excel
    excel_data = test_data

    info_delivery_bills = []

    for index, row in excel_data.iterrows():
        info_delivery_bill = {
            "PPU": int(row['PPU']),
            "VatPerc": int(row['VatPerc']),
            "LotId": int(row['LotId']),
            "ItemId": int(row['itemId']),
            "ItemSource": int(row['ItemSource']),
            "Qty": int(row['Qty']),
            "Status": int(row['Status']),
            "imsGetInvNowWithBy": row['imsGetInvNowWithBy'],
            "Type": int(row['Type']),
            "Type.1": int(row['Type.1']),
            "RefStoreId": int(row['RefStoreId']),
            "Description": str(row['Description']),
            "StoreId": int(row['StoreId']),
            "InvSource": int(row['InvSource']),
            "CreateById": int(row['CreateById']),
            "InvStatus": int(row['InvStatus']),
            "Attribute": row['Attribute'],
            "InvStatusDescription": row['InvStatusDescription'],
            "ProcStatusDescription": row['ProcStatusDescription'],
            "CustomerName": row['CustomerName'],
            "InvoiceText": row['InvoiceText'],
            "RequestByInventory": row['RequestByInventory'],
            "TxVisitId": row['TxVisitId'],
            "VisitEntryId": row['VisitEntryId'],
            "RevocationVoucherIns": row['RevocationVoucherIns'],
        }
        info_delivery_bills.append(info_delivery_bill)

    bill_data = data_create_delivery_bill(info_delivery_bills)

    response_data, voucherid, id, createOn, createById = create_bills(bill_data)

    response_data, voucherout_ids, itemIds, recall_medicine_details = create_info_charge(voucherid)

    response_data, charge_details = create_charge(voucherout_ids)

    CreateAndSaveVoucherIn_data = data_CreateAndSaveVoucherIn(row, info_delivery_bills, voucherid, recall_medicine_details, charge_details)

    # Hết tồn sẽ báo không tạo được phiếu xuất
    Info_data = CreateAndSaveVoucherIn(CreateAndSaveVoucherIn_data)

    return Info_data


# Xuất khác (xuất hủy/thanh lý)
def other_export(test_data, testcase_id):
    from Dược.GET import liquidation_export
    test_data = test_data.loc[test_data['TestCaseId'] == testcase_id]

    # Đọc dữ liệu gốc từ tệp Excel
    excel_data = test_data

    info_delivery_bills = []

    for index, row in excel_data.iterrows():
        info_delivery_bill = {
            "PPU": int(row['PPU']),
            "VatPerc": int(row['VatPerc']),
            "LotId": int(row['LotId']),
            "ItemId": int(row['itemId']),
            "ItemSource": int(row['ItemSource']),
            "Qty": int(row['Qty']),
            "Status": int(row['Status']),
            "imsGetInvNowWithBy": row['imsGetInvNowWithBy'],
            "Type": int(row['Type']),
            "Type.1": int(row['Type.1']),
            "RefStoreId": row['RefStoreId'],
            "Description": str(row['Description']),
            "StoreId": int(row['StoreId']),
            "InvSource": int(row['InvSource']),
            "CreateById": int(row['CreateById']),
            "InvStatus": int(row['InvStatus']),
            "Attribute": row['Attribute'],
            "InvStatusDescription": row['InvStatusDescription'],
            "ProcStatusDescription": row['ProcStatusDescription'],
            "CustomerName": row['CustomerName'],
            "InvoiceText": row['InvoiceText'],
            "RequestByInventory": row['RequestByInventory'],
            "TxVisitId": row['TxVisitId'],
            "VisitEntryId": row['VisitEntryId'],
            "RevocationVoucherIns": row['RevocationVoucherIns'],
        }
        info_delivery_bills.append(info_delivery_bill)

    liquidation_export()

    bill_data = data_create_delivery_bill(info_delivery_bills)

    response_data, voucherid, id, createOn, createById, lotIds, StoreId = create_liquidation_bills(bill_data)

    response_data, voucherout_ids, itemIds, recall_medicine_details = create_info_charge(voucherid)

    response_data, charge_details = create_charge(voucherout_ids)

    ItemLots(lotIds)

    product_data = data_create_product(StoreId, itemIds)

    Info_data = create_product(product_data)

    return Info_data


# Hoàn trả - kho
def warehouse_return(test_data, testcase_id):
    test_data = test_data.loc[test_data['TestCaseId'] == testcase_id]

    # Đọc dữ liệu gốc từ tệp Excel
    excel_data = test_data

    info_delivery_bills = []

    for index, row in excel_data.iterrows():
        info_delivery_bill = {
            "PPU": int(row['PPU']),
            "VatPerc": int(row['VatPerc']),
            "LotId": int(row['LotId']),
            "ItemId": int(row['itemId']),
            "ItemSource": int(row['ItemSource']),
            "Qty": int(row['Qty']),
            "Status": int(row['Status']),
            "imsGetInvNowWithBy": row['imsGetInvNowWithBy'],
            "Type": int(row['Type']),
            "Type.1": int(row['Type.1']),
            "RefStoreId": row['RefStoreId'],
            "Description": str(row['Description']),
            "StoreId": int(row['StoreId']),
            "InvSource": int(row['InvSource']),
            "CreateById": int(row['CreateById']),
            "InvStatus": int(row['InvStatus']),
            "Attribute": row['Attribute'],
            "InvStatusDescription": row['InvStatusDescription'],
            "ProcStatusDescription": row['ProcStatusDescription'],
            "CustomerName": row['CustomerName'],
            "InvoiceText": row['InvoiceText'],
            "RequestByInventory": row['RequestByInventory'],
            "TxVisitId": row['TxVisitId'],
            "VisitEntryId": row['VisitEntryId'],
            "RevocationVoucherIns": row['RevocationVoucherIns'],
        }
        info_delivery_bills.append(info_delivery_bill)

    bill_data = data_create_delivery_bill(info_delivery_bills)

    response_data, voucherid, id, createOn, createById, lotIds, StoreId = create_warehouse_return_bills(bill_data)

    response_data, voucherout_ids, itemIds, recall_medicine_details = create_info_charge(voucherid)

    response_data, charge_details = create_charge(voucherout_ids)

    ItemLots(lotIds)

    product_data = data_create_warehouse_return(StoreId, lotIds)

    Info_data = create_product(product_data)

    return Info_data
