from pprint import pprint

from hh import get_vacancies, get_vacancies_stats

HH_API_BASE_URL = "https://api.hh.ru"
HH_VACANCIES_ENDPOINT = "/vacancies"
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
    "1С",
]


def main():

    total_stats = {}

    for language in PROGRAMMING_LANGUAGES:
        vacancies = get_vacancies(
            base_url=HH_API_BASE_URL,
            endpoint=HH_VACANCIES_ENDPOINT,
            role_id=96,
            area_id=1,
            period=30,
            text=language,
            per_page=100,
        )
        total_stats[language] = get_vacancies_stats(vacancies)

    pprint(total_stats)


if __name__ == "__main__":
    main()
