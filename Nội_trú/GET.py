import datetime
import requests
import json
from Cấu_hình.Setup import base_url_4, auth_token_4, base_url_2, auth_token_2


def date_formatted():
    from Tiếp_nhận.GET import CurrentServerDateTime
    date = str(CurrentServerDateTime())
    date_value_trimmed = date[:20] + "+" + date[-6:]
    isit_on_value_trimmed = date_value_trimmed.replace('"', '')

    date_datetime = datetime.datetime.strptime(isit_on_value_trimmed, "%Y-%m-%dT%H:%M:%S%z")
    date_fomatted = date_datetime.strftime("%Y%m%d")
    print("Formated_visit_on: ", date_fomatted)
    return date_fomatted


# Load bệnh nhân ở màn hình DS chờ nhập khoa
def load_Patient_wait(date_fomatted):
    try:
        url = f"{base_url_4}/MedRecords/?fromDate={date_fomatted}000000&toDate={date_fomatted}235959&status=1&ptName=&YOB=&insCardNo=&ptCode=&disFromDate=&disToDate=&wardAdmStatus=1&medRcdType=2&icdCode=&expSettleFromDate=&expSettleToDate=&wardId=8"
        headers = {"Authorization": auth_token_4}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        visitIds = []
        if isinstance(response_data, list):
            for item in response_data:
                visitId = item.get("visitId", None)
                if visitId is not None:
                    visitIds.append(visitId)
        else:
            print("response_data is not a list")
        return response_data, visitIds
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        return []


def check_visit_enty(entry_id):
    visitIds = []
    try:
        url = f"{base_url_2}/VisitEntries/{entry_id}"
        headers = {"Authorization": auth_token_2}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        visitId = response_data.get("visitId", None)
        visitIds.append(visitId)
        return visitIds, response_data
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        return []


def check_information_patient_initial(visitIds):
    visit_idas = []
    for visit_id in visitIds:
        url = f"{base_url_2}/Visits/Id/{visit_id}?isGetDeleted=False"
        headers = {"Authorization": auth_token_2}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        visit_json = response.json()
        visit_id = visit_json["visitId"]
        insBenefitType = int(visit_json.get("insBenefitType", 0))
        if insBenefitType != 2:
            print(f"Visit with visit_id {visit_id} does not have insBenefitType equal to 2.")
            continue
        visit_idas.append(visit_id)
        return visit_idas, visit_json


# Lấy thông tin đợt điều trị
def take_data_Medrecord(visitIds):
    medRcdIds = []
    for visit_id in visitIds:
        url = f"{base_url_4}/MedRecords/VisitId/{visit_id}"
        headers = {"Authorization": auth_token_4}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            visit_json = response.json()
            if isinstance(visit_json, list):
                for item in visit_json:
                    medRcdId = item.get("medRcdId", None)
                    if medRcdId is not None:
                        print("medRcdId:", medRcdId)
                        insBenefitType = int(item.get("insBenefitType", 0))
                        if insBenefitType != 2:
                            print(f"Visit with visit_id {visit_id} does not have insBenefitType equal to 2.")
                            continue
                        medRcdIds.append(medRcdId)
            else:
                print("response_data is not a list")

            print("medRcdIds = ", medRcdIds)
            return medRcdIds, visit_json

        except requests.RequestException as e:
            print(f"Request failed: {e}")


# Lấy thông tin ở Medrecord
def get_Medrecords(medRcdIds):
    for medRcdId in medRcdIds:
        url = f"{base_url_4}/MedRecords/{medRcdId}"
        headers = {"Authorization": auth_token_4}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        Medrecords_json = response.json()
        return Medrecords_json

