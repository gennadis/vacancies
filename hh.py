from locale import currency
import requests
from pprint import pprint

HH_BASE_API = "https://api.hh.ru"
PROG_LANGUAGES = ["JavaScript", "Python", "Go", "Java", "Kotlin", "C++", "PHP", "Swift"]


def get_vacacnies(
    base_url: str, endpoint: str, role_id: int, area_id: int, period: int, text: str
):

    url = f"{base_url}{endpoint}"
    params = {
        "professional_role": role_id,
        "area": area_id,
        "period": period,
        "text": text,
    }

    response = requests.get(url, params)
    response.raise_for_status()

    return response.json()


def predict_rub_salary(vacancy: dict) -> int:
    salary: dict = vacancy.get("salary")
    salary_from: int = salary.get("from")
    salary_to: int = salary.get("to")
    currency: str = salary.get("currency")

    if currency != "RUR":
        return

    if salary_to is None:
        return salary_from * 1.2

    if salary_from is None:
        return salary_to * 0.8

    return (salary_from + salary_to) / 2


def main():
    python_jobs = get_vacacnies(HH_BASE_API, "/vacancies", 96, 1, 30, "python")["items"]
    for job in python_jobs:
        print(predict_rub_salary(job))


if __name__ == "__main__":
    main()
