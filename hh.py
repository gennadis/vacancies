import requests
from typing import Optional

from utils import predict_salary, collect_vacancies_stats


HH_API_BASE_URL = "https://api.hh.ru"


def fetch_vacancies_from_hh(
    base_url: str,
    endpoint: str,
    role_id: int,
    area_id: int,
    period: int,
    text: str,
    currency: str = "RUR",
    per_page: int = 20,
) -> list[dict]:
    """Get open vacancies from HeadHunter.

    API documentation:
    https://github.com/hhru/api/blob/master/docs_eng/vacancies.md
    """
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
    """Predict HH vacancy salary depending on various factors."""
    salary: dict = vacancy.get("salary")
    salary_from: int = salary.get("from")
    salary_to: int = salary.get("to")

    if salary.get("currency") != "RUR":
        return

    return int(predict_salary(salary_from, salary_to))


def collect_stats_from_hh(languages: list) -> dict:
    """Get HeadHunter vacancies stats for programming languages."""
    hh_stats = {}
    for language in languages:
        vacancies = fetch_vacancies_from_hh(
            base_url=HH_API_BASE_URL,
            endpoint="/vacancies",
            role_id=96,  # Developer
            area_id=1,  # Moscow
            period=30,  # last month
            text=language,
            per_page=100,
        )
        hh_stats[language] = collect_vacancies_stats(vacancies, predict_rub_salary_hh)

    return hh_stats
