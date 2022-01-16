import requests
from typing import Optional

from utils import predict_salary


def get_vacancies_hh(
    base_url: str,
    endpoint: str,
    role_id: int,
    area_id: int,
    period: int,
    text: str,
    currency: str = "RUR",
    per_page: int = 20,
) -> list[dict]:

    url = f"{base_url}{endpoint}"
    params = {
        "professional_role": role_id,
        "area": area_id,
        "period": period,
        "text": text,
        "only_with_salary": True,
        "currency": currency,
        "per_page": per_page,
    }

    current_page = 0
    total_pages = 1

    vacancies = []

    while current_page < total_pages:
        params["page"] = current_page

        response = requests.get(url, params)
        response.raise_for_status()
        page_data = response.json()

        vacancies.extend(page_data["items"])
        total_pages = page_data["pages"]
        current_page += 1

    return vacancies


def predict_rub_salary_hh(vacancy: dict) -> Optional[int]:
    salary: dict = vacancy.get("salary")
    salary_from: int = salary.get("from")
    salary_to: int = salary.get("to")

    if salary.get("currency") != "RUR":
        return

    return int(predict_salary(salary_from, salary_to))
