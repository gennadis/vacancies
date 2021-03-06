from itertools import count
from typing import Optional

import requests

from analytics import predict_salary, collect_vacancies_stats

HH_API_BASE_URL = "https://api.hh.ru"


def fetch_vacancies_from_hh(
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
    url = f"{HH_API_BASE_URL}/vacancies"
    params = {
        "professional_role": role_id,
        "area": area_id,
        "period": period,
        "text": text,
        "only_with_salary": True,
        "currency": currency,
        "per_page": per_page,
    }

    vacancies = []

    for page_number in count(0):
        params["page"] = page_number
        response = requests.get(url, params)
        response.raise_for_status()

        vacancies_page = response.json()
        vacancies.extend(vacancies_page["items"])

        if page_number >= vacancies_page["pages"]:
            break

    return vacancies_page["found"], vacancies


def predict_rub_salary_hh(vacancy: dict) -> Optional[int]:
    """Predict HH vacancy salary depending on various factors."""
    salary: dict = vacancy.get("salary")
    salary_from: int = salary.get("from")
    salary_to: int = salary.get("to")

    if salary.get("currency") != "RUR":
        return

    return int(predict_salary(salary_from, salary_to))


def collect_stats_from_hh_for(language: str) -> dict:
    """Get HeadHunter vacancies stats for passed programming language."""
    vacancies_count, vacancies = fetch_vacancies_from_hh(
        role_id=96,  # Developer
        area_id=1,  # Moscow
        period=30,  # last month
        text=language,
        per_page=100,
    )

    hh_stats = collect_vacancies_stats(
        vacancies_count, vacancies, predict_rub_salary_hh
    )

    return hh_stats
