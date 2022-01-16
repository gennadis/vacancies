import os

from dotenv import load_dotenv
from terminaltables import SingleTable

from hh import get_vacancies_hh, predict_rub_salary_hh
from superjob import get_vacancies_sj, predict_rub_salary_sj
from utils import get_vacancies_stats, prepare_table

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
    hh_table_data = prepare_table(table_headers=table_headers, content=hh_total_stats)
    hh_table = SingleTable(hh_table_data)
    hh_table.title = "HeadHunter"
    print(hh_table.table)

    sj_total_stats = get_sj_total_stats(PROGRAMMING_LANGUAGES, superjob_token)
    sj_table_data = prepare_table(table_headers=table_headers, content=sj_total_stats)
    sj_table = SingleTable(sj_table_data)
    sj_table.title = "SuperJob"
    print(sj_table.table)


if __name__ == "__main__":
    main()
