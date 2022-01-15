import requests
from pprint import pprint

HH_BASE_API = "https://api.hh.ru"
DEVELOPER_ROLE_ID = 96


def get_vacacnies(base_url, endpoint, role_id):

    url = f"{base_url}{endpoint}"
    params = {"professional_role": role_id}

    response = requests.get(url, params)
    response.raise_for_status()

    return response.json()


pprint(get_vacacnies(HH_BASE_API, "/vacancies", DEVELOPER_ROLE_ID))
