import requests
import json
from Cấu_hình.Setup import base_url, auth_token

# Base url
base_url = base_url


# Auth token
auth_token = auth_token


# GET request
def CurrentServerDateTime():
    url = base_url + "/master/Masters/CurrentServerDateTime"
    headers = {
        "Authorization": auth_token
    }
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    json_data = response.json()
    json_str = json.dumps(json_data, indent=4)
    return json_str
