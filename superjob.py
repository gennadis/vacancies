import os
from pprint import pprint

from dotenv import load_dotenv

import requests

SUPERJOB_API_URL = "https://api.superjob.ru/2.0"
ENDPOINT = "/vacancies"


def get_vacancies(
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


def main():
    load_dotenv()
    superjob_token = os.getenv("SUPERJOB_TOKEN")

    vacancies = get_vacancies(
        base_url=SUPERJOB_API_URL,
        endpoint=ENDPOINT,
        token=superjob_token,
        town_id=4,
        profession_id=48,
        keyword="программист",
    )

    for vacancie in vacancies:
        print(vacancie["profession"], vacancie["town"]["title"])


if __name__ == "__main__":
    main()
