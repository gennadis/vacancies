import os

from dotenv import load_dotenv

from hh import collect_stats_from_hh
from superjob import collect_stats_from_sj
from analytics import create_table


def main():
    load_dotenv()
    sj_token = os.getenv("SUPERJOB_TOKEN")

    programming_languages = [
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
    table_headers = [
        "Язык программирования",
        "Вакансий найдено",
        "Вакансий обработано",
        "Средняя зарплата",
    ]

    hh_stats = collect_stats_from_hh(programming_languages)
    hh_table = create_table(table_headers, hh_stats, "HeadHunter Moscow")
    print(hh_table)

    sj_stats = collect_stats_from_sj(programming_languages, sj_token)
    sj_table = create_table(table_headers, sj_stats, "SuperJob Moscow")
    print(sj_table)


if __name__ == "__main__":
    main()
