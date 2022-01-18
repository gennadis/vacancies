import requests
from typing import Optional

from utils import predict_salary, collect_vacancies_stats


SJ_API_BASE_URL = "https://api.superjob.ru/2.0"
SJ_VACANCIES_ENDPOINT = "/vacancies"


def fetch_vacancies_from_sj(
    base_url: str,
    endpoint: str,
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
    """Predict SuperJob vacancy salary depending on various factors."""
    salary_from: int = vacancy.get("payment_from")
    salary_to: int = vacancy.get("payment_to")

    if vacancy.get("currency") != "rub":
        return
    if salary_from == salary_to == 0:
        return
    return int(predict_salary(salary_from, salary_to))


def collect_stats_from_sj(languages: list, token: str) -> dict:
    """Get SuperJob vacancies stats for programming languages."""
    sj_stats = {}
    for language in languages:
        vacancies = fetch_vacancies_from_sj(
            base_url=SJ_API_BASE_URL,
            endpoint=SJ_VACANCIES_ENDPOINT,
            token=token,
            town_id=4,  # Moscow
            profession_id=48,  # Developer
            keyword=language,
            per_page=100,
        )
        sj_stats[language] = collect_vacancies_stats(vacancies, predict_rub_salary_sj)
    return sj_stats
