import os

from dotenv import load_dotenv

from hh import get_vacancies_hh, predict_rub_salary_hh
from superjob import get_vacancies_sj, predict_rub_salary_sj
from utils import get_vacancies_stats, get_table

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


def get_hh_total_stats(languages: list):
    """Get HeadHunter vacancies stats by given programming languages."""
    hh_total_stats = {}
    for language in languages:
        vacancies = get_vacancies_hh(
            base_url=HH_API_BASE_URL,
            endpoint=HH_VACANCIES_ENDPOINT,
            role_id=96,  # Developer
            area_id=1,  # Moscow
            period=30,  # last month
            text=language,
            per_page=100,
        )
        hh_total_stats[language] = get_vacancies_stats(vacancies, predict_rub_salary_hh)

    return hh_total_stats


def get_sj_total_stats(languages: list, token: str):
    """Get SuperJob vacancies stats by given programming languages."""
    sj_total_stats = {}
    for language in languages:
        vacancies = get_vacancies_sj(
            base_url=SJ_API_BASE_URL,
            endpoint=SJ_VACANCIES_ENDPOINT,
            token=token,
            town_id=4,  # Moscow
            profession_id=48,  # Developer
            keyword=language,
            per_page=100,
        )
        sj_total_stats[language] = get_vacancies_stats(vacancies, predict_rub_salary_sj)
    return sj_total_stats


def main():
    load_dotenv()
    superjob_token = os.getenv("SUPERJOB_TOKEN")

    table_headers = [
        "Язык программирования",
        "Вакансий найдено",
        "Вакансий обработано",
        "Средняя зарплата",
    ]

    hh_total_stats = get_hh_total_stats(PROGRAMMING_LANGUAGES)
    hh_table = get_table(table_headers, hh_total_stats, "HeadHunter")
    print(hh_table)

    sj_total_stats = get_sj_total_stats(PROGRAMMING_LANGUAGES, superjob_token)
    sj_table = get_table(table_headers, sj_total_stats, "SuperJob")
    print(sj_table)


if __name__ == "__main__":
    main()
