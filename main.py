import os
from pprint import pprint

from dotenv import load_dotenv

from hh import get_vacancies_hh, predict_rub_salary_hh
from superjob import get_vacancies_sj, predict_rub_salary_sj
from utils import get_vacancies_stats

HH_API_BASE_URL = "https://api.hh.ru"
HH_VACANCIES_ENDPOINT = "/vacancies"

SJ_API_BASE_URL = "https://api.superjob.ru/2.0"
SJ_VACANCIES_ENDPOINT = "/vacancies"

PROGRAMMING_LANGUAGES = [
    "JavaScript",
    "Python",
    "Go",
    "Java",
    "Kotlin",
    "C#",
    "PHP",
    "Swift",
    "Ruby",
]


def main():

    load_dotenv()
    superjob_token = os.getenv("SUPERJOB_TOKEN")

    hh_total_stats = {}
    for language in PROGRAMMING_LANGUAGES:
        vacancies = get_vacancies_hh(
            base_url=HH_API_BASE_URL,
            endpoint=HH_VACANCIES_ENDPOINT,
            role_id=96,  # Developer
            area_id=1,  # Moscow
            period=30,
            text=language,
            per_page=100,
        )
        hh_total_stats[language] = get_vacancies_stats(vacancies, predict_rub_salary_hh)
    pprint(hh_total_stats)

    print("-" * 35)

    sj_total_stats = {}
    for language in PROGRAMMING_LANGUAGES:
        vacancies = get_vacancies_sj(
            base_url=SJ_API_BASE_URL,
            endpoint=SJ_VACANCIES_ENDPOINT,
            token=superjob_token,
            town_id=4,  # Moscow
            profession_id=48,  # Developer
            keyword=language,
            per_page=100,
        )
        sj_total_stats[language] = get_vacancies_stats(vacancies, predict_rub_salary_sj)
    pprint(sj_total_stats)


if __name__ == "__main__":
    main()
