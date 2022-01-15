import os
import requests
from pprint import pprint
from typing import Optional, Union

from dotenv import load_dotenv

from utils import predict_salary, get_vacancies_stats

SUPERJOB_API_URL = "https://api.superjob.ru/2.0"
ENDPOINT = "/vacancies"


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


def main():
    load_dotenv()
    superjob_token = os.getenv("SUPERJOB_TOKEN")

    prog_langs = [
        "Python",
        "Java",
        "JavaScript",
        "Kotlin",
        "Swift",
    ]

    total_stats = {}

    for language in prog_langs:

        vacancies = get_vacancies_sj(
            base_url=SUPERJOB_API_URL,
            endpoint=ENDPOINT,
            token=superjob_token,
            town_id=4,  # "Москва"
            profession_id=48,  # "Разработка, программирование"
            keyword=language,
            per_page=100,
        )

        total_stats[language] = get_vacancies_stats(vacancies, predict_rub_salary_sj)

    pprint(total_stats)


if __name__ == "__main__":
    main()
