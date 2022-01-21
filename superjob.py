from itertools import count
from typing import Optional

import requests

from analytics import predict_salary, collect_vacancies_stats

SJ_API_BASE_URL = "https://api.superjob.ru/2.0"


def fetch_vacancies_from_sj(
    base_url: str,
    token: str,
    town_id: int,
    profession_id: int,
    keyword: str,
    per_page: int = 20,
) -> list[dict]:
    """Get open vacancies from SuperJob.

    API documentation:
    https://api.superjob.ru/#search_vacanices
    """
    url = f"{base_url}/vacancies"
    headers = {
        "X-Api-App-Id": token,
    }
    params = {
        "town": town_id,
        "catalogues": profession_id,
        "keyword": keyword,
        "count": per_page,
    }

    vacancies = []

    for page_number in count(0):
        params["page"] = page_number
        response = requests.get(url=url, headers=headers, params=params)
        response.raise_for_status()

        vacancies_page = response.json()

        vacancies.extend(vacancies_page.get("objects"))

        if not vacancies_page["more"]:
            break

    return vacancies_page["total"], vacancies


def predict_rub_salary_sj(vacancy: dict) -> Optional[int]:
    """Predict SuperJob vacancy salary depending on various factors."""
    salary_from: int = vacancy.get("payment_from")
    salary_to: int = vacancy.get("payment_to")

    if vacancy.get("currency") != "rub":
        return
    if not salary_from and not salary_to:
        return
    return int(predict_salary(salary_from, salary_to))


def collect_stats_from_sj_for(language: str, token: str) -> dict:
    """Get SuperJob vacancies stats for passed programming language."""
    vacancies_count, vacancies = fetch_vacancies_from_sj(
        base_url=SJ_API_BASE_URL,
        token=token,
        town_id=4,  # Moscow
        profession_id=48,  # Developer
        keyword=language,
        per_page=100,
    )
    sj_stats = collect_vacancies_stats(
        vacancies_count, vacancies, predict_rub_salary_sj
    )
    return sj_stats
