import os

from dotenv import load_dotenv

from hh import collect_stats_from_hh_for
from superjob import collect_stats_from_sj_for
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

    hh_stats, sj_stats = {}, {}

    for language in programming_languages:
        hh_stats[language] = collect_stats_from_hh_for(language)
        sj_stats[language] = collect_stats_from_sj_for(language, sj_token)

    hh_table = create_table(table_headers, hh_stats, "HeadHunter Moscow")
    sj_table = create_table(table_headers, sj_stats, "SuperJob Moscow")

    print(hh_table)
    print(sj_table)


if __name__ == "__main__":
    main()
