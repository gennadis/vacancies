import requests
from pprint import pprint
from typing import Union

HH_BASE_API = "https://api.hh.ru"


def get_vacancies(
    base_url: str, endpoint: str, role_id: int, area_id: int, period: int, text: str
) -> list[dict]:

    url = f"{base_url}{endpoint}"
    params = {
        "professional_role": role_id,
        "area": area_id,
        "period": period,
        "text": text,
        "only_with_salary": True,
        "currency": "RUR",
    }

    response = requests.get(url, params)
    response.raise_for_status()

    return response.json()


def predict_rub_salary(vacancy: dict) -> Union[int, None]:
    salary: dict = vacancy.get("salary")
    salary_from: int = salary.get("from")
    salary_to: int = salary.get("to")
    currency: str = salary.get("currency")

    if currency != "RUR":
        return

    if salary_to is None:
        return int(salary_from * 1.2)

    if salary_from is None:
        return int(salary_to * 0.8)

    return int((salary_from + salary_to) / 2)


def get_vacancies_stats(vacancies: list[dict]) -> dict:
    statistics = {}

    salaries = []
    for vacancy in vacancies.get("items"):
        salary: Union[int, None] = predict_rub_salary(vacancy)
        if salary:
            salaries.append(salary)

    statistics["vacancies_found"] = vacancies.get("found")
    statistics["vacancies_processed"] = len(salaries)
    statistics["average_salary"] = int(sum(salaries) / len(salaries))

    return statistics


def main():
    total_stats = {}

    prog_languages = [
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

    for language in prog_languages:
        vacancies = get_vacancies(
            base_url=HH_BASE_API,
            endpoint="/vacancies",
            role_id=96,
            area_id=1,
            period=30,
            text=language,
        )
        total_stats[language] = get_vacancies_stats(vacancies)

    pprint(total_stats)


if __name__ == "__main__":
    main()
