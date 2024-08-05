import requests
import json
from Cấu_hình.Setup import base_url_2, auth_token_2, base_url_3, auth_token_3


# GET request
def CurrentServerDateTime():
    url = base_url_3 + "/Masters/CurrentServerDateTime"
    headers = {
        "Authorization": auth_token_3
    }
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    json_data = response.json()
    json_str = json.dumps(json_data, indent=4)
    return json_str


# Hiển thị lại thông tin VisitOn
def Load_VisitOn(patientId):
    url = f"{base_url_2}/Visits/VisitHistory/{patientId}"
    headers = {"Authorization": auth_token_2}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    if isinstance(response_data, list):
        for item in response_data:
            rxCertId = item.get("rxCertId")
            return rxCertId