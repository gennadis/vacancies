import os
from pprint import pprint

from dotenv import load_dotenv

import requests

SUPERJOB_API_URL = "https://api.superjob.ru/2.0"
ENDPOINT = "/vacancies"


def get_vacancies(base_url: str, endpoint: str, token: str) -> list[dict]:

    url = f"{base_url}{endpoint}"
    headers = {
        "X-Api-App-Id": token,
    }

    response = requests.get(url=url, headers=headers)
    response.raise_for_status()

    vacancies = response.json()["objects"]
    return vacancies


def main():
    load_dotenv()
    superjob_token = os.getenv("SUPERJOB_TOKEN")

    vacancies = get_vacancies(SUPERJOB_API_URL, ENDPOINT, superjob_token)

    for vacancie in vacancies:
        print(vacancie["profession"])


if __name__ == "__main__":
    main()
