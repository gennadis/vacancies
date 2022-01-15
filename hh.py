import requests
from pprint import pprint
from typing import Union

HH_BASE_API = "https://api.hh.ru"


def get_vacancies(
    base_url: str,
    endpoint: str,
    role_id: int,
    area_id: int,
    period: int,
    text: str,
    currency: str = "RUR",
    per_page: int = 20,
) -> list[dict]:

    url = f"{base_url}{endpoint}"
    params = {
        "professional_role": role_id,
        "area": area_id,
        "period": period,
        "text": text,
        "only_with_salary": True,
        "currency": currency,
        "per_page": per_page,
    }

    current_page = 0
    total_pages = 1

    vacancies = []

    while current_page < total_pages:
        params["page"] = current_page

        response = requests.get(url, params)
        response.raise_for_status()
        page_data = response.json()

        vacancies.extend(page_data["items"])
        total_pages = page_data["pages"]
        current_page += 1

    return vacancies


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

    python = get_vacancies(
        base_url=HH_BASE_API,
        endpoint="/vacancies",
        role_id=96,
        area_id=1,
        period=30,
        text="python",
        per_page=100,
    )
    print(len(python))


if __name__ == "__main__":
    main()
