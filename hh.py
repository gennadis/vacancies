import requests
from pprint import pprint

HH_BASE_API = "https://api.hh.ru"


def get_vacacnies(
    base_url: str, endpoint: str, role_id: int, area_id: int, period: int
):

    url = f"{base_url}{endpoint}"
    params = {
        "professional_role": role_id,
        "area": area_id,
        "period": period,
    }

    response = requests.get(url, params)
    response.raise_for_status()

    return response.json()


pprint(get_vacacnies(HH_BASE_API, "/vacancies", 96, 1, 30))
