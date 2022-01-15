import os
import requests
from pprint import pprint
from typing import Optional

from dotenv import load_dotenv

from utils import predict_salary

SUPERJOB_API_URL = "https://api.superjob.ru/2.0"
ENDPOINT = "/vacancies"


def get_vacancies_sj(
    base_url: str,
    endpoint: str,
    token: str,
    town_id: int,
    profession_id: int,
    keyword: str,
) -> list[dict]:

    url = f"{base_url}{endpoint}"
    headers = {
        "X-Api-App-Id": token,
    }
    params = {
        "town": town_id,
        "catalogues": profession_id,
        "keyword": keyword,
    }

    response = requests.get(url=url, headers=headers, params=params)
    response.raise_for_status()

    vacancies = response.json()["objects"]
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

    vacancies = get_vacancies_sj(
        base_url=SUPERJOB_API_URL,
        endpoint=ENDPOINT,
        token=superjob_token,
        town_id=4,  # "Москва"
        profession_id=48,  # "Разработка, программирование"
        keyword="программист",
    )

    for vacancy in vacancies:
        print(
            vacancy["profession"],
            vacancy["town"]["title"],
            predict_rub_salary_sj(vacancy),
            sep=", ",
        )


if __name__ == "__main__":
    main()
