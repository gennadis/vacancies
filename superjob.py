import requests
from typing import Optional

from utils import predict_salary


def get_vacancies_sj(
    base_url: str,
    endpoint: str,
    token: str,
    town_id: int,
    profession_id: int,
    keyword: str,
    per_page: int = 20,
) -> list[dict]:

    url = f"{base_url}{endpoint}"
    headers = {
        "X-Api-App-Id": token,
    }
    params = {
        "town": town_id,
        "catalogues": profession_id,
        "keyword": keyword,
        "count": per_page,
    }

    current_page = 0
    more_pages = True

    vacancies = []

    while more_pages:
        params["page"] = current_page

        response = requests.get(url=url, headers=headers, params=params)
        response.raise_for_status()

        page_data = response.json()

        vacancies.extend(page_data.get("objects"))

        more_pages = page_data["more"]
        current_page += 1

    return vacancies


def predict_rub_salary_sj(vacancy: dict) -> Optional[int]:
    salary_from: int = vacancy.get("payment_from")
    salary_to: int = vacancy.get("payment_to")

    if vacancy.get("currency") != "rub":
        return
    if salary_from == salary_to == 0:
        return
    return int(predict_salary(salary_from, salary_to))
